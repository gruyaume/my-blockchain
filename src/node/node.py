import binascii
import json

from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15

from node.block import Block
from transaction.transaction_input import TransactionInput
from transaction.transaction_output import TransactionOutput


class NodeTransaction:
    def __init__(self, blockchain: Block):
        self.blockchain = blockchain
        self.transaction_data = ""
        self.signature = ""
        self.inputs = ""
        self.outputs = ""

    def receive(self, transaction: dict):
        self.inputs = transaction["inputs"]
        self.outputs = transaction["outputs"]

    def validate_signature(self):
        for tx_input in self.inputs:
            tx_input_dict = json.loads(tx_input)
            tx_input_object = TransactionInput(transaction_hash=tx_input_dict["transaction_hash"],
                                               output_index=tx_input_dict["output_index"],
                                               public_key=tx_input_dict["public_key"],
                                               signature=tx_input_dict["signature"])
            public_key_object = RSA.import_key(tx_input_object.public_key)
            transaction_data = {
                "transaction_hash": tx_input_object.transaction_hash,
                "output_index": str(tx_input_object.output_index)
            }
            transaction_bytes = json.dumps(transaction_data, indent=2).encode('utf-8')
            transaction_hash = SHA256.new(transaction_bytes)
            signature_bytes = binascii.unhexlify(tx_input_object.signature)
            pkcs1_15.new(public_key_object).verify(transaction_hash, signature_bytes)

    def validate_funds(self, amount: int, utxos: [TransactionOutput]) -> bool:
        current_block = self.blockchain
        total = 0
        while current_block:
            if not utxos:
                break
            for count, utxo in enumerate(utxos):
                if utxo.transaction_hash == current_block.transaction_data["hash"]:
                    total = total + current_block.transaction_data["outputs"][utxo.output_index][1]
                    utxos.remove(utxo)
            current_block = current_block.previous_block
        if total >= amount:
            return True
        else:
            return False
