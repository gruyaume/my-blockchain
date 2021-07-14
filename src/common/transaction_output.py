import json


class TransactionOutput:
    def __init__(self, public_key_hash: bytes, amount: int):
        self.amount = amount
        self.locking_script = f"OP_DUP OP_HASH160 {public_key_hash} OP_EQUAL_VERIFY OP_CHECKSIG"

    def to_json(self) -> str:
        return json.dumps({
            "amount": self.amount,
            "locking_script": self.locking_script
        })
