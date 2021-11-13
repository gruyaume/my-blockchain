import time

import pytest
import requests

from blockchain_users.camille import private_key as camille_private_key
from common.node import Node
from common.transaction_input import TransactionInput
from common.transaction_output import TransactionOutput
from integration_tests.common.blockchain_network import DefaultBlockchainNetwork, NODE00_HOSTNAME
from wallet.wallet import Owner, Wallet


@pytest.fixture(scope="module")
def camille():
    return Owner(private_key=camille_private_key)


@pytest.fixture(scope="module")
def node00():
    return Node(NODE00_HOSTNAME)


@pytest.fixture(scope="module")
def blockchain_network():
    return DefaultBlockchainNetwork()


@pytest.fixture(scope="module")
def camille_wallet(camille, node00):
    return Wallet(camille, node00)


def test_given_good_transaction_when_accepted_then_transaction_is_eventually_added_to_blockchian(
        camille_wallet, blockchain_network, node00):
    blockchain_network.restart()
    time.sleep(3)
    utxo_0 = TransactionInput(transaction_hash="e10154f49ae1119777b93e5bcd1a1506b6a89c1f82cc85f63c6cbe83a39df5dc",
                              output_index=0)
    output_0 = TransactionOutput(public_key_hash=b"a037a093f0304f159fe1e49cfcfff769eaac7cda", amount=5)
    camille_wallet.process_transaction(inputs=[utxo_0], outputs=[output_0])

    initial_blockchain = node00.get_blockchain()
    timeout = 60
    start_time = time.time()
    passed_time = 0
    while passed_time < timeout:
        current_blockchain = node00.get_blockchain()
        print(len(current_blockchain))
        print(current_blockchain)
        if len(current_blockchain) == len(initial_blockchain) + 1:
            break
        time.sleep(3)
        passed_time = time.time() - start_time
    raise
