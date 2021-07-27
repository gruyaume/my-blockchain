import json
from multiprocessing import shared_memory

import pytest

from blockchain_users.camille import private_key as camille_private_key
from common.initialize_blockchain import blockchain
from common.transaction_input import TransactionInput
from common.transaction_output import TransactionOutput
from node.new_block_creation.new_block_creation import ProofOfWork
from wallet.wallet import Owner, Wallet, Transaction
import requests


def store_transaction_data(transactions_str: [str]):
    try:
        sharable_list = shared_memory.ShareableList(transactions_str, name="mem_pool")
    except FileExistsError:
        current_sharable_list = shared_memory.ShareableList(name='mem_pool')
        current_sharable_list.shm.close()
        current_sharable_list.shm.unlink()
        sharable_list = shared_memory.ShareableList(transactions_str, name="mem_pool")
    sharable_list.shm.close()


@pytest.fixture(scope="module")
def camille():
    return Owner(private_key=camille_private_key)


@pytest.fixture(scope="module")
def camille_wallet(camille):
    return Wallet(camille)


@pytest.fixture(scope="module")
def create_good_transactions(camille):
    utxo_0 = TransactionInput(transaction_hash="5669d7971b76850a4d725c75fbbc20ea97bd1382e2cfae43c41e121ca399b660",
                              output_index=0)
    output_0 = TransactionOutput(public_key_hash=b"a037a093f0304f159fe1e49cfcfff769eaac7cda", amount=5)
    transaction_1 = Transaction(camille, inputs=[utxo_0], outputs=[output_0])
    transaction_1.sign()
    transactions = [transaction_1]
    transactions_str = [json.dumps(transaction.transaction_data, indent=2) for transaction in transactions]
    store_transaction_data(transactions_str)


@pytest.fixture(scope="module")
def create_bad_transactions(camille):
    utxo_0 = TransactionInput(transaction_hash="5669d7971b76850a4d725c75fbbc20ea97bd1382e2cfae43c41e121ca399b660",
                              output_index=0)
    output_0 = TransactionOutput(public_key_hash=b"a037a093f0304f159fe1e49cfcfff769eaac7cda", amount=25)
    transaction_1 = Transaction(camille, inputs=[utxo_0], outputs=[output_0])
    transaction_1.sign()
    transactions = [transaction_1]
    transactions_str = [json.dumps(transaction.transaction_data, indent=2) for transaction in transactions]
    store_transaction_data(transactions_str)


def test_given_good_transactions_in_mem_pool_when_new_block_is_created_then_new_block_is_accepted(create_good_transactions):
    blockchain_base = blockchain()
    with ProofOfWork(blockchain_base) as pow:
        pow.create_new_block()
        pow.broadcast()


def test_given_bad_transactions_in_mem_pool_when_new_block_is_created_then_new_block_is_refused(create_bad_transactions):
    blockchain_base = blockchain()
    with ProofOfWork(blockchain_base) as pow:
        pow.create_new_block()
        with pytest.raises(requests.exceptions.HTTPError) as error:
            pow.broadcast()
        assert 'Transaction inputs and outputs did not match' in error.value.response.text