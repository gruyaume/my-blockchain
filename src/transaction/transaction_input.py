import binascii
import json


class TransactionInput:
    def __init__(self, transaction_hash: str, output_index: int, public_key: bytes = b"", signature: str = "", ):
        self.transaction_hash = transaction_hash
        self.output_index = output_index
        self.public_key = public_key
        self.signature = signature

    def to_json(self) -> str:
        return json.dumps({
            "transaction_hash": self.transaction_hash,
            "output_index": self.output_index,
            "public_key": self.public_key.decode("utf-8"),
            "signature": binascii.hexlify(self.signature).decode("utf-8")
        })
