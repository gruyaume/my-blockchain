import requests

from common.transaction import Transaction
from common.transaction_input import TransactionInput
from common.transaction_output import TransactionOutput
from common.owner import Owner


class Node:
    def __init__(self):
        ip = "127.0.0.1"
        port = 5000
        self.base_url = f"http://{ip}:{port}/"

    def send(self, transaction_data: dict) -> requests.Response:
        url = f"{self.base_url}transactions"
        req_return = requests.post(url, json=transaction_data)
        req_return.raise_for_status()
        return req_return


class Wallet:
    def __init__(self, owner: Owner):
        self.owner = owner
        self.node = Node()

    def process_transaction(self, inputs: [TransactionInput], outputs: [TransactionOutput]) -> requests.Response:
        transaction = Transaction(inputs, outputs)
        transaction.sign(self.owner)
        return self.node.send({"transaction": transaction.transaction_data})
