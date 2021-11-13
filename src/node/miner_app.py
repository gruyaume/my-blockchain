import logging
import os
import time
import requests
from common.io_mem_pool import MemPool
from node.new_block_creation.new_block_creation import ProofOfWork, BlockException

logging.basicConfig(level=logging.DEBUG, format=f'%(asctime)s: %(message)s')


def main():
    my_hostname = os.environ['MY_HOSTNAME']
    mempool = MemPool()
    mempool.clear_transactions_from_memory()

    while True:
        pow = ProofOfWork(my_hostname)
        try:
            pow.create_new_block()
            pow.broadcast()
            mempool.clear_transactions_from_memory()
        except BlockException:
            logging.info("No transaction in mem pool")
        time.sleep(5)


if __name__ == "__main__":
    main()
