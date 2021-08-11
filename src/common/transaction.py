import binascii
import json

from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15

from common.transaction_input import TransactionInput
from common.transaction_output import TransactionOutput
from common.utils import calculate_hash


class Transaction:
    def __init__(self, inputs: [TransactionInput], outputs: [TransactionOutput]):
        self.inputs = inputs
        self.outputs = outputs
        self.transaction_hash = self.get_transaction_hash()

    def get_transaction_hash(self) -> str:
        transaction_data = {
            "inputs": [i.to_dict() for i in self.inputs],
            "outputs": [i.to_dict() for i in self.outputs]
        }
        transaction_bytes = json.dumps(transaction_data, indent=2)
        return calculate_hash(transaction_bytes)

    def sign_transaction_data(self, owner):
        transaction_dict = {"inputs": [tx_input.to_dict(with_unlocking_script=False) for tx_input in self.inputs],
                            "outputs": [tx_output.to_dict() for tx_output in self.outputs]}
        transaction_bytes = json.dumps(transaction_dict, indent=2).encode('utf-8')
        hash_object = SHA256.new(transaction_bytes)
        signature = pkcs1_15.new(owner.private_key).sign(hash_object)
        return signature

    def sign(self, owner):
        signature_hex = binascii.hexlify(self.sign_transaction_data(owner)).decode("utf-8")
        for transaction_input in self.inputs:
            transaction_input.unlocking_script = f"{signature_hex} {owner.public_key_hex}"

    @property
    def transaction_data(self) -> dict:
        transaction_data = {
            "inputs": [i.to_dict() for i in self.inputs],
            "outputs": [i.to_dict() for i in self.outputs],
            "transaction_hash": self.transaction_hash
        }
        return transaction_data
