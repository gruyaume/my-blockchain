from datetime import datetime

import pytest

from common.transaction_input import TransactionInput
from common.transaction_output import TransactionOutput
from node.block import Block
from node.node import NodeTransaction
from wallet.wallet import Transaction, initialize_wallet


@pytest.fixture(scope="module")
def albert_wallet():
    return initialize_wallet()


@pytest.fixture(scope="module")
def bertrand_wallet():
    return initialize_wallet()


@pytest.fixture(scope="module")
def camille_wallet():
    return initialize_wallet()


@pytest.fixture(scope="module")
def blockchain(albert_wallet, bertrand_wallet, camille_wallet):
    timestamp_0 = datetime.timestamp(datetime.fromisoformat('2011-11-04 00:05:23.111'))
    input_0 = TransactionInput(transaction_hash="abcd1234",
                               output_index=0)
    output_0 = TransactionOutput(public_key_hash=b"Albert",
                                 amount=40)
    inputs = [input_0.to_json()]
    outputs = [output_0.to_json()]
    block_0 = Block(
        transaction_data={"inputs": inputs, "outputs": outputs},
        timestamp=timestamp_0
    )

    timestamp_1 = datetime.timestamp(datetime.fromisoformat('2011-11-04 00:05:23.111'))
    input_0 = TransactionInput(transaction_hash=block_0.transaction_hash,
                               output_index=0)
    output_0 = TransactionOutput(public_key_hash=bertrand_wallet.public_key_hash,
                                 amount=30)
    output_1 = TransactionOutput(public_key_hash=albert_wallet.public_key_hash,
                                 amount=10)
    inputs = [input_0.to_json()]
    outputs = [output_0.to_json(), output_1.to_json()]

    block_1 = Block(
        transaction_data={"inputs": inputs, "outputs": outputs},
        timestamp=timestamp_1,
        previous_block=block_0
    )

    timestamp_2 = datetime.timestamp(datetime.fromisoformat('2011-11-07 00:05:13.222'))
    input_0 = TransactionInput(transaction_hash=block_1.transaction_hash,
                               output_index=1)
    output_0 = TransactionOutput(public_key_hash=camille_wallet.public_key_hash,
                                 amount=10)
    inputs = [input_0.to_json()]
    outputs = [output_0.to_json()]
    block_2 = Block(
        transaction_data={"inputs": inputs, "outputs": outputs},
        timestamp=timestamp_2,
        previous_block=block_1
    )

    timestamp_3 = datetime.timestamp(datetime.fromisoformat('2011-11-09 00:11:13.333'))
    input_0 = TransactionInput(transaction_hash=block_1.transaction_hash,
                               output_index=0)
    output_0 = TransactionOutput(public_key_hash=camille_wallet.public_key_hash,
                                 amount=5)
    output_1 = TransactionOutput(public_key_hash=bertrand_wallet.public_key_hash,
                                 amount=25)
    inputs = [input_0.to_json()]
    outputs = [output_0.to_json(), output_1.to_json()]
    block_3 = Block(
        transaction_data={"inputs": inputs, "outputs": outputs},
        timestamp=timestamp_3,
        previous_block=block_2
    )
    return block_3


def test_given_valid_signature_when_signature_is_validated_then_no_exception_is_thrown(
        blockchain, albert_wallet, camille_wallet):

    utxo_0 = TransactionInput(transaction_hash=blockchain.transaction_hash, output_index=0)
    output_0 = TransactionOutput(public_key_hash=albert_wallet.public_key_hash, amount=5)
    transaction = Transaction(camille_wallet, inputs=[utxo_0], outputs=[output_0])
    transaction.sign()
    transaction_data = transaction.send_to_nodes()

    node = NodeTransaction(blockchain)
    node.receive(transaction_data)
    node.validate()


def test_test_given_sender_tries_to_send_fund_from_somebody_else_when_signature_is_validated_then_exception_is_thrown(
        blockchain, albert_wallet, camille_wallet):
    utxo_0 = TransactionInput(transaction_hash=blockchain.transaction_hash, output_index=1)
    output_0 = TransactionOutput(public_key_hash=albert_wallet.public_key_hash, amount=5)
    transaction = Transaction(camille_wallet, inputs=[utxo_0], outputs=[output_0])
    transaction.sign()
    transaction_data = transaction.send_to_nodes()

    node = NodeTransaction(blockchain)
    node.receive(transaction_data)

    with pytest.raises(Exception):
        node.validate()


def test_given_sufficient_funds_when_validate_funds_then_return_true(blockchain, albert_wallet, camille_wallet):
    utxo_0 = TransactionInput(transaction_hash=blockchain.transaction_hash, output_index=0)
    output_0 = TransactionOutput(public_key_hash=albert_wallet.public_key_hash, amount=5)
    transaction = Transaction(camille_wallet, inputs=[utxo_0], outputs=[output_0])
    transaction.sign()
    transaction_data = transaction.send_to_nodes()

    node = NodeTransaction(blockchain)
    node.receive(transaction_data)
    node.validate()
    node.validate_funds()


def test_given_insufficient_funds_when_validate_funds_then_return_false(blockchain, albert_wallet, camille_wallet):
    utxo_0 = TransactionInput(transaction_hash=blockchain.transaction_hash, output_index=0)
    output_0 = TransactionOutput(public_key_hash=albert_wallet.public_key_hash, amount=10)
    transaction = Transaction(camille_wallet, inputs=[utxo_0], outputs=[output_0])
    transaction.sign()
    transaction_data = transaction.send_to_nodes()
    node = NodeTransaction(blockchain)
    node.receive(transaction_data)
    with pytest.raises(Exception):
        node.validate_funds()
