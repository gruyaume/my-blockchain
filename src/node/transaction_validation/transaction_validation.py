import copy

import requests

from common.block import Block
from common.io_mem_pool import get_transactions_from_memory, store_transactions_in_memory
from common.network import Network
from node.transaction_validation.script import StackScript


class TransactionException(Exception):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message


class Transaction:
    def __init__(self, blockchain: Block, network: Network):
        self.blockchain = blockchain
        self.network = network
        self.transaction_data = {}
        self.inputs = []
        self.outputs = []
        self.is_valid = False
        self.is_funds_sufficient = False

    def receive(self, transaction: dict):
        self.transaction_data = transaction
        self.inputs = transaction["inputs"]
        self.outputs = transaction["outputs"]

    @property
    def is_new(self):
        current_transactions = get_transactions_from_memory()
        if self.transaction_data in current_transactions:
            return False
        return True

    def execute_script(self, unlocking_script, locking_script):
        unlocking_script_list = unlocking_script.split(" ")
        locking_script_list = locking_script.split(" ")
        transaction_data = copy.deepcopy(self.transaction_data)
        if "transaction_hash" in transaction_data:
            transaction_data.pop("transaction_hash")
        stack_script = StackScript(transaction_data)
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
            try:
                locking_script = self.blockchain.get_locking_script_from_utxo(transaction_hash, output_index)
            except Exception:
                raise TransactionException(f"{transaction_hash}:{output_index}", "Could not find locking script for utxo")
            try:
                self.execute_script(tx_input["unlocking_script"], locking_script)
                self.is_valid = True
            except Exception:
                print('Transaction script validation failed')
                raise TransactionException(f"UTXO ({transaction_hash}:{output_index})", "Transaction script validation failed")

    def get_total_amount_in_inputs(self) -> int:
        total_in = 0
        for tx_input in self.inputs:
            transaction_data = self.blockchain.get_transaction_from_utxo(tx_input["transaction_hash"])
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
        node_list = self.network.known_nodes
        for node in node_list:
            if node.hostname != self.network.node.hostname:
                try:
                    node.send_transaction(self.transaction_data)
                except requests.ConnectionError:
                    pass

    def store(self):
        if self.is_valid and self.is_funds_sufficient:
            current_transactions = get_transactions_from_memory()
            current_transactions.append(self.transaction_data)
            store_transactions_in_memory(current_transactions)
