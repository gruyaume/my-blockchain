from Crypto.Hash import SHA256


def calculate_hash(data) -> str:
    if type(data) == str:
        data = bytearray(data, "utf-8")
    h = SHA256.new()
    h.update(data)
    return h.hexdigest()
