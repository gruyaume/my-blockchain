import binascii
import json
import os
from datetime import datetime

import pytest

from node.block import Block
from node.node import NodeTransaction
from tests.utils import generate_transaction_data
from transaction.transaction_input import TransactionInput
from transaction.transaction_output import TransactionOutput
from wallet.utils import convert_transaction_data_to_bytes
from wallet.wallet import Transaction, initialize_wallet


def open_transaction_file(file_directory: str):
    f = open(file_directory, "r")
    file_content = f.read()
    file_dict = json.loads(file_content)
    transaction_data = file_dict["transaction_data"].encode("utf-8")
    transaction_data_dict = json.loads(transaction_data)
    transaction_data_bytes = convert_transaction_data_to_bytes(transaction_data_dict)
    signature_bytes = binascii.unhexlify(file_dict["signature"])
    return transaction_data_bytes, signature_bytes


@pytest.fixture(scope="module")
def blockchain():
    timestamp_0 = datetime.timestamp(datetime.fromisoformat('2011-11-04 00:05:23.111'))
    inputs = [("0000xxxx:0", 40)]
    outputs = [(b"Albert", 40)]
    transaction_data_0 = generate_transaction_data(inputs, outputs)
    block_0 = Block(
        transaction_data=transaction_data_0,
        timestamp=timestamp_0
    )

    timestamp_1 = datetime.timestamp(datetime.fromisoformat('2011-11-04 00:05:23.111'))
    inputs = [("aaaa1111:0", 40)]
    outputs = [(b"Bertrand", 30), (b"Albert", 10)]
    transaction_data_1 = generate_transaction_data(inputs, outputs)
    block_1 = Block(
        transaction_data=transaction_data_1,
        timestamp=timestamp_1,
        previous_block=block_0
    )

    timestamp_2 = datetime.timestamp(datetime.fromisoformat('2011-11-07 00:05:13.222'))
    inputs = [("bbbb2222:1", 10)]
    outputs = [(b"Camille", 10)]
    transaction_data_2 = generate_transaction_data(inputs, outputs)
    block_2 = Block(
        transaction_data=transaction_data_2,
        timestamp=timestamp_2,
        previous_block=block_1
    )

    timestamp_3 = datetime.timestamp(datetime.fromisoformat('2011-11-09 00:11:13.333'))
    inputs = [("bbbb2222:0", 30)]
    outputs = [(b"Camille", 5), (b"Bertrand", 25)]
    transaction_data_3 = generate_transaction_data(inputs, outputs)
    block_3 = Block(
        transaction_data=transaction_data_3,
        timestamp=timestamp_3,
        previous_block=block_2
    )
    return block_3


def test_given_valid_signature_when_signature_is_validated_then_no_exception_is_thrown():
    owner = initialize_wallet()
    utxo_0 = TransactionInput(transaction_hash="dd6b073c0dc172f100705d53e295dad06103b8e1e4e74d4632b7950e51be13b9",
                              output_index=0)
    output_0 = TransactionOutput(b'Bertrand', 5)
    transaction = Transaction(owner, inputs=[utxo_0], outputs=[output_0])
    transaction.sign()

    transaction_content = transaction.send_to_nodes()

    node_transaction = NodeTransaction(blockchain)
    node_transaction.receive(transaction_content)
    node_transaction.validate_signature()


def test_test_given_non_valid_signature_when_signature_is_validated_then_exception_is_thrown():
    owner = initialize_wallet()
    utxo_0 = TransactionInput(transaction_hash="dd6b073c0dc172f100705d53e295dad06103b8e1e4e74d4632b7950e51be13b9",
                              output_index=0)
    output_0 = TransactionOutput(b'Bertrand', 5)
    transaction = Transaction(owner, inputs=[utxo_0], outputs=[output_0])
    transaction.sign()

    transaction_content = transaction.send_to_nodes()

    node_transaction = NodeTransaction(blockchain)
    node_transaction.receive(transaction_content)

    tx_data_0 = json.loads(node_transaction.inputs[0])
    tx_data_0["output_index"] = 1

    node_transaction.inputs[0] = json.dumps(tx_data_0)
    with pytest.raises(Exception):
        node_transaction.validate_signature()
