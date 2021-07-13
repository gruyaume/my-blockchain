from Crypto.Hash import SHA256


def calculate_hash(data: bytes) -> str:
    h = SHA256.new()
    h.update(data)
    return h.hexdigest()
