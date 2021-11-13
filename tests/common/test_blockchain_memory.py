from common.initialize_default_blockchain import initialize_default_blockchain
from common.io_blockchain import BlockchainMemory


def test_given_two_memory_reads_from_blockchain_both_yield_same_value():
    blockchain_memory = BlockchainMemory("src/doc/blockchain")
    initialize_default_blockchain(blockchain_memory)
    first_block_read = blockchain_memory.get_blockchain_from_memory()
    second_block_read = blockchain_memory.get_blockchain_from_memory()

    assert first_block_read == second_block_read
