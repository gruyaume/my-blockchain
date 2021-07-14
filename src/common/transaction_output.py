import json


class TransactionOutput:
    def __init__(self, public_key_hash: str, amount: int):
        self.amount = amount
        self.public_key_hash = public_key_hash

    def to_json(self) -> str:
        return json.dumps({
            "amount": self.amount,
            "public_key_hash": self.public_key_hash
        })
