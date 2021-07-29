import json

from common.utils import calculate_hash


class BlockHeader:
    def __init__(self, previous_block_hash: str, timestamp: float, noonce: int, merkle_root: str, hash: str = ""):

        self.previous_block_hash = previous_block_hash
        self.merkle_root = merkle_root
        self.timestamp = timestamp
        self.noonce = noonce
        self.hash = hash
        if not self.hash:
            self.hash = self.get_hash()

    def __eq__(self, other):
        try:
            assert self.previous_block_hash == other.previous_block_hash
            assert self.merkle_root == other.merkle_root
            assert self.timestamp == other.timestamp
            assert self.noonce == other.noonce
            assert self.hash == other.hash
            return True
        except AssertionError:
            return False

    def get_hash(self) -> str:
        header_data = {"previous_block_hash": self.previous_block_hash,
                       "merkle_root": self.merkle_root,
                       "timestamp": self.timestamp,
                       "noonce": self.noonce}
        return calculate_hash(json.dumps(header_data))

    @property
    def to_dict(self) -> dict:
        return {
            "previous_block_hash": self.previous_block_hash,
            "merkle_root": self.merkle_root,
            "timestamp": self.timestamp,
            "noonce": self.noonce,
            "hash": self.hash
        }

    def __str__(self):
        return json.dumps(self.to_dict)

    @property
    def to_json(self) -> str:
        return json.dumps(self.to_dict)


class Block:
    def __init__(
            self,
            transactions: [dict],
            block_header: BlockHeader,
            previous_block=None,
    ):
        self.block_header = block_header
        self.transactions = self.set_transactions_hashes(transactions)
        self.previous_block = previous_block

    def __eq__(self, other):
        try:
            assert self.block_header == other.block_header
            assert self.transactions == other.transactions
            return True
        except AssertionError:
            return False

    def __len__(self) -> int:
        i = 1
        current_block = self
        while current_block.previous_block:
            i = i + 1
            current_block = current_block.previous_block
        return i

    def __str__(self):
        return json.dumps({"timestamp": self.block_header.timestamp,
                           "hash": self.block_header.hash,
                           "transactions": self.transactions})

    @property
    def to_json(self) -> str:
        block_list = []
        current_block = self
        while current_block:

            block_data = {
                "header": current_block.block_header.to_json,
                "transactions": current_block.transactions
            }
            block_list.append(block_data)
            current_block = current_block.previous_block
        return json.dumps(block_list)

    @staticmethod
    def set_transactions_hashes(transactions: list) -> list:
        for transaction in transactions:
            transaction_data = {"inputs": transaction["inputs"],
                                "outputs": transaction["outputs"]}
            transaction_bytes = json.dumps(transaction_data, indent=2).encode('utf-8')
            transaction["transaction_hash"] = calculate_hash(transaction_bytes)
        return transactions
