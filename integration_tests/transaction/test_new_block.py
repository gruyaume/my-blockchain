import pytest
import requests

from blockchain_users.camille import private_key as camille_private_key
from common.io_blockchain import get_blockchain_from_memory
from common.io_mem_pool import store_transactions_in_memory
from common.transaction_input import TransactionInput
from common.transaction_output import TransactionOutput
from integration_tests.common.flask import Server
from node.new_block_creation.new_block_creation import ProofOfWork
from wallet.wallet import Owner, Wallet, Transaction
from common.network import Network
from common.node import Node


@pytest.fixture(scope="module")
def camille():
    return Owner(private_key=camille_private_key)


@pytest.fixture(scope="module")
def camille_wallet(camille):
    return Wallet(camille)


@pytest.fixture(scope="module")
def create_good_transactions(camille):
    utxo_0 = TransactionInput(transaction_hash="e10154f49ae1119777b93e5bcd1a1506b6a89c1f82cc85f63c6cbe83a39df5dc",
                              output_index=0)
    output_0 = TransactionOutput(public_key_hash=b"a037a093f0304f159fe1e49cfcfff769eaac7cda", amount=5)
    transaction_1 = Transaction(inputs=[utxo_0], outputs=[output_0])
    transaction_1.sign(camille)
    transactions = [transaction_1]
    transactions_str = [transaction.transaction_data for transaction in transactions]
    store_transactions_in_memory(transactions_str)


@pytest.fixture(scope="module")
def create_bad_transactions(camille):
    utxo_0 = TransactionInput(transaction_hash="5669d7971b76850a4d725c75fbbc20ea97bd1382e2cfae43c41e121ca399b660",
                              output_index=0)
    output_0 = TransactionOutput(public_key_hash=b"a037a093f0304f159fe1e49cfcfff769eaac7cda", amount=25)
    transaction_1 = Transaction(inputs=[utxo_0], outputs=[output_0])
    transaction_1.sign(camille)
    transactions = [transaction_1]
    transactions_str = [transaction.transaction_data for transaction in transactions]
    store_transactions_in_memory(transactions_str)


@pytest.fixture(scope="module")
def server() -> Server:
    server = Server()
    return server


@pytest.fixture(scope="module")
def network() -> Network:
    node = Node(hostname="1.1.1.1:1234")
    network = Network(node)
    return network


def test_given_good_transactions_in_mem_pool_when_new_block_is_created_then_new_block_is_accepted(
        create_good_transactions, server, network):
    server.start()
    pow = ProofOfWork(network)
    pow.create_new_block()
    pow.broadcast()
    server.stop()


def test_given_good_transactions_in_mem_pool_when_new_block_is_created_then_new_block_is_added_to_current_blockchain(
        create_good_transactions, server, network):
    server.start()
    initial_blockchain = get_blockchain_from_memory()
    pow = ProofOfWork(network)
    pow.create_new_block()
    pow.broadcast()
    new_block = get_blockchain_from_memory()
    server.stop()
    assert len(new_block) == len(initial_blockchain) + 1
    assert new_block.block_header.hash == pow.new_block.block_header.hash


def test_given_good_transactions_in_mem_pool_when_new_block_is_created_then_new_block_contains_new_transactions_and_coinbase(
        create_good_transactions, server, network):
    server.start()
    pow = ProofOfWork(network)
    pow.create_new_block()
    pow.broadcast()
    new_block = get_blockchain_from_memory()
    server.stop()
    assert len(new_block.transactions) == 2
    assert new_block.transactions[0]["outputs"] == [
        {
            'amount': 5,
            'locking_script': "OP_DUP OP_HASH160 b'a037a093f0304f159fe1e49cfcfff769eaac7cda' OP_EQUAL_VERIFY OP_CHECKSIG"
        }
    ]
    assert new_block.transactions[1]["outputs"] == [
        {
            'amount': 6.25,
            'locking_script': 'OP_DUP OP_HASH160 4d9715dc8f9578ca2af159409be9c559c5eaceba OP_EQUAL_VERIFY OP_CHECKSIG'
         }
    ]


def test_given_bad_transactions_in_mem_pool_when_new_block_is_created_then_new_block_is_refused(
        create_bad_transactions, server, network):
    server.start()
    pow = ProofOfWork(network)
    pow.create_new_block()
    with pytest.raises(requests.exceptions.HTTPError) as error:
        pow.broadcast()
    assert 'Could not find locking script for utxo' in error.value.response.text
    server.stop()
