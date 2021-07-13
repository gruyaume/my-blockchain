import json


class TransactionOutput:
    def __init__(self, receiver_address: bytes, amount: int):
        self.amount = amount
        self.receiver_address = receiver_address

    def to_json(self) -> str:
        return json.dumps({
            "amount": self.amount,
            "receiver_address": self.receiver_address.decode("utf-8")
        })
