import json
from datetime import datetime

import requests

from common.block import Block, BlockHeader
from common.io_blockchain import get_blockchain_from_memory
from common.io_mem_pool import get_transactions_from_memory
from common.merkle_tree import get_merkle_root
from common.node import Node
from common.utils import calculate_hash
from common.values import NUMBER_OF_LEADING_ZEROS


class BlockException(Exception):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message


class OtherNode(Node):
    def __init__(self, ip: str, port: int):
        super().__init__(ip, port)

    def send_new_block(self, block: dict) -> requests.Response:
        return self.post(endpoint="block", data=block)


class ProofOfWork:
    def __init__(self):
        self.blockchain = get_blockchain_from_memory()
        self.new_block = None

    @staticmethod
    def get_noonce(block_header: BlockHeader) -> int:
        block_header_hash = ""
        noonce = block_header.noonce
        starting_zeros = "".join([str(0) for _ in range(NUMBER_OF_LEADING_ZEROS)])
        while not block_header_hash.startswith(starting_zeros):
            noonce = noonce + 1
            block_header_content = {
                "previous_block_hash": block_header.previous_block_hash,
                "merkle_root": block_header.merkle_root,
                "timestamp": block_header.timestamp,
                "noonce": noonce
            }
            block_header_hash = calculate_hash(json.dumps(block_header_content))
        return noonce

    def create_new_block(self):
        transactions = get_transactions_from_memory()
        if transactions:
            block_header = BlockHeader(
                merkle_root=get_merkle_root(transactions),
                previous_block_hash=self.blockchain.block_header.hash,
                timestamp=datetime.timestamp(datetime.now()),
                noonce=0
            )
            block_header.noonce = self.get_noonce(block_header)
            block_header.hash = block_header.get_hash()
            self.new_block = Block(transactions=transactions, block_header=block_header)
        else:
            raise BlockException("", "No transaction in mem_pool")

    def broadcast(self):
        node_list = [OtherNode("127.0.0.1", 5000)]
        for node in node_list:
            block_content = {
                "block": {
                    "header": self.new_block.block_header.to_dict,
                    "transactions": self.new_block.transactions
                }
            }
            node.send_new_block(block_content)
