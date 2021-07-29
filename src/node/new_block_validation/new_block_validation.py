from common.block import Block, BlockHeader
from common.io_blockchain import store_blockchain_in_memory
from common.values import NUMBER_OF_LEADING_ZEROS
from node.transaction_validation.transaction_validation import Transaction


class NewBlockException(Exception):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message


class NewBlock:
    def __init__(self, blockchain: Block):
        self.blockchain = blockchain
        self.new_block = None

    def receive(self, new_block: dict):
        block_header = BlockHeader(**new_block["header"])
        self.new_block = Block(transactions=new_block["transactions"], block_header=block_header)
        try:
            assert self.blockchain.block_header.hash == self.new_block.block_header.previous_block_hash
        except AssertionError:
            print("Previous block provided is not the most recent block")
            raise NewBlockException("", "Previous block provided is not the most recent block")

    def validate(self):
        self._validate_hash()
        self._validate_transactions()

    def _validate_hash(self):
        new_block_hash = self.new_block.block_header.get_hash()
        number_of_zeros_string = "".join([str(0) for _ in range(NUMBER_OF_LEADING_ZEROS)])
        try:
            assert new_block_hash.startswith(number_of_zeros_string)
        except AssertionError:
            print('Proof of work validation failed')
            raise NewBlockException("", "Proof of work validation failed")

    def _validate_transactions(self):
        for transaction in self.new_block.transactions:
            transaction_validation = Transaction(self.blockchain)
            transaction_validation.receive(transaction=transaction)
            transaction_validation.validate()
            transaction_validation.validate_funds()

    def add(self):
        self.new_block.previous_block = self.blockchain
        store_blockchain_in_memory(self.new_block)
