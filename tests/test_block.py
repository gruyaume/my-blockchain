import time
from datetime import datetime

import pytest

from block import Block


class TestBlock:

    @pytest.fixture(scope="module")
    def blockchain(self):
        timestamp_0 = datetime.timestamp(datetime.fromisoformat('2011-11-04 00:05:23.111'))
        transaction_data_0 = "Albert,Bertrand,30"
        block_0 = Block(
            transaction_data=transaction_data_0,
            timestamp=timestamp_0
        )

        timestamp_1 = datetime.timestamp(datetime.fromisoformat('2011-11-07 00:05:13.222'))
        transaction_data_1 = "Albert,Camille,10"
        block_1 = Block(
            transaction_data=transaction_data_1,
            timestamp=timestamp_1,
            previous_block_cryptographic_hash=block_0.cryptographic_hash()
        )

        timestamp_2 = datetime.timestamp(datetime.fromisoformat('2011-11-09 00:11:13.333'))
        transaction_data_2 = "Bertrand,Camille,5"
        block_2 = Block(
            transaction_data=transaction_data_2,
            timestamp=timestamp_2,
            previous_block_cryptographic_hash=block_1.cryptographic_hash()
        )
        return block_2

    @pytest.fixture(scope="module")
    def identical_blockchain(self):
        timestamp_0 = datetime.timestamp(datetime.fromisoformat('2011-11-04 00:05:23.111'))
        transaction_data_0 = "Albert,Bertrand,30"
        block_0 = Block(
            transaction_data=transaction_data_0,
            timestamp=timestamp_0
        )

        timestamp_1 = datetime.timestamp(datetime.fromisoformat('2011-11-07 00:05:13.222'))
        transaction_data_1 = "Albert,Camille,10"
        block_1 = Block(
            transaction_data=transaction_data_1,
            timestamp=timestamp_1,
            previous_block_cryptographic_hash=block_0.cryptographic_hash()
        )

        timestamp_2 = datetime.timestamp(datetime.fromisoformat('2011-11-09 00:11:13.333'))
        transaction_data_2 = "Bertrand,Camille,5"
        block_2 = Block(
            transaction_data=transaction_data_2,
            timestamp=timestamp_2,
            previous_block_cryptographic_hash=block_1.cryptographic_hash()
        )
        return block_2

    @pytest.fixture(scope="module")
    def tempered_blockchain(self):
        timestamp_0 = datetime.timestamp(datetime.fromisoformat('2011-11-04 00:05:23.111'))
        transaction_data_0 = "Albert,Bertrand,30"
        block_0 = Block(
            transaction_data=transaction_data_0,
            timestamp=timestamp_0
        )

        timestamp_1 = datetime.timestamp(datetime.fromisoformat('2011-11-07 00:05:13.222'))
        transaction_data_1 = "Albert,Camille,8"
        block_1 = Block(
            transaction_data=transaction_data_1,
            timestamp=timestamp_1,
            previous_block_cryptographic_hash=block_0.cryptographic_hash()
        )

        timestamp_2 = datetime.timestamp(datetime.fromisoformat('2011-11-09 00:11:13.333'))
        transaction_data_2 = "Bertrand,Camille,5"
        block_2 = Block(
            transaction_data=transaction_data_2,
            timestamp=timestamp_2,
            previous_block_cryptographic_hash=block_1.cryptographic_hash()
        )
        return block_2

    def test_given_blockchain_when_time_passes_then_hash_doesnt_change(self, blockchain: Block):

        last_block_hash_initial = blockchain.cryptographic_hash()
        time.sleep(0.05)
        last_block_hash_after_time = blockchain.cryptographic_hash()
        assert last_block_hash_initial == last_block_hash_after_time

    def test_given_blockchain_when_data_is_tempered_then_hash_changes(
            self, blockchain: Block, tempered_blockchain: Block):

        assert blockchain.cryptographic_hash() != tempered_blockchain.cryptographic_hash()

    def test_given_two_instances_of_blockchain_when_data_is_identical_then_hash_is_identical(
            self, blockchain: Block, identical_blockchain: Block):

        assert blockchain.cryptographic_hash() == identical_blockchain.cryptographic_hash()
