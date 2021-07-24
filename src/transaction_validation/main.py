from multiprocessing import shared_memory

from flask import Flask, request

from common.initialize_blockchain import blockchain
from transaction_validation.transaction import Transaction, TransactionException
import json
app = Flask(__name__)


@app.route("/transactions", methods=['POST'])
def validate_transaction():
    content = request.json
    try:
        node = Transaction(blockchain_base)
        node.receive(transaction=content["transaction"])
        node.validate()
        node.validate_funds()
        node.broadcast()
        node.store()
    except TransactionException as transaction_exception:
        return f'{transaction_exception}', 400
    return "Transaction success", 200


def create_mem_pool():
    transactions = [{"a": "b"}, {"c": "d"}, {"e": "f"}, {"g": "h"}]
    transactions_str = []
    for transaction in transactions:
        transactions_str.append(json.dumps(transaction, indent=2))
    a = shared_memory.ShareableList(transactions_str, name="mem_pool")
    a.shm.close()
    # a = shared_memory.ShareableList(name="mem_pool")
    # a.shm.close()

blockchain_base = blockchain()
create_mem_pool()
