from flask import Flask, request

from common.initialize_blockchain import blockchain
from transaction_validation.transaction import Transaction, TransactionException

app = Flask(__name__)

blockchain_base = blockchain()


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
