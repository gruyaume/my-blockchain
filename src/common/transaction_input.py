import json


class TransactionInput:
    def __init__(self, transaction_hash: str, output_index: int, public_key: str = "", signature: str = ""):
        self.transaction_hash = transaction_hash
        self.output_index = output_index
        self.public_key = public_key
        self.signature = signature

    def to_json(self, with_signature_and_public_key: bool = True) -> str:
        if with_signature_and_public_key:
            return json.dumps({
                "transaction_hash": self.transaction_hash,
                "output_index": self.output_index,
                "public_key": self.public_key,
                "signature": self.signature
            })
        else:
            return json.dumps({
                "transaction_hash": self.transaction_hash,
                "output_index": self.output_index
            })
