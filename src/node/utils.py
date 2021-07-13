import json

from Crypto.Hash import SHA256


def calculate_hash(data) -> str:
    if type(data) == str:
        data = bytearray(data, "utf-8")
    h = SHA256.new()
    h.update(data)
    return h.hexdigest()


def convert_transaction_data_to_bytes(transaction_data: dict):
    new_transaction_data = transaction_data.copy()
    new_transaction_data["inputs"] = str(transaction_data["inputs"])
    new_transaction_data["outputs"] = str(transaction_data["outputs"])
    return json.dumps(new_transaction_data, indent=2).encode('utf-8')
