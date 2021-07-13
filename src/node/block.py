import json

from node.utils import calculate_hash


class Block:
    def __init__(
            self,
            timestamp: float,
            transaction_data: str,
            previous_block=None,
    ):
        self.transaction_data = transaction_data
        self.timestamp = timestamp
        self.previous_block = previous_block

    @property
    def previous_block_cryptographic_hash(self):
        previous_block_cryptographic_hash = ""
        if self.previous_block:
            previous_block_cryptographic_hash = self.previous_block.cryptographic_hash
        return previous_block_cryptographic_hash

    @property
    def cryptographic_hash(self) -> str:
        block_content = {
            "transaction_data": self.transaction_data,
            "timestamp": self.timestamp,
            "previous_block_cryptographic_hash": self.previous_block_cryptographic_hash
        }
        block_content_bytes = json.dumps(block_content, indent=2).encode('utf-8')
        return calculate_hash(block_content_bytes)
