import time

import pytest
import requests

from blockchain_users.camille import private_key as camille_private_key
from common.node import Node
from common.transaction_input import TransactionInput
from common.transaction_output import TransactionOutput
from integration_tests.common.blockchain_network import DefaultBlockchainNetwork, NODE00_HOSTNAME
from wallet.wallet import Owner, Wallet, Transaction


@pytest.fixture(scope="module")
def camille():
    return Owner(private_key=camille_private_key)


@pytest.fixture(scope="module")
def default_node():
    return Node(NODE00_HOSTNAME)


@pytest.fixture(scope="module")
def blockchain_network():
    return DefaultBlockchainNetwork()


@pytest.fixture(scope="module")
def camille_wallet(camille, default_node):
    return Wallet(camille, default_node)


def forge_signature(transaction_data: dict):
    input_0_dict = transaction_data["inputs"][0]
    signature, public_key = input_0_dict["unlocking_script"].split(" ")
    new_signature = signature.replace("a", "b")
    new_unlocking_script = f"{new_signature} {public_key}"
    input_0_dict["unlocking_script"] = new_unlocking_script
    transaction_data["inputs"][0] = input_0_dict
    return transaction_data


def test_given_user_has_funds_when_process_transaction_then_transaction_is_accepted(
        camille_wallet, blockchain_network):
    time.sleep(2)
    blockchain_network.restart()
    time.sleep(2)
    utxo_0 = TransactionInput(transaction_hash="e10154f49ae1119777b93e5bcd1a1506b6a89c1f82cc85f63c6cbe83a39df5dc",
                              output_index=0)
    output_0 = TransactionOutput(public_key_hash=b"a037a093f0304f159fe1e49cfcfff769eaac7cda", amount=5)
    camille_wallet.process_transaction(inputs=[utxo_0], outputs=[output_0])


def test_given_user_has_more_funds_then_necessary_when_process_transaction_then_transaction_is_accepted(
        camille_wallet, blockchain_network):
    time.sleep(2)
    blockchain_network.restart()
    time.sleep(2)
    utxo_0 = TransactionInput(transaction_hash="e10154f49ae1119777b93e5bcd1a1506b6a89c1f82cc85f63c6cbe83a39df5dc",
                              output_index=0)
    output_0 = TransactionOutput(public_key_hash=b"a037a093f0304f159fe1e49cfcfff769eaac7cda", amount=3)
    output_1 = TransactionOutput(public_key_hash=b"7681c82af05a85f68a5810d967ee3a4087711867", amount=2)
    camille_wallet.process_transaction(inputs=[utxo_0], outputs=[output_0, output_1])


def test_given_user_points_to_non_existant_utxo_when_process_transaction_then_transaction_is_refused(
        camille_wallet, blockchain_network):
    time.sleep(2)
    blockchain_network.restart()
    time.sleep(2)
    utxo_0 = TransactionInput(transaction_hash="5669d7971b76850a4d725c75fbbc20ea97bd1382e24fae43c41e121ca399b660",
                              output_index=0)
    output_0 = TransactionOutput(public_key_hash=b"a037a093f0304f159fe1e49cfcfff769eaac7cda", amount=5)
    with pytest.raises(requests.exceptions.HTTPError) as error:
        camille_wallet.process_transaction(inputs=[utxo_0], outputs=[output_0])
    assert "Could not find locking script for utxo" in error.value.response.text


def test_given_user_points_to_utxo_output_index_not_owned_by_user_when_process_transaction_then_transaction_is_refused(
        camille_wallet, blockchain_network):
    time.sleep(2)
    blockchain_network.restart()
    time.sleep(2)
    utxo_0 = TransactionInput(transaction_hash="e10154f49ae1119777b93e5bcd1a1506b6a89c1f82cc85f63c6cbe83a39df5dc",
                              output_index=3)
    output_0 = TransactionOutput(public_key_hash=b"a037a093f0304f159fe1e49cfcfff769eaac7cda", amount=5)
    with pytest.raises(requests.exceptions.HTTPError) as error:
        camille_wallet.process_transaction(inputs=[utxo_0], outputs=[output_0])
    assert 'Could not find locking script for utxo' in error.value.response.text


def test_given_inputs_and_outputs_amounts_dont_match_when_process_transaction_then_transaction_is_refused(
        camille_wallet, blockchain_network):
    time.sleep(2)
    blockchain_network.restart()
    time.sleep(2)
    utxo_0 = TransactionInput(transaction_hash="e10154f49ae1119777b93e5bcd1a1506b6a89c1f82cc85f63c6cbe83a39df5dc",
                              output_index=0)
    output_0 = TransactionOutput(public_key_hash=b"a037a093f0304f159fe1e49cfcfff769eaac7cda", amount=3)
    with pytest.raises(requests.exceptions.HTTPError) as error:
        camille_wallet.process_transaction(inputs=[utxo_0], outputs=[output_0])
    assert 'Transaction inputs and outputs did not match' in error.value.response.text


def test_given_bad_signature_when_process_transaction_then_transaction_is_refused(
        camille, blockchain_network, default_node):
    time.sleep(2)
    blockchain_network.restart()
    time.sleep(2)
    utxo_0 = TransactionInput(transaction_hash="e10154f49ae1119777b93e5bcd1a1506b6a89c1f82cc85f63c6cbe83a39df5dc",
                              output_index=0)
    output_0 = TransactionOutput(public_key_hash=b"a037a093f0304f159fe1e49cfcfff769eaac7cda", amount=5)
    transaction = Transaction(inputs=[utxo_0], outputs=[output_0])
    transaction.sign(camille)
    forged_transaction_data = forge_signature(transaction.transaction_data)
    with pytest.raises(requests.exceptions.HTTPError) as error:
        default_node.send_transaction({"transaction": forged_transaction_data})
    assert 'Transaction script validation failed' in error.value.response.text
