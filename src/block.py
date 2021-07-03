import hashlib


class Block(object):
    def __init__(self, timestamp: float, transaction_data: str, previous_block_cryptographic_hash=None):
        self.transaction_data = transaction_data
        self.timestamp = timestamp
        self.previous_block_cryptographic_hash = previous_block_cryptographic_hash

    def cryptographic_hash(self) -> str:
        block_data_string = f"{self.transaction_data}; {self.timestamp}; {self.previous_block_cryptographic_hash}"
        block_data_bytes = bytearray(block_data_string, "utf-8")
        block_hash = hashlib.sha256(block_data_bytes).hexdigest()
        return block_hash
