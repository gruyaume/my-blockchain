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
