
import binascii
import json

import base58
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15

from utils import calculate_hash, generate_transaction_data, convert_transaction_data_to_bytes


class Owner:
    def __init__(self, private_key: RSA.RsaKey, public_key: bytes, bitcoin_address: bytes):
        self.private_key = private_key
        self.public_key = public_key
        self.bitcoin_address = bitcoin_address


def initialize_wallet():
    private_key = RSA.generate(2048)
    public_key = private_key.publickey().export_key()
    hash_1 = calculate_hash(public_key, hash_function="sha256")
    hash_2 = calculate_hash(hash_1, hash_function="ripemd160")
    bitcoin_address = base58.b58encode(hash_2)
    return Owner(private_key, public_key, bitcoin_address)


class Transaction:
    def __init__(self, owner: Owner, receiver_bitcoin_address: bytes, amount: int):
        self.owner = owner
        self.receiver_bitcoin_address = receiver_bitcoin_address
        self.amount = amount

    def generate_data(self) -> bytes:
        transaction_data = generate_transaction_data(self.owner.bitcoin_address, self.receiver_bitcoin_address, self.amount)
        return convert_transaction_data_to_bytes(transaction_data)

    @staticmethod
    def create_file(transaction_data: bytes, signature: bytes) -> str:
        file_name = calculate_hash(signature)
        file_content = {
            "transaction_data": transaction_data.decode("utf-8"),
            "signature": binascii.hexlify(signature).decode("utf-8")
        }
        f = open(file_name, "x")
        json.dump(file_content, f)
        f.close()
        return file_name

    def sign(self) -> str:
        transaction_data = self.generate_data()
        hash_object = SHA256.new(transaction_data)
        signature = pkcs1_15.new(self.owner.private_key).sign(hash_object)
        return self.create_file(transaction_data, signature)

    def send_to_nodes(self, transaction_file: str):
        pass
