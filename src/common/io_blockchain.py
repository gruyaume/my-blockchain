import json
import logging
import os

from common.block import Block, BlockHeader


class BlockchainMemory:

    def __init__(self):
        self.file_name = os.environ["BLOCKCHAIN_DIR"]

    def get_blockchain_from_memory(self):
        logging.info("Getting blockchain from memory")
        with open(self.file_name, "r") as file_obj:
            blocks_text = file_obj.read()
            block_list = json.loads(blocks_text)
            previous_block = None
            for block_dict in reversed(block_list):
                block_header_str = block_dict.pop("header")
                block_header = BlockHeader(**block_header_str)
                block_object = Block(**block_dict, block_header=block_header)
                block_object.previous_block = previous_block
                previous_block = block_object
        return block_object

    def store_blockchain_in_memory(self, blockchain: Block):
        self.store_blockchain_dict_in_memory(blockchain.to_dict)

    def store_blockchain_dict_in_memory(self, blockchain_list: list):
        logging.info("Storing blockchain in memory")
        text = json.dumps(blockchain_list).encode("utf-8")
        with open(self.file_name, "wb") as file_obj:
            file_obj.write(text)
