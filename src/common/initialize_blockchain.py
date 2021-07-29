from datetime import datetime

from blockchain_users.albert import private_key as albert_private_key
from blockchain_users.bertrand import private_key as bertrand_private_key
from blockchain_users.camille import private_key as camille_private_key
from common.block import Block, BlockHeader
from common.blockchain_memory import store_blockchain_in_memory
from common.merkle_tree import get_merkle_root
from common.transaction_input import TransactionInput
from common.transaction_output import TransactionOutput
from wallet.wallet import Owner

albert_wallet = Owner(private_key=albert_private_key)
bertrand_wallet = Owner(private_key=bertrand_private_key)
camille_wallet = Owner(private_key=camille_private_key)


def initialize_blockchain():
    timestamp_0 = datetime.timestamp(datetime.fromisoformat('2011-11-04 00:05:23.111'))
    input_0 = TransactionInput(transaction_hash="abcd1234",
                               output_index=0)
    output_0 = TransactionOutput(public_key_hash=b"Albert",
                                 amount=40)
    inputs_0 = [input_0.to_json()]
    outputs_0 = [output_0.to_json()]
    transactions_0 = [{"inputs": inputs_0, "outputs": outputs_0}]
    block_header_0 = BlockHeader(previous_block_hash="1111",
                                 timestamp=timestamp_0,
                                 noonce=2,
                                 merkle_root=get_merkle_root(transactions_0))
    block_0 = Block(
        transactions=transactions_0,
        block_header=block_header_0
    )

    timestamp_1 = datetime.timestamp(datetime.fromisoformat('2011-11-04 00:05:23.111'))
    input_0 = TransactionInput(transaction_hash=block_0.transactions[0]["transaction_hash"],
                               output_index=0)
    output_0 = TransactionOutput(public_key_hash=bertrand_wallet.public_key_hash,
                                 amount=30)
    output_1 = TransactionOutput(public_key_hash=albert_wallet.public_key_hash,
                                 amount=10)
    inputs_1 = [input_0.to_json()]
    outputs_1 = [output_0.to_json(), output_1.to_json()]
    transactions_1 = [{"inputs": inputs_1, "outputs": outputs_1}]
    block_header_1 = BlockHeader(previous_block_hash=block_0.block_header.hash,
                                 timestamp=timestamp_1,
                                 noonce=3,
                                 merkle_root=get_merkle_root(transactions_1))
    block_1 = Block(
        transactions=transactions_1,
        block_header=block_header_1,
        previous_block=block_0,
    )
    timestamp_2 = datetime.timestamp(datetime.fromisoformat('2011-11-07 00:05:13.222'))
    input_0 = TransactionInput(transaction_hash=block_1.transactions[0]["transaction_hash"],
                               output_index=1)
    output_0 = TransactionOutput(public_key_hash=camille_wallet.public_key_hash,
                                 amount=10)
    inputs_2 = [input_0.to_json()]
    outputs_2 = [output_0.to_json()]
    transactions_2 = [{"inputs": inputs_2, "outputs": outputs_2}]
    block_header_2 = BlockHeader(previous_block_hash=block_1.block_header.hash,
                                 timestamp=timestamp_2,
                                 noonce=4,
                                 merkle_root=get_merkle_root(transactions_2))
    block_2 = Block(
        transactions=transactions_2,
        block_header=block_header_2,
        previous_block=block_1,
    )

    timestamp_3 = datetime.timestamp(datetime.fromisoformat('2011-11-09 00:11:13.333'))
    input_0 = TransactionInput(transaction_hash=block_1.transactions[0]["transaction_hash"],
                               output_index=0)
    output_0 = TransactionOutput(public_key_hash=camille_wallet.public_key_hash,
                                 amount=5)
    output_1 = TransactionOutput(public_key_hash=bertrand_wallet.public_key_hash,
                                 amount=25)
    inputs_3 = [input_0.to_json()]
    outputs_3 = [output_0.to_json(), output_1.to_json()]
    transactions_3 = [{"inputs": inputs_3, "outputs": outputs_3}]
    block_header_3 = BlockHeader(previous_block_hash=block_2.block_header.hash,
                                 timestamp=timestamp_3,
                                 noonce=5,
                                 merkle_root=get_merkle_root(transactions_3))
    block_3 = Block(
        transactions=transactions_3,
        block_header=block_header_3,
        previous_block=block_2,
    )
    store_blockchain_in_memory(block_3)
