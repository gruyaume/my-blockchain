import time

import pytest
import requests

from blockchain_users.camille import private_key as camille_private_key
from common.block import BlockHeader
from common.io_mem_pool import store_transactions_in_memory
from common.network import Network
from common.node import Node
from common.transaction_input import TransactionInput
from common.transaction_output import TransactionOutput
from integration_tests.common.blockchain_network import DefaultBlockchainNetwork, NODE00_HOSTNAME, \
    NODE01_HOSTNAME, NODE02_HOSTNAME
from node.new_block_creation.new_block_creation import ProofOfWork
from wallet.wallet import Owner, Wallet, Transaction


@pytest.fixture(scope="module")
def camille():
    return Owner(private_key=camille_private_key)


@pytest.fixture(scope="module")
def node00():
    return Node(NODE00_HOSTNAME)


@pytest.fixture(scope="module")
def node01():
    return Node(NODE01_HOSTNAME)


@pytest.fixture(scope="module")
def node02():
    return Node(NODE02_HOSTNAME)



@pytest.fixture(scope="module")
def blockchain_network():
    return DefaultBlockchainNetwork()


@pytest.fixture(scope="module")
def camille_wallet(camille, default_node):
    return Wallet(camille, default_node)


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
def network() -> Network:
    node = Node(hostname="1.1.1.1:1234")
    network = Network(node)
    return network


def test_given_good_transactions_in_mem_pool_when_new_block_is_created_then_new_block_is_accepted(
        create_good_transactions, blockchain_network, network):
    blockchain_network.restart()
    time.sleep(3)
    pow = ProofOfWork(network)
    pow.create_new_block()
    pow.broadcast()


def test_given_good_transactions_in_mem_pool_when_new_block_is_created_then_a_new_block_is_added_to_current_blockchain(
        create_good_transactions, blockchain_network, node00, network):
    blockchain_network.restart()
    time.sleep(3)
    node00_initial_blockchain = node00.get_blockchain()
    pow = ProofOfWork(network)
    pow.create_new_block()
    pow.broadcast()
    node00_new_blockchain = node00.get_blockchain()
    assert len(node00_new_blockchain) == len(node00_initial_blockchain) + 1


def test_given_good_transactions_in_mem_pool_when_new_block_is_created_then_new_block_contains_correct_data(
        create_good_transactions, blockchain_network, node00, network):
    blockchain_network.restart()
    time.sleep(3)
    pow = ProofOfWork(network)
    pow.create_new_block()
    pow.broadcast()
    node00_new_blockchain = node00.get_blockchain()
    node00_new_block_header = node00_new_blockchain[0]["header"]
    node00_new_block_header_obj = BlockHeader(
        merkle_root=node00_new_block_header["merkle_root"],
        noonce=node00_new_block_header["noonce"],
        previous_block_hash=node00_new_block_header["previous_block_hash"],
        timestamp=node00_new_block_header["timestamp"]
    )
    assert node00_new_block_header_obj.hash == pow.new_block.block_header.hash


def test_given_good_transactions_in_mem_pool_when_new_block_is_created_then_all_nodes_add_new_block(
        create_good_transactions, blockchain_network, node00, node01, node02, network):
    blockchain_network.restart()
    time.sleep(3)
    node00_initial_blockchain = node00.get_blockchain()
    node01_initial_blockchain = node01.get_blockchain()
    node02_initial_blockchain = node02.get_blockchain()
    pow = ProofOfWork(network)
    pow.create_new_block()
    pow.broadcast()
    node00_new_blockchain = node00.get_blockchain()
    node01_new_blockchain = node01.get_blockchain()
    node02_new_blockchain = node02.get_blockchain()
    assert len(node00_initial_blockchain) == len(node01_initial_blockchain) == len(node02_initial_blockchain)
    assert len(node00_new_blockchain) == len(node01_new_blockchain) == len(node02_new_blockchain)
    assert len(node00_new_blockchain) == len(node00_initial_blockchain) + 1


def test_given_good_transactions_in_mem_pool_when_new_block_is_created_then_all_nodes_contain_correct_data(
        create_good_transactions, blockchain_network, node00, node01, node02, network):
    blockchain_network.restart()
    time.sleep(3)
    pow = ProofOfWork(network)
    pow.create_new_block()
    pow.broadcast()
    node00_new_blockchain = node00.get_blockchain()
    node01_new_blockchain = node01.get_blockchain()
    node02_new_blockchain = node02.get_blockchain()
    node00_new_block_header = node00_new_blockchain[0]["header"]
    node00_new_block_header_obj = BlockHeader(
        merkle_root=node00_new_block_header["merkle_root"],
        noonce=node00_new_block_header["noonce"],
        previous_block_hash=node00_new_block_header["previous_block_hash"],
        timestamp=node00_new_block_header["timestamp"]
    )
    node01_new_block_header = node01_new_blockchain[0]["header"]
    node01_new_block_header_obj = BlockHeader(
        merkle_root=node01_new_block_header["merkle_root"],
        noonce=node01_new_block_header["noonce"],
        previous_block_hash=node01_new_block_header["previous_block_hash"],
        timestamp=node01_new_block_header["timestamp"]
    )
    node02_new_block_header = node02_new_blockchain[0]["header"]
    node02_new_block_header_obj = BlockHeader(
        merkle_root=node02_new_block_header["merkle_root"],
        noonce=node02_new_block_header["noonce"],
        previous_block_hash=node02_new_block_header["previous_block_hash"],
        timestamp=node02_new_block_header["timestamp"]
    )
    assert node00_new_block_header_obj == node01_new_block_header_obj == node02_new_block_header_obj
    assert node00_new_block_header_obj.hash == pow.new_block.block_header.hash


def test_given_good_transactions_in_mem_pool_when_new_block_is_created_then_new_block_contains_new_transactions_and_coinbase(
        create_good_transactions, blockchain_network, node00, network):
    blockchain_network.restart()
    time.sleep(3)
    pow = ProofOfWork(network)
    pow.create_new_block()
    pow.broadcast()
    new_blockchain = node00.get_blockchain()
    assert len(new_blockchain[0]["transactions"]) == 2
    assert new_blockchain[0]["transactions"][0]["outputs"] == [
        {
            'amount': 5,
            'locking_script': "OP_DUP OP_HASH160 b'a037a093f0304f159fe1e49cfcfff769eaac7cda' OP_EQUAL_VERIFY OP_CHECKSIG"
        }
    ]
    assert new_blockchain[0]["transactions"][1]["outputs"] == [
        {
            'amount': 6.25,
            'locking_script': 'OP_DUP OP_HASH160 4d9715dc8f9578ca2af159409be9c559c5eaceba OP_EQUAL_VERIFY OP_CHECKSIG'
         }
    ]


def test_given_bad_transactions_in_mem_pool_when_new_block_is_created_then_new_block_is_refused(
        create_bad_transactions, blockchain_network, node00, network):
    blockchain_network.restart()
    initial_blockchain = node00.get_blockchain()
    pow = ProofOfWork(network)
    pow.create_new_block()
    with pytest.raises(requests.exceptions.HTTPError) as error:
        pow.broadcast()
    new_blockchain = node00.get_blockchain()
    assert 'Could not find locking script for utxo' in error.value.response.text
    assert initial_blockchain == new_blockchain
