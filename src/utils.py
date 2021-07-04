import hashlib


def calculate_hash(string_data: str) -> str:
    bytes_data = bytearray(string_data, "utf-8")
    return hashlib.sha256(bytes_data).hexdigest()
