import json

from common.block import Block
from common.utils import calculate_hash
from common.values import NUMBER_OF_LEADING_ZEROS
from node.transaction_validation.transaction_validation import Transaction


class NewBlockException(Exception):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message


class NewBlock:
    def __init__(self, blockchain: Block):
        self.blockchain = blockchain
        self.new_block = dict()
        self.header = None
        self.transactions = []

    def receive(self, new_block: dict):
        self.new_block = new_block
        self.header = new_block["header"]
        self.transactions = new_block["transactions"]

    def validate(self):
        self._validate_hash()
        self._validate_transactions()

    def _validate_hash(self):
        hash = calculate_hash(json.dumps(self.header))
        number_of_zeros_string = "".join([str(0) for _ in range(NUMBER_OF_LEADING_ZEROS)])
        assert hash.startswith(number_of_zeros_string)

    def _validate_transactions(self):
        for transaction in self.transactions:
            transaction_validation = Transaction(self.blockchain)
            transaction_validation.receive(transaction=transaction)
            transaction_validation.validate()
            transaction_validation.validate_funds()

    def add(self):
        new_block = Block(transactions=self.transactions,
                          noonce=self.header["noonce"],
                          timestamp=self.header["timestamp"])
        new_block.previous_block = self.blockchain
        self.blockchain = new_block
