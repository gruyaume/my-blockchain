import json
from multiprocessing import shared_memory

from common.block import Block, BlockHeader


def get_blockchain_from_memory() -> Block:
    current_mem_pool = shared_memory.ShareableList(name="blockchain")
    previous_block = None
    block_object = None
    for block in reversed(current_mem_pool):
        block_dict = json.loads(block)
        block_header_str = block_dict.pop("header")
        block_header = BlockHeader(**block_header_str)
        block_object = Block(**block_dict, block_header=block_header)
        block_object.previous_block = previous_block
        previous_block = block_object
    current_mem_pool.shm.close()
    return block_object


def store_blockchain_in_memory(blockchain: Block):
    blockchain_list = [json.dumps(i) for i in json.loads(blockchain.to_json)]

    try:
        sharable_list = shared_memory.ShareableList(blockchain_list, name="blockchain")
    except FileExistsError:
        current_sharable_list = shared_memory.ShareableList(name="blockchain")
        current_sharable_list.shm.close()
        current_sharable_list.shm.unlink()
        sharable_list = shared_memory.ShareableList(blockchain_list, name="blockchain")
    sharable_list.shm.close()
