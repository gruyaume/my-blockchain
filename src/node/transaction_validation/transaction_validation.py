import copy
import logging

import requests

from common.block import Block
from common.io_mem_pool import MemPool
from node.transaction_validation.script import StackScript
from common.io_known_nodes import KnownNodesMemory


class TransactionException(Exception):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message


class Transaction:
    def __init__(self, blockchain: Block, hostname: str):
        self.blockchain = blockchain
        self.transaction_data = {}
        self.inputs = []
        self.outputs = []
        self.is_valid = False
        self.is_funds_sufficient = False
        self.mempool = MemPool()
        self.known_node_memory = KnownNodesMemory()
        self.sender = ""
        self.hostname = hostname

    def receive(self, transaction: dict):
        self.transaction_data = transaction
        self.inputs = transaction["inputs"]
        self.outputs = transaction["outputs"]

    @property
    def is_new(self):
        current_transactions = self.mempool.get_transactions_from_memory()
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
        logging.info("Validating inputs")
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
                logging.info('Transaction script validation failed')
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
        logging.info("Validating funds")
        inputs_total = self.get_total_amount_in_inputs()
        outputs_total = self.get_total_amount_in_outputs()
        try:
            assert inputs_total == outputs_total
            self.is_funds_sufficient = True
            logging.info("Funds are sufficient")
        except AssertionError:
            logging.info('Transaction inputs and outputs did not match')
            raise TransactionException(f"inputs ({inputs_total}), outputs ({outputs_total})",
                                       "Transaction inputs and outputs did not match")

    def broadcast(self):
        logging.info("Broadcasting to all nodes")
        node_list = self.known_node_memory.known_nodes
        for node in node_list:
            if node.hostname != self.hostname and node.hostname != self.sender:
                try:
                    logging.info(f"Broadcasting to {node.hostname}")
                    node.send_transaction({"transaction": self.transaction_data})
                except requests.ConnectionError:
                    logging.info(f"Failed broadcasting to {node.hostname}")

    def store(self):
        if self.is_valid and self.is_funds_sufficient:
            logging.info("Storing transaction data in memory")
            logging.info(f"Transaction data: {self.transaction_data}")
            current_transactions = self.mempool.get_transactions_from_memory()
            current_transactions.append(self.transaction_data)
            self.mempool.store_transactions_in_memory(current_transactions)
