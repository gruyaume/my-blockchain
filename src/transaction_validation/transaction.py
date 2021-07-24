import json

import requests

from common.block import Block
from transaction_validation.script import StackScript
from multiprocessing import shared_memory


class TransactionException(Exception):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message


class OtherNode:
    def __init__(self, ip: str, port: int):
        self.base_url = f"http://{ip}:{port}/"

    def send(self, transaction_data: dict) -> requests.Response:
        url = f"{self.base_url}transactions"
        req_return = requests.post(url, json=transaction_data)
        req_return.raise_for_status()
        return req_return


class Transaction:
    def __init__(self, blockchain: Block):
        self.blockchain = blockchain
        self.transaction_data = {}
        self.inputs = ""
        self.outputs = ""
        self.is_valid = False
        self.is_funds_sufficient = False

    def receive(self, transaction: dict):
        self.transaction_data = transaction
        self.inputs = transaction["inputs"]
        self.outputs = transaction["outputs"]

    def get_transaction_from_utxo(self, utxo_hash: str) -> dict:
        current_block = self.blockchain
        while current_block:
            for transaction in current_block.transactions:
                if utxo_hash == transaction["transaction_hash"]:
                    return transaction
            current_block = current_block.previous_block

    def get_locking_script_from_utxo(self, utxo_hash: str, utxo_index: int):
        transaction_data = self.get_transaction_from_utxo(utxo_hash)
        if transaction_data:
            return json.loads(transaction_data["outputs"][utxo_index])["locking_script"]
        else:
            raise TransactionException(f"{utxo_hash}:{utxo_index}", "UTXO hash/output index combination not valid")

    def execute_script(self, unlocking_script, locking_script):
        unlocking_script_list = unlocking_script.split(" ")
        locking_script_list = locking_script.split(" ")
        stack_script = StackScript(self.transaction_data)
        for element in unlocking_script_list:
            if element.startswith("OP"):
                class_method = getattr(StackScript, element.lower())
                class_method(stack_script)
            else:
                stack_script.push(element)
        for element in locking_script_list:
            if element.startswith("OP"):
                class_method = getattr(StackScript, element.lower())
                class_method(stack_script)
            else:
                stack_script.push(element)

    def validate(self):
        for tx_input in self.inputs:
            input_dict = json.loads(tx_input)
            transaction_hash = input_dict["transaction_hash"]
            output_index = input_dict["output_index"]
            locking_script = self.get_locking_script_from_utxo(transaction_hash, output_index)
            try:
                self.execute_script(input_dict["unlocking_script"], locking_script)
                self.is_valid = True
            except Exception:
                raise TransactionException(f"UTXO ({transaction_hash}:{output_index})", "Transaction script validation failed")

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
        inputs_total = self.get_total_amount_in_inputs()
        outputs_total = self.get_total_amount_in_outputs()
        try:
            assert inputs_total == outputs_total
            self.is_funds_sufficient = True
        except AssertionError:
            raise TransactionException(f"inputs ({inputs_total}), outputs ({outputs_total})",
                                       "Transaction inputs and outputs did not match")

    def broadcast(self):
        node_list = [OtherNode("127.0.0.1", 5001), OtherNode("127.0.0.1", 5002)]
        for node in node_list:
            try:
                node.send(self.transaction_data)
            except requests.ConnectionError:
                pass

    def store(self):
        if self.is_valid and self.is_funds_sufficient:
            try:
                current_mem_pool = shared_memory.ShareableList(name="mem_pool")
                mem_pool_list = [x for x in current_mem_pool]
                current_mem_pool.shm.close()
                current_mem_pool.shm.unlink()
            except FileNotFoundError:
                mem_pool_list = []
            mem_pool_list.append(json.dumps(self.transaction_data, indent=2))
            a = shared_memory.ShareableList(mem_pool_list, name="mem_pool")
            a.shm.close()
