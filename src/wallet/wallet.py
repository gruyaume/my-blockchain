import json

import base58
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15

from wallet.utils import calculate_hash
from transaction.transaction_input import TransactionInput
from transaction.transaction_output import TransactionOutput


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
    def __init__(self, owner: Owner, inputs: [TransactionInput], outputs: [TransactionOutput]):
        self.owner = owner
        self.inputs = inputs
        self.outputs = outputs

    def sign_transaction_data(self, transaction_input: TransactionInput):
        transaction_dict = {
            "transaction_hash": str(transaction_input.transaction_hash),
            "output_index": str(transaction_input.output_index)
        }
        transaction_bytes = json.dumps(transaction_dict, indent=2).encode('utf-8')
        hash_object = SHA256.new(transaction_bytes)
        signature = pkcs1_15.new(self.owner.private_key).sign(hash_object)
        return signature

    def sign(self):
        for transaction_input in self.inputs:
            transaction_input.signature = self.sign_transaction_data(transaction_input)
            transaction_input.public_key = self.owner.public_key

    def send_to_nodes(self):
        return {
            "inputs": [i.to_json() for i in self.inputs],
            "outputs": [i.to_json() for i in self.outputs]
        }
