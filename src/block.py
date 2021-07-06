from utils import calculate_hash


class Block:
    def __init__(self, timestamp: float, transaction_data: str, previous_block_cryptographic_hash=None):
        self.transaction_data = transaction_data
        self.timestamp = timestamp
        self.previous_block_cryptographic_hash = previous_block_cryptographic_hash

    def cryptographic_hash(self) -> str:
        return calculate_hash(f"{self.transaction_data}; {self.timestamp}; {self.previous_block_cryptographic_hash}")
