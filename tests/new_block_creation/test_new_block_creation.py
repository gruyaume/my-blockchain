import json
from multiprocessing import shared_memory

import pytest

from common.initialize_blockchain import blockchain
from common.utils import calculate_hash
from node.new_block_creation.new_block_creation import ProofOfWork, NUMBER_OF_LEADING_ZEROS


@pytest.fixture(scope="module")
def store_transactions_in_mem_pool():
    transactions = [{"a": "b"}, {"c": "d"}, {"e": "f"}, {"g": "h"}]
    transactions_str = []
    for transaction in transactions:
        transactions_str.append(json.dumps(transaction, indent=2))
    a = shared_memory.ShareableList(transactions_str, name="mem_pool")
    a.shm.close()


@pytest.fixture(scope="module")
def starting_zeros():
    return "".join([str(0) for _ in range(NUMBER_OF_LEADING_ZEROS)])


def test_given_transactions_in_mem_pool_when_new_block_is_created_then_header_hash_starts_with_four_zeros(
        store_transactions_in_mem_pool, starting_zeros):
    blockchain_base = blockchain()
    with ProofOfWork(blockchain_base) as pow:
        pow.create_new_block()
    block_header_hash = calculate_hash(json.dumps(pow.new_block.block_header.data))

    assert block_header_hash.startswith(starting_zeros)
