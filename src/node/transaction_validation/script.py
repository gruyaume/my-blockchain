import binascii
import json

from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15

from common.utils import calculate_hash


class Stack:
    def __init__(self):
        self.elements = []

    def push(self, element):
        self.elements.append(element)

    def pop(self):
        return self.elements.pop()


class StackScript(Stack):
    def __init__(self, transaction_data: dict):
        super().__init__()
        for count, tx_input in enumerate(transaction_data["inputs"]):
            tx_input_dict = json.loads(tx_input)
            tx_input_dict.pop("unlocking_script")
            transaction_data["inputs"][count] = json.dumps(tx_input_dict)
        self.transaction_data = transaction_data

    def op_dup(self):
        last_element = self.pop()
        self.push(last_element)
        self.push(last_element)

    def op_hash160(self):
        last_element = self.pop()
        self.push(calculate_hash(calculate_hash(last_element, hash_function="sha256"), hash_function="ripemd160"))

    def op_equal_verify(self):
        last_element_1 = self.pop()
        last_element_2 = self.pop()
        assert last_element_1 == last_element_2

    def op_checksig(self):
        public_key = self.pop()
        signature = self.pop()
        signature_decoded = binascii.unhexlify(signature.encode("utf-8"))
        public_key_bytes = public_key.encode("utf-8")
        public_key_object = RSA.import_key(binascii.unhexlify(public_key_bytes))
        transaction_bytes = json.dumps(self.transaction_data, indent=2).encode('utf-8')
        transaction_hash = SHA256.new(transaction_bytes)
        pkcs1_15.new(public_key_object).verify(transaction_hash, signature_decoded)
