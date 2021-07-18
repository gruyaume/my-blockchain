from flask import Flask, request

from node.node import NodeTransaction, TransactionException
from initialize_blockchain import blockchain

app = Flask(__name__)

blockchain_base = blockchain()


@app.route("/transactions", methods=['POST'])
def validate_transaction():
    content = request.json
    try:
        node = NodeTransaction(blockchain_base)
        node.receive(transaction=content["transaction"])
        node.validate()
        node.validate_funds()
        node.broadcast()
    except TransactionException as transaction_exception:
        return f'{transaction_exception}', 400
    return "Transaction success", 200
