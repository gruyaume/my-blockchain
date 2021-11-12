import logging
import os
import time

from common.io_mem_pool import MemPool
from common.network import Network
from common.node import Node
from node.new_block_creation.new_block_creation import ProofOfWork, BlockException

logging.basicConfig(level=logging.DEBUG, format=f'%(asctime)s: %(message)s')


def main():
    my_hostname = os.environ['MY_HOSTNAME']
    mempool_dir = os.environ['MEMPOOL_DIR']
    my_node = Node(my_hostname)
    network = Network(my_node, init_known_nodes_file=False)
    mempool = MemPool(mempool_dir)
    mempool.clear_transactions_from_memory()

    while True:
        pow = ProofOfWork(network)
        try:
            pow.create_new_block()
            pow.broadcast()
            mempool.clear_transactions_from_memory()
        except BlockException:
            logging.info("No transaction in mem pool")
        time.sleep(5)


if __name__ == "__main__":
    main()
