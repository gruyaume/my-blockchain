import logging

import requests

from common.block import Block, BlockHeader
from common.io_mem_pool import MemPool
from common.io_known_nodes import KnownNodesMemory
from common.io_blockchain import BlockchainMemory
from common.values import NUMBER_OF_LEADING_ZEROS, BLOCK_REWARD
from node.transaction_validation.transaction_validation import Transaction


class NewBlockException(Exception):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message


class NewBlock:
    def __init__(self, blockchain: Block,  hostname: str):
        self.blockchain = blockchain
        self.new_block = None
        self.sender = ""
        self.mempool = MemPool()
        self.known_nodes_memory = KnownNodesMemory()
        self.blockchain_memory = BlockchainMemory()
        self.hostname = hostname

    def receive(self, new_block: dict, sender: str):
        block_header = BlockHeader(**new_block["header"])
        self.new_block = Block(transactions=new_block["transactions"], block_header=block_header)
        self.sender = sender
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
        input_amount = 0
        output_amount = 0
        for transaction in self.new_block.transactions:
            transaction_validation = Transaction(self.blockchain, self.hostname)
            transaction_validation.receive(transaction=transaction)
            transaction_validation.validate()
            input_amount = input_amount + transaction_validation.get_total_amount_in_inputs()
            output_amount = output_amount + transaction_validation.get_total_amount_in_outputs()
        self._validate_funds(input_amount, output_amount)

    @staticmethod
    def _validate_funds(input_amount: float, output_amount: float):
        assert input_amount + BLOCK_REWARD == output_amount

    def add(self):
        self.new_block.previous_block = self.blockchain
        self.blockchain_memory.store_blockchain_in_memory(self.new_block)

    def clear_block_transactions_from_mempool(self):
        current_transactions = self.mempool.get_transactions_from_memory()
        transactions_cleared = [i for i in current_transactions if not (i in self.new_block.transactions)]
        self.mempool.store_transactions_in_memory(transactions_cleared)

    def broadcast(self):
        logging.info(f"Broadcasting block")
        node_list = self.known_nodes_memory.known_nodes
        for node in node_list:
            if node.hostname != self.hostname and node.hostname != self.sender:
                block_content = {
                    "block": {
                        "header": self.new_block.block_header.to_dict,
                        "transactions": self.new_block.transactions
                    },
                    "sender": self.hostname
                }
                try:
                    logging.info(f"Broadcasting to {node.hostname}")
                    node.send_new_block(block_content)
                except requests.exceptions.HTTPError as error:
                    logging.info(f"Failed to broadcast block to {node.hostname}: {error}")
