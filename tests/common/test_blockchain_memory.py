from common.blockchain_memory import get_blockchain_from_memory
from common.initialize_blockchain import initialize_blockchain


def test_given_two_memory_reads_from_blockchain_both_yield_same_value():
    initialize_blockchain()
    first_block_read = get_blockchain_from_memory()
    second_block_read = get_blockchain_from_memory()

    assert first_block_read == second_block_read
