import json

from Crypto.Hash import RIPEMD160, SHA256


def calculate_hash(data, hash_function: str = "sha256") -> str:
    if type(data) == str:
        data = bytearray(data, "utf-8")
    if hash_function == "sha256":
        h = SHA256.new()
        h.update(data)
        return h.hexdigest()
    if hash_function == "ripemd160":
        h = RIPEMD160.new()
        h.update(data)
        return h.hexdigest()


def generate_transaction_data(sender_bitcoin_address, receiver_bitcoin_address, amount: int) -> dict:
    return {
        "sender": sender_bitcoin_address,
        "receiver": receiver_bitcoin_address,
        "amount": amount
    }


def convert_transaction_data_to_bytes(transaction_data: dict):
    new_transaction_data = transaction_data.copy()
    new_transaction_data["sender"] = str(transaction_data["sender"])
    new_transaction_data["receiver"] = str(transaction_data["receiver"])
    new_transaction_data["amount"] = str(transaction_data["amount"])
    return json.dumps(new_transaction_data, indent=2).encode('utf-8')
