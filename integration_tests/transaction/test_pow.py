import time

import pytest

from blockchain_users.camille import private_key as camille_private_key
from common.node import Node
from common.transaction_input import TransactionInput
from common.transaction_output import TransactionOutput
from integration_tests.common.blockchain_network import DefaultBlockchainNetwork, NODE00_HOSTNAME, \
    NODE01_HOSTNAME, NODE02_HOSTNAME
from wallet.wallet import Owner, Wallet


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
def camille_wallet(camille, node00):
    return Wallet(camille, node00)


def test_given_good_transaction_when_accepted_then_transaction_is_eventually_part_of_blockchain(
        camille_wallet, blockchain_network, node00):
    time.sleep(2)
    blockchain_network.restart()
    time.sleep(2)
    transaction_hash = "e10154f49ae1119777b93e5bcd1a1506b6a89c1f82cc85f63c6cbe83a39df5dc"
    output_index = 0
    utxo_0 = TransactionInput(transaction_hash=transaction_hash,
                              output_index=output_index)
    output_0 = TransactionOutput(public_key_hash=b"a037a093f0304f159fe1e49cfcfff769eaac7cda", amount=5)
    camille_wallet.process_transaction(inputs=[utxo_0], outputs=[output_0])

    initial_blockchain = node00.get_blockchain()
    timeout = 60
    start_time = time.time()
    passed_time = 0
    while passed_time < timeout:
        current_blockchain = node00.get_blockchain()
        if len(current_blockchain) == len(initial_blockchain) + 1:
            latest_block_transactions = current_blockchain[0]["transactions"]
            our_transaction = latest_block_transactions[0]
            assert our_transaction["inputs"][0]["output_index"] == output_index
            assert our_transaction["inputs"][0]["transaction_hash"] == transaction_hash
            return
        time.sleep(2)
        passed_time = time.time() - start_time
    raise TimeoutError("Blockchain didn't change size in the expected time")


def test_given_good_transaction_when_accepted_then_new_block_is_created_and_propagated(
        camille_wallet, blockchain_network, node00, node01, node02):
    time.sleep(2)
    blockchain_network.restart()
    time.sleep(2)
    transaction_hash = "e10154f49ae1119777b93e5bcd1a1506b6a89c1f82cc85f63c6cbe83a39df5dc"
    output_index = 0
    utxo_0 = TransactionInput(transaction_hash=transaction_hash,
                              output_index=output_index)
    output_0 = TransactionOutput(public_key_hash=b"a037a093f0304f159fe1e49cfcfff769eaac7cda", amount=5)
    camille_wallet.process_transaction(inputs=[utxo_0], outputs=[output_0])

    node00_initial_blockchain = node00.get_blockchain()
    node01_initial_blockchain = node01.get_blockchain()
    node02_initial_blockchain = node02.get_blockchain()
    assert len(node00_initial_blockchain) == len(node01_initial_blockchain) == len(node02_initial_blockchain)
    timeout = 60
    start_time = time.time()
    passed_time = 0
    while passed_time < timeout:
        node00_current_blockchain = node00.get_blockchain()
        node01_current_blockchain = node01.get_blockchain()
        node02_current_blockchain = node02.get_blockchain()
        if len(node00_current_blockchain) == len(node01_current_blockchain) == len(node02_current_blockchain) and len(node00_current_blockchain) == len(node00_initial_blockchain) + 1:
            latest_node_00_block_transactions = node00_current_blockchain[0]["transactions"]
            latest_node_01_block_transactions = node01_current_blockchain[0]["transactions"]
            latest_node_02_block_transactions = node02_current_blockchain[0]["transactions"]
            node_00_latest_transaction = latest_node_00_block_transactions[0]
            node_01_latest_transaction = latest_node_01_block_transactions[0]
            node_02_latest_transaction = latest_node_02_block_transactions[0]
            assert node_00_latest_transaction["inputs"][0]["output_index"] == output_index
            assert node_00_latest_transaction["inputs"][0]["transaction_hash"] == transaction_hash
            assert node_01_latest_transaction["inputs"][0]["output_index"] == output_index
            assert node_01_latest_transaction["inputs"][0]["transaction_hash"] == transaction_hash
            assert node_02_latest_transaction["inputs"][0]["output_index"] == output_index
            assert node_02_latest_transaction["inputs"][0]["transaction_hash"] == transaction_hash
            return
        time.sleep(2)
        passed_time = time.time() - start_time
    raise TimeoutError("Blockchain didn't change size in the expected time")
