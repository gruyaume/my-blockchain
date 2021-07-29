import json
from multiprocessing import shared_memory

import requests

from common.block import Block
from common.node import Node
from node.transaction_validation.script import StackScript


class TransactionException(Exception):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message


class OtherNode(Node):
    def __init__(self, ip: str, port: int):
        super().__init__(ip, port)

    def send_transaction(self, transaction_data: dict) -> requests.Response:
        return self.post("transactions", transaction_data)


class Transaction:
    def __init__(self, blockchain: Block):
        self.blockchain = blockchain
        self.transaction_data = {}
        self.inputs = []
        self.outputs = []
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
            try:
                return transaction_data["outputs"][utxo_index]["locking_script"]
            except IndexError:
                print('UTXO hash/output index combination not valid')
                raise TransactionException(f"{utxo_hash}:{utxo_index}", "UTXO hash/output index combination not valid")
        else:
            print('No transaction with UTXO hash exists')
            raise TransactionException(f"{utxo_hash}:{utxo_index}", "No transaction with UTXO hash exists")

    def execute_script(self, unlocking_script, locking_script):
        unlocking_script_list = unlocking_script.split(" ")
        locking_script_list = locking_script.split(" ")
        if "transaction_hash" in self.transaction_data:
            self.transaction_data.pop("transaction_hash")
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
            transaction_hash = tx_input["transaction_hash"]
            output_index = tx_input["output_index"]
            locking_script = self.get_locking_script_from_utxo(transaction_hash, output_index)
            try:
                self.execute_script(tx_input["unlocking_script"], locking_script)
                self.is_valid = True
            except Exception:
                print('Transaction script validation failed')
                raise TransactionException(f"UTXO ({transaction_hash}:{output_index})", "Transaction script validation failed")

    def get_total_amount_in_inputs(self) -> int:
        total_in = 0
        for tx_input in self.inputs:
            transaction_data = self.get_transaction_from_utxo(tx_input["transaction_hash"])
            utxo_amount = transaction_data["outputs"][tx_input["output_index"]]["amount"]
            total_in = total_in + utxo_amount
        return total_in

    def get_total_amount_in_outputs(self) -> int:
        total_out = 0
        for tx_output in self.outputs:
            amount = tx_output["amount"]
            total_out = total_out + amount
        return total_out

    def validate_funds(self):
        inputs_total = self.get_total_amount_in_inputs()
        outputs_total = self.get_total_amount_in_outputs()
        try:
            assert inputs_total == outputs_total
            self.is_funds_sufficient = True
        except AssertionError:
            print('Transaction inputs and outputs did not match')
            raise TransactionException(f"inputs ({inputs_total}), outputs ({outputs_total})",
                                       "Transaction inputs and outputs did not match")

    def broadcast(self):
        node_list = [OtherNode("127.0.0.1", 5001), OtherNode("127.0.0.1", 5002)]
        for node in node_list:
            try:
                node.send_transaction(self.transaction_data)
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
            sharable_list = shared_memory.ShareableList(mem_pool_list, name="mem_pool")
            sharable_list.shm.close()
