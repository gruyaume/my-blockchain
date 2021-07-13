from datetime import datetime

import pytest

from node.block import Block
from node.node import NodeTransaction
from tests.utils import generate_transaction_data
from transaction.transaction_input import TransactionInput


class TestNode:

    @pytest.fixture(scope="module")
    def blockchain(self):
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

    def test_given_more_then_sufficient_funds_when_validate_funds_then_return_true(self, blockchain):
        node = NodeTransaction(blockchain)
        utxo_0 = TransactionInput(transaction_hash="dd6b073c0dc172f100705d53e295dad06103b8e1e4e74d4632b7950e51be13b9",
                                  output_index=0)
        enough_funds = node.validate_funds(5, [utxo_0])

        assert enough_funds

    def test_given_exactly_sufficient_funds_when_validate_funds_then_return_true(self, blockchain):
        node = NodeTransaction(blockchain)
        utxo_0 = TransactionInput(transaction_hash="dd6b073c0dc172f100705d53e295dad06103b8e1e4e74d4632b7950e51be13b9",
                                  output_index=0)
        utxo_1 = TransactionInput(transaction_hash="8d7acdaacb6fb49dc88594880f723a2e2fda1c15b35a5c3f2353f06fe500e554",
                                  output_index=0)
        enough_funds = node.validate_funds(15, [utxo_0, utxo_1])

        assert enough_funds

    def test_given_insufficient_funds_when_validate_funds_then_return_false(self, blockchain):
        node = NodeTransaction(blockchain)
        utxo_0 = TransactionInput(transaction_hash="dd6b073c0dc172f100705d53e295dad06103b8e1e4e74d4632b7950e51be13b9",
                                  output_index=0)
        utxo_1 = TransactionInput(transaction_hash="8d7acdaacb6fb49dc88594880f723a2e2fda1c15b35a5c3f2353f06fe500e554",
                                  output_index=0)
        enough_funds = node.validate_funds(20, [utxo_0, utxo_1])

        assert not enough_funds
