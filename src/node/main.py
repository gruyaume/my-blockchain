from flask import Flask, request, jsonify

from common.io_blockchain import get_blockchain_from_memory
from common.network import Network
from common.node import Node
from node.new_block_validation.new_block_validation import NewBlock, NewBlockException
from node.transaction_validation.transaction_validation import Transaction, TransactionException

app = Flask(__name__)

MY_HOSTNAME = "127.0.0.1:5000"
my_node = Node(MY_HOSTNAME)
network = Network(my_node)
network.join_network()


@app.route("/block", methods=['POST'])
def validate_block():
    content = request.json
    blockchain_base = get_blockchain_from_memory()
    try:
        block = NewBlock(blockchain_base, network)
        block.receive(new_block=content["block"])
        block.validate()
        block.add()
        block.broadcast()
    except (NewBlockException, TransactionException) as new_block_exception:
        return f'{new_block_exception}', 400
    return "Transaction success", 200


@app.route("/transactions", methods=['POST'])
def validate_transaction():
    content = request.json
    blockchain_base = get_blockchain_from_memory()
    try:
        transaction = Transaction(blockchain_base, network)
        transaction.receive(transaction=content["transaction"])
        if transaction.is_new:
            transaction.validate()
            transaction.validate_funds()
            transaction.broadcast()
            transaction.store()
    except TransactionException as transaction_exception:
        return f'{transaction_exception}', 400
    return "Transaction success", 200


@app.route("/block", methods=['GET'])
def get_blocks():
    blockchain_base = get_blockchain_from_memory()
    return jsonify(blockchain_base.to_dict)


@app.route("/utxo/<user>", methods=['GET'])
def get_user_utxos(user):
    blockchain_base = get_blockchain_from_memory()
    return jsonify(blockchain_base.get_user_utxos(user))


@app.route("/transactions/<transaction_hash>", methods=['GET'])
def get_transaction(transaction_hash):
    blockchain_base = get_blockchain_from_memory()
    return jsonify(blockchain_base.get_transaction(transaction_hash))


@app.route("/new_node_advertisement", methods=['POST'])
def new_node_advertisement():
    content = request.json
    hostname = content["hostname"]
    try:
        new_node = Node(hostname)
        network.store_new_node(new_node)
    except TransactionException as transaction_exception:
        return f'{transaction_exception}', 400
    return "New node advertisement success", 200


@app.route("/known_node_request", methods=['GET'])
def known_node_request():
    return jsonify(network.return_known_nodes())


def main():
    global network
    my_node = Node(MY_HOSTNAME)
    network = Network(my_node)
    network.join_network()
    app.run()


if __name__ == "__main__":
    main()
