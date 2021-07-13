import time
from datetime import datetime

import pytest

from node.block import Block
from tests.utils import generate_transaction_data


class TestBlock:

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

    @pytest.fixture(scope="module")
    def identical_blockchain(self):
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

    @pytest.fixture(scope="module")
    def tempered_blockchain(self):
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
        outputs = [(b"Camille", 8), (b"Albert", 2)]
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

    def test_given_blockchain_when_time_passes_then_hash_doesnt_change(self, blockchain: Block):
        last_block_hash_initial = blockchain.cryptographic_hash
        time.sleep(0.05)
        last_block_hash_after_time = blockchain.cryptographic_hash
        assert last_block_hash_initial == last_block_hash_after_time

    def test_given_blockchain_when_data_is_tempered_then_hash_changes(
            self, blockchain: Block, tempered_blockchain: Block):

        assert blockchain.cryptographic_hash != tempered_blockchain.cryptographic_hash

    def test_given_two_instances_of_blockchain_when_data_is_identical_then_hash_is_identical(
            self, blockchain: Block, identical_blockchain: Block):

        assert blockchain.cryptographic_hash == identical_blockchain.cryptographic_hash
