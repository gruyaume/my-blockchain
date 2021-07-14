import binascii
import copy
import json

from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15

from common.utils import calculate_hash
from node.block import Block


class NodeTransaction:
    def __init__(self, blockchain: Block):
        self.blockchain = blockchain
        self.transaction_data = {}
        self.signature = ""
        self.inputs = ""
        self.outputs = ""

    def receive(self, transaction: dict):
        self.transaction_data = transaction
        self.inputs = transaction["inputs"]
        self.outputs = transaction["outputs"]

    def validate_signature(self):
        transaction_data = copy.deepcopy(self.transaction_data)
        for count, tx_input in enumerate(transaction_data["inputs"]):
            tx_input_dict = json.loads(tx_input)
            public_key = tx_input_dict.pop("public_key")
            signature = tx_input_dict.pop("signature")
            transaction_data["inputs"][count] = json.dumps(tx_input_dict)
            signature_decoded = binascii.unhexlify(signature.encode("utf-8"))
            public_key_bytes = public_key.encode("utf-8")
            public_key_object = RSA.import_key(binascii.unhexlify(public_key_bytes))
            transaction_bytes = json.dumps(transaction_data, indent=2).encode('utf-8')
            transaction_hash = SHA256.new(transaction_bytes)
            pkcs1_15.new(public_key_object).verify(transaction_hash, signature_decoded)

    def get_transaction_from_utxo(self, utxo_hash: str) -> dict:
        current_block = self.blockchain
        while current_block:
            if utxo_hash == current_block.transaction_hash:
                return current_block.transaction_data
            current_block = current_block.previous_block

    def validate(self):
        self.validate_signature()
        self.validate_funds_are_owned_by_sender()
        self.validate_funds()

    def validate_funds(self):
        assert self.get_total_amount_in_inputs() == self.get_total_amount_in_outputs()

    def get_total_amount_in_inputs(self) -> int:
        total_in = 0
        for tx_input in self.inputs:
            input_dict = json.loads(tx_input)
            transaction_data = self.get_transaction_from_utxo(input_dict["transaction_hash"])
            utxo_amount = json.loads(transaction_data["outputs"][input_dict["output_index"]])["amount"]
            total_in = total_in + utxo_amount
        return total_in

    def get_total_amount_in_outputs(self) -> int:
        total_out = 0
        for tx_output in self.outputs:
            output_dict = json.loads(tx_output)
            amount = output_dict["amount"]
            total_out = total_out + amount
        return total_out

    def validate_funds_are_owned_by_sender(self):
        for tx_input in self.inputs:
            input_dict = json.loads(tx_input)
            public_key = input_dict["public_key"]
            sender_public_key_hash = calculate_hash(calculate_hash(public_key, hash_function="sha256"), hash_function="ripemd160")
            transaction_data = self.get_transaction_from_utxo(input_dict["transaction_hash"])
            public_key_hash = json.loads(transaction_data["outputs"][input_dict["output_index"]])["public_key_hash"]
            assert public_key_hash == sender_public_key_hash
