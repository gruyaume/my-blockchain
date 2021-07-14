import json

from node.block import Block
from node.script import StackScript


class NodeTransaction:
    def __init__(self, blockchain: Block):
        self.blockchain = blockchain
        self.transaction_data = {}
        self.inputs = ""
        self.outputs = ""

    def receive(self, transaction: dict):
        self.transaction_data = transaction
        self.inputs = transaction["inputs"]
        self.outputs = transaction["outputs"]

    def get_transaction_from_utxo(self, utxo_hash: str) -> dict:
        current_block = self.blockchain
        while current_block:
            if utxo_hash == current_block.transaction_hash:
                return current_block.transaction_data
            current_block = current_block.previous_block

    def get_locking_script_from_utxo(self, utxo_hash: str, utxo_index: int):
        transaction_data = self.get_transaction_from_utxo(utxo_hash)
        return json.loads(transaction_data["outputs"][utxo_index])["locking_script"]

    def execute_script(self, unlocking_script, locking_script):
        unlocking_script_list = unlocking_script.split(" ")
        signature = unlocking_script_list[0]
        public_key = unlocking_script_list[1]
        locking_script_list = locking_script.split(" ")
        receiver_address = locking_script_list[2]

        stack_script = StackScript()
        stack_script.push(signature)
        stack_script.push(public_key)
        stack_script.op_dup()
        stack_script.op_hash_160()
        stack_script.push(receiver_address)
        stack_script.op_equal_verify()
        stack_script.op_check_sig(self.transaction_data)

    def validate(self):
        for tx_input in self.inputs:
            input_dict = json.loads(tx_input)
            locking_script = self.get_locking_script_from_utxo(input_dict["transaction_hash"], input_dict["output_index"])
            self.execute_script(input_dict["unlocking_script"], locking_script)

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

    def validate_funds(self):
        assert self.get_total_amount_in_inputs() == self.get_total_amount_in_outputs()
