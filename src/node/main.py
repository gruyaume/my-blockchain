import logging
import os

from flask import Flask, request, jsonify

from common.io_blockchain import BlockchainMemory
from common.io_known_nodes import KnownNodesMemory
from common.network import Network
from common.node import Node
from node.new_block_validation.new_block_validation import NewBlock, NewBlockException
from node.transaction_validation.transaction_validation import Transaction, TransactionException
from common.io_mem_pool import MemPool

logging.basicConfig(level=logging.DEBUG, format=f'%(asctime)s: %(message)s')

app = Flask(__name__)


MY_HOSTNAME = os.environ['MY_HOSTNAME']
MEMPOOL_DIR = os.environ["MEMPOOL_DIR"]
KNOWN_NODES_DIR = os.environ["KNOWN_NODES_DIR"]
BLOCKCHAIN_DIR = os.environ["BLOCKCHAIN_DIR"]
mempool = MemPool()
blockchain_memory = BlockchainMemory()
my_node = Node(MY_HOSTNAME)
network = Network(my_node)
network.join_network()


@app.route("/block", methods=['POST'])
def validate_block():
    content = request.json
    blockchain_base = blockchain_memory.get_blockchain_from_memory()
    try:
        block = NewBlock(blockchain_base, MY_HOSTNAME)
        block.receive(new_block=content["block"], sender=content["sender"])
        block.validate()
        block.add()
        block.clear_block_transactions_from_mempool()
        block.broadcast()
    except (NewBlockException, TransactionException) as new_block_exception:
        return f'{new_block_exception}', 400
    return "Transaction success", 200


@app.route("/transactions", methods=['POST'])
def validate_transaction():
    logging.info("New transaction validation request")
    content = request.json
    logging.info(f"Transaction: {content['transaction']}")
    blockchain_base = blockchain_memory.get_blockchain_from_memory()
    try:
        transaction = Transaction(blockchain_base, MY_HOSTNAME)
        transaction.receive(transaction=content["transaction"])
        if transaction.is_new:
            logging.info("Transaction is new")
            transaction.validate()
            transaction.validate_funds()
            transaction.store()
            transaction.broadcast()
    except TransactionException as transaction_exception:
        return f'{transaction_exception}', 400
    return "Transaction success", 200


@app.route("/block", methods=['GET'])
def get_blocks():
    logging.info("Block request")
    blockchain_base = blockchain_memory.get_blockchain_from_memory()
    return jsonify(blockchain_base.to_dict)


@app.route("/utxo/<user>", methods=['GET'])
def get_user_utxos(user):
    logging.info("User utxo request")
    blockchain_base = blockchain_memory.get_blockchain_from_memory()
    return jsonify(blockchain_base.get_user_utxos(user))


@app.route("/transactions/<transaction_hash>", methods=['GET'])
def get_transaction(transaction_hash):
    logging.info("Transaction request")
    blockchain_base = blockchain_memory.get_blockchain_from_memory()
    return jsonify(blockchain_base.get_transaction(transaction_hash))


@app.route("/new_node_advertisement", methods=['POST'])
def new_node_advertisement():
    logging.info("New node advertisement request")
    content = request.json
    hostname = content["hostname"]
    known_nodes_memory = KnownNodesMemory()
    try:
        new_node = Node(hostname)
        known_nodes_memory.store_new_node(new_node)
    except TransactionException as transaction_exception:
        return f'{transaction_exception}', 400
    return "New node advertisement success", 200


@app.route("/known_node_request", methods=['GET'])
def known_node_request():
    logging.info("Known node request")
    return jsonify(network.return_known_nodes())


@app.route("/restart", methods=['POST'])
def restart():
    logging.info("Node restart request")
    my_node = Node(MY_HOSTNAME)
    network = Network(my_node)
    mempool = MemPool()
    mempool.clear_transactions_from_memory()
    network.join_network()
    return "Restart success", 200


def main():
    global network
    my_node = Node(MY_HOSTNAME)
    network = Network(my_node)
    network.join_network()
    app.run()


if __name__ == "__main__":
    main()
