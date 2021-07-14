import binascii
import json

from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15

from common.transaction_input import TransactionInput
from common.transaction_output import TransactionOutput
from common.utils import calculate_hash


class Owner:
    def __init__(self, private_key: RSA.RsaKey, public_key_hash: str, public_key_hex: str):
        self.private_key = private_key
        self.public_key_hash = public_key_hash
        self.public_key_hex = public_key_hex


def initialize_wallet():
    private_key = RSA.generate(2048)
    public_key = private_key.publickey().export_key("DER")
    public_key_hex = binascii.hexlify(public_key).decode("utf-8")
    public_key_hash = calculate_hash(calculate_hash(public_key_hex, hash_function="sha256"), hash_function="ripemd160")
    return Owner(private_key=private_key, public_key_hash=public_key_hash, public_key_hex=public_key_hex)


class Transaction:
    def __init__(self, owner: Owner, inputs: [TransactionInput], outputs: [TransactionOutput]):
        self.owner = owner
        self.inputs = inputs
        self.outputs = outputs

    def sign_transaction_data(self):
        transaction_dict = {
            "inputs": [tx_input.to_json(with_signature_and_public_key=False) for tx_input in self.inputs],
            "outputs": [tx_output.to_json() for tx_output in self.outputs]
        }
        transaction_bytes = json.dumps(transaction_dict, indent=2).encode('utf-8')
        hash_object = SHA256.new(transaction_bytes)
        signature = pkcs1_15.new(self.owner.private_key).sign(hash_object)
        return signature

    def sign(self):
        signature_hex = binascii.hexlify(self.sign_transaction_data()).decode("utf-8")
        for transaction_input in self.inputs:
            transaction_input.signature = signature_hex
            transaction_input.public_key = self.owner.public_key_hex

    def send_to_nodes(self):
        return {
            "inputs": [i.to_json() for i in self.inputs],
            "outputs": [i.to_json() for i in self.outputs]
        }
