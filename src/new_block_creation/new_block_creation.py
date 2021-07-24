import json
from datetime import datetime

from common.utils import calculate_hash
from common.block import Block
from common.merkle_tree import build_merkle_tree
from multiprocessing import shared_memory

NUMBER_OF_ZEROS = 3


class BlockException(Exception):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message


class NewBlockHeader:
    def __init__(self, previous_block_hash: str, merkle_root: str):
        self.previous_block_hash = previous_block_hash
        self.merkle_root = merkle_root
        self.timestamp = datetime.timestamp(datetime.now())
        self.noonce = self.get_noonce()

    def get_noonce(self) -> int:  # proof-of-work
        block_header_hash = ""
        self.noonce = 0
        starting_zeros = "".join([str(0) for _ in range(NUMBER_OF_ZEROS)])
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


class ProofOfWork:
    def __init__(self, blockchain: Block):
        self.blockchain = blockchain

    def __enter__(self):
        self.mem_pool = shared_memory.ShareableList(name='mem_pool')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.mem_pool.shm.close()

    def create_new_block(self):
        transactions = [json.loads(a) for a in self.mem_pool]
        if transactions:
            new_block = NewBlock(previous_block_hash=self.blockchain.block_header.hash,
                                 transactions=transactions)
            return new_block
        else:
            raise BlockException("", "No transaction in mem_pool")
