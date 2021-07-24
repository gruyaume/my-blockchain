import json

from common.utils import calculate_hash
from node.merkle_tree import build_merkle_tree


class Block:
    def __init__(
            self,
            timestamp: float,
            transactions: [dict],
            previous_block=None,
    ):
        self.transactions = self.set_transactions_hashes(transactions)
        self.timestamp = timestamp
        self.previous_block = previous_block
        self.hash = ""
        self.merkle_root = self.get_merkle_root()

    def __str__(self):
        return json.dumps({"timestamp": self.timestamp,
                           "hash": self.hash,
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
