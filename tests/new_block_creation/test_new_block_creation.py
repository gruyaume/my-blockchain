from datetime import datetime
from unittest.mock import patch

import pytest

from blockchain_users.albert import private_key as albert_private_key
from blockchain_users.bertrand import private_key as bertrand_private_key
from blockchain_users.camille import private_key as camille_private_key
from blockchain_users.miner import public_key_hash
from common.block import Block, BlockHeader
from common.io_mem_pool import MemPool
from common.merkle_tree import get_merkle_root
from common.network import Network
from common.node import Node
from common.transaction import Transaction
from common.transaction_input import TransactionInput
from common.transaction_output import TransactionOutput
from node.new_block_creation.new_block_creation import ProofOfWork, NUMBER_OF_LEADING_ZEROS, \
    BLOCK_REWARD
from wallet.wallet import Owner


@pytest.fixture(scope="module")
def transaction_fee():
    return 0.5


@pytest.fixture(scope="module")
def transactions(transaction_fee):
    return [
        {
            'inputs': [
                {
                    'transaction_hash': '53f41fef3b00c05448f3f1bd37265588b601b7b9c75c4b51a9876539bc2a3ecd',
                    'output_index': 0,
                    'unlocking_script': '34d7591e9054b549779a867057f9444e9550dbc985c33dd536c24556f03af3b6c40a2074f9bd1b9b8a79473e9bf3ab277206436f465836aa5f0774dccdfc57c2da62c66dfd1fae2ced3e4ea1a6e4cac1f93f41568f1003ff348c78cc1853f73098f60baebdc312fdadc1044c1e4ecc1bee1d39dacb7c1a4b002b777de3ee5168d00d1490c128a25aadcacb466be8ded401fd03450d48b24ecb46757d1d29f03c3ea1ffc3e18950078e5cac04a3fa26adfc3cad8248777972eb89e81c02737c9bf4ed0a89b4552ac721e59a4cf49c1baec2641ecebbd392924234a78c9187c149fc53b850a3c8951cd40a285164b2308fbf593c77af67808accf91806bd702a97 30820122300d06092a864886f70d01010105000382010f003082010a0282010100a1024da701411ea065119f40079b8e18b3f3546a9aacb4a5fd79a190cb052c5df8f469d00d659c9817a59a243bc781da15df5ed5cde52804556e283fa6205d1c76c290b332ed415236446ad12f56a7f2b06e64fd552372bc775f7ac2d1367ca79816ce010980a33a14b39522516e023e8a44d90d5ba9cfd3231b0a69efe9e82d74893d0420fb8bb7961ba0e5d04d697d98b9669e5c0dbcd80b9942d6e776e089fbb5cde7c1768458fc778b7421fdc0ebeb6e01c4b25f74def4c49b7fa7eacec582fd03054170d5ed6c23bf9d39b8affa104e24a522c162a7e201834462b4e5bd5530327bb614907358e75bb5234a122b460550710e178d030558a0d8e2d552830203010001'
                }
            ],
            'outputs': [
                {
                    'amount': 30 - transaction_fee,
                    'locking_script': "OP_DUP OP_HASH160 b'a037a093f0304f159fe1e49cfcfff769eaac7cda' OP_EQUAL_VERIFY OP_CHECKSIG"
                }
            ],
            'transaction_hash': 'ca89afe1ec98d140d9014d8da73c3b06dd56828ce19d3e2b6ba3bc77d653f261'
        }
    ]


@pytest.fixture(scope="module")
def mempool():
    return MemPool("src/doc/mem_pool")


@pytest.fixture(scope="module")
def store_transactions_in_mem_pool(transactions, mempool):
    mempool.store_transactions_in_memory(transactions)


@pytest.fixture(scope="module")
def starting_zeros():
    return "".join([str(0) for _ in range(NUMBER_OF_LEADING_ZEROS)])


@pytest.fixture(scope="module")
def network():
    node = Node("1.1.1.1:1234")
    return Network(node)


@pytest.fixture(scope="module")
def albert_wallet():
    return Owner(private_key=albert_private_key)


@pytest.fixture(scope="module")
def bertrand_wallet():
    return Owner(private_key=bertrand_private_key)


@pytest.fixture(scope="module")
def camille_wallet():
    return Owner(private_key=camille_private_key)


@pytest.fixture(scope="module")
def blockchain(albert_wallet, bertrand_wallet, camille_wallet):
    timestamp_0 = datetime.timestamp(datetime.fromisoformat('2011-11-04 00:05:23.111'))
    input_0 = TransactionInput(transaction_hash="abcd1234",
                               output_index=0)
    output_0 = TransactionOutput(public_key_hash=b"Albert",
                                 amount=40)
    transaction_0 = Transaction([input_0], [output_0])
    block_header_0 = BlockHeader(previous_block_hash="1111",
                                 timestamp=timestamp_0,
                                 noonce=2,
                                 merkle_root=get_merkle_root([transaction_0.transaction_data]))
    block_0 = Block(
        transactions=[transaction_0.transaction_data],
        block_header=block_header_0
    )

    timestamp_1 = datetime.timestamp(datetime.fromisoformat('2011-11-04 00:05:23.111'))
    input_0 = TransactionInput(transaction_hash=block_0.transactions[0]["transaction_hash"], output_index=0)
    output_0 = TransactionOutput(public_key_hash=bertrand_wallet.public_key_hash, amount=30)
    output_1 = TransactionOutput(public_key_hash=albert_wallet.public_key_hash, amount=10)
    transaction_1 = Transaction([input_0], [output_0, output_1])
    block_header_1 = BlockHeader(
        previous_block_hash=block_0.block_header.hash,
        timestamp=timestamp_1,
        noonce=3,
        merkle_root=get_merkle_root([transaction_1.transaction_data])
    )
    block_1 = Block(
        transactions=[transaction_1.transaction_data],
        block_header=block_header_1,
        previous_block=block_0,
    )
    timestamp_2 = datetime.timestamp(datetime.fromisoformat('2011-11-07 00:05:13.222'))
    input_0 = TransactionInput(transaction_hash=block_1.transactions[0]["transaction_hash"], output_index=1)
    output_0 = TransactionOutput(public_key_hash=camille_wallet.public_key_hash, amount=10)
    transaction_2 = Transaction([input_0], [output_0])
    block_header_2 = BlockHeader(
        previous_block_hash=block_1.block_header.hash,
        timestamp=timestamp_2,
        noonce=4,
        merkle_root=get_merkle_root([transaction_2.transaction_data])
    )
    block_2 = Block(
        transactions=[transaction_2.transaction_data],
        block_header=block_header_2,
        previous_block=block_1,
    )

    timestamp_3 = datetime.timestamp(datetime.fromisoformat('2011-11-09 00:11:13.333'))
    input_0 = TransactionInput(transaction_hash=block_1.transactions[0]["transaction_hash"], output_index=0)
    output_0 = TransactionOutput(public_key_hash=camille_wallet.public_key_hash, amount=5)
    output_1 = TransactionOutput(public_key_hash=bertrand_wallet.public_key_hash, amount=25)
    transaction_3 = Transaction([input_0], [output_0, output_1])
    block_header_3 = BlockHeader(
        previous_block_hash=block_2.block_header.hash,
        timestamp=timestamp_3,
        noonce=5,
        merkle_root=get_merkle_root([transaction_3.transaction_data])
    )
    block_3 = Block(
        transactions=[transaction_3.transaction_data],
        block_header=block_header_3,
        previous_block=block_2,
    )
    return block_3


@patch("common.io_blockchain.get_blockchain_from_memory")
def test_given_transactions_in_mem_pool_when_new_block_is_created_then_header_hash_starts_with_four_zeros(
        mock_get_blockchain_from_memory_, store_transactions_in_mem_pool, starting_zeros, network, blockchain, mempool):
    mock_get_blockchain_from_memory_.return_value = ""
    pow = ProofOfWork(network, mempool)
    pow.create_new_block()
    assert pow.new_block.block_header.hash.startswith(starting_zeros)


def test_given_transactions_in_mem_pool_when_create_new_block_then_coinbase_transaction_is_added(
        store_transactions_in_mem_pool, transactions, transaction_fee, network, mempool):
    pow = ProofOfWork(network, mempool)
    pow.create_new_block()
    new_block_transactions = pow.new_block.transactions

    assert len(new_block_transactions) == len(transactions) + 1
    assert new_block_transactions[-1] == {
        'inputs': [],
        'outputs': [{
            'amount': BLOCK_REWARD + transaction_fee,
            'locking_script': f'OP_DUP OP_HASH160 {public_key_hash} OP_EQUAL_VERIFY OP_CHECKSIG'
        }]
    }


def test_given_no_transaction_when_get_transaction_fees_then_0_is_returned(network, mempool):
    transactions = []
    pow = ProofOfWork(network, mempool)

    transaction_fees = pow.get_transaction_fees(transactions)

    assert transaction_fees == 0


def test_given_transactions_when_get_transaction_fees_then_transaction_fees_are_returned(
        transactions, network, mempool):
    pow = ProofOfWork(network, mempool)

    transaction_fees = pow.get_transaction_fees(transactions)

    assert transaction_fees == 0.5


def test_given_transaction_fees_when_get_coinbase_transaction_then_coinbase_transaction_is_returned(
        transaction_fee, network, mempool):
    pow = ProofOfWork(network, mempool)

    coinbase_transaction = pow.get_coinbase_transaction(transaction_fee)

    assert coinbase_transaction == {
        'inputs': [],
        'outputs': [{
            'amount': BLOCK_REWARD + transaction_fee,
            'locking_script': f'OP_DUP OP_HASH160 {public_key_hash} OP_EQUAL_VERIFY OP_CHECKSIG'
        }]
    }
