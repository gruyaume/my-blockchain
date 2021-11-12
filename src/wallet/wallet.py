import requests

from common.transaction import Transaction
from common.transaction_input import TransactionInput
from common.transaction_output import TransactionOutput
from common.owner import Owner
from common.node import Node


class Wallet:
    def __init__(self, owner: Owner, node: Node):
        self.owner = owner
        self.node = node

    def process_transaction(self, inputs: [TransactionInput], outputs: [TransactionOutput]) -> requests.Response:
        transaction = Transaction(inputs, outputs)
        transaction.sign(self.owner)
        return self.node.send_transaction({"transaction": transaction.transaction_data})
