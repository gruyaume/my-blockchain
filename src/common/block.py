import json

from common.utils import calculate_hash
from common.merkle_tree import build_merkle_tree


class BlockHeader:
    def __init__(self, previous_block_hash, merkle_root, timestamp, noonce):
        self.previous_block_hash = previous_block_hash
        self.merkle_root = merkle_root
        self.timestamp = timestamp
        self.noonce = noonce

    @property
    def hash(self) -> str:
        header_data = {"previous_block_hash": self.previous_block_hash,
                       "merkle_root": self.merkle_root,
                       "timestamp": self.timestamp,
                       "noonce": self.noonce}
        return calculate_hash(json.dumps(header_data))


class Block:
    def __init__(
            self,
            timestamp: float,
            transactions: [dict],
            noonce: int,
            previous_block=None,
    ):

        self.transactions = self.set_transactions_hashes(transactions)
        self.previous_block = previous_block
        merkle_root = self.get_merkle_root()
        previous_block_hash = calculate_hash("1111")
        if self.previous_block:
            previous_block_hash = previous_block.block_header.hash
        self.block_header = BlockHeader(previous_block_hash=previous_block_hash,
                                        merkle_root=merkle_root,
                                        timestamp=timestamp,
                                        noonce=noonce)

    def __str__(self):
        return json.dumps({"timestamp": self.block_header.timestamp,
                           "hash": self.block_header.hash,
                           "transactions": self.transactions})

    @staticmethod
    def set_transactions_hashes(transactions: list) -> list:
        for transaction in transactions:
            transaction_bytes = json.dumps(transaction, indent=2).encode('utf-8')
            transaction["transaction_hash"] = calculate_hash(transaction_bytes)
        return transactions

    def get_merkle_root(self) -> str:
        transactions_bytes = [json.dumps(transaction, indent=2).encode('utf-8') for transaction in self.transactions]
        merkle_tree = build_merkle_tree(transactions_bytes)
        return merkle_tree.value
