import json
from datetime import datetime
from multiprocessing import shared_memory

import requests

from common.block import Block
from common.merkle_tree import build_merkle_tree
from common.node import Node
from common.utils import calculate_hash

NUMBER_OF_LEADING_ZEROS = 3


class BlockException(Exception):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message


class OtherNode(Node):
    def __init__(self, ip: str, port: int):
        super().__init__(ip, port)

    def send_new_block(self, block: dict) -> requests.Response:
        return self.post(endpoint="new_block", data=block)


class NewBlockHeader:
    def __init__(self, previous_block_hash: str, merkle_root: str):
        self.previous_block_hash = previous_block_hash
        self.merkle_root = merkle_root
        self.timestamp = datetime.timestamp(datetime.now())
        self.noonce = self.get_noonce()

    def get_noonce(self) -> int:  # proof-of-work
        block_header_hash = ""
        self.noonce = 0
        starting_zeros = "".join([str(0) for _ in range(NUMBER_OF_LEADING_ZEROS)])
        while not block_header_hash.startswith(starting_zeros):
            self.noonce = self.noonce + 1
            block_header_hash = self.hash
        return self.noonce

    @property
    def data(self):
        return {"previous_block_hash": self.previous_block_hash,
                "merkle_root": self.merkle_root,
                "timestamp": self.timestamp,
                "noonce": self.noonce}

    @property
    def hash(self):
        return calculate_hash(json.dumps(self.data))


class NewBlock:
    def __init__(self, previous_block_hash: str, transactions: [dict]):
        transactions_bytes = [json.dumps(transaction, indent=2).encode('utf-8') for transaction in transactions]
        merkle_tree = build_merkle_tree(transactions_bytes)
        self.block_header = NewBlockHeader(previous_block_hash, merkle_tree.value)
        self.transactions = transactions

    def to_json(self) -> dict:
        return {"header": self.block_header.data,
                "transactions": self.transactions}


class ProofOfWork:
    def __init__(self, blockchain: Block):
        self.blockchain = blockchain
        self.new_block = None

    def __enter__(self):
        self.mem_pool = shared_memory.ShareableList(name='mem_pool')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.mem_pool.shm.close()

    def create_new_block(self):
        transactions = [json.loads(a) for a in self.mem_pool]
        if transactions:
            self.new_block = NewBlock(previous_block_hash=self.blockchain.block_header.hash,
                                      transactions=transactions)
        else:
            raise BlockException("", "No transaction in mem_pool")

    def broadcast(self):
        node_list = [OtherNode("127.0.0.1", 5001), OtherNode("127.0.0.1", 5002)]
        for node in node_list:
            try:
                node.send_new_block(self.new_block.to_json)
            except requests.ConnectionError:
                pass
