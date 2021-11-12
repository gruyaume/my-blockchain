import logging
import os
import time

from common.io_mem_pool import clear_transactions_from_memory
from common.network import Network
from common.node import Node
from node.new_block_creation.new_block_creation import ProofOfWork, BlockException

logging.basicConfig(level=logging.DEBUG, format=f'%(asctime)s: %(message)s')


def main():
    my_hostname = os.environ['MY_HOSTNAME']
    my_node = Node(my_hostname)
    network = Network(my_node, init_known_nodes_file=False)
    clear_transactions_from_memory()

    while True:
        pow = ProofOfWork(network)
        try:
            pow.create_new_block()
            pow.broadcast()
            clear_transactions_from_memory()
        except BlockException:
            logging.info("No transaction in mem pool")
        time.sleep(5)


if __name__ == "__main__":
    main()
