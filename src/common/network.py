import logging

import requests

from common.initialize_default_blockchain import initialize_default_blockchain
from common.io_blockchain import BlockchainMemory
from common.io_known_nodes import KnownNodesMemory
from common.node import Node


class Network:

    FIRST_KNOWN_NODE_HOSTNAME = "node00.my-blockchain.gruyaume.com"

    def __init__(self, node: Node, init_known_nodes_file: bool = True):
        self.node = node
        self.blockchain_memory = BlockchainMemory()
        self.known_nodes_memory = KnownNodesMemory()
        if init_known_nodes_file:
            self.initialize_known_nodes_file()

    def initialize_known_nodes_file(self):
        logging.info("Initializing known nodes file")
        initial_known_node = Node(hostname=self.FIRST_KNOWN_NODE_HOSTNAME)
        if self.node.dict != initial_known_node.dict:
            self.known_nodes_memory.store_known_nodes([self.node.dict, initial_known_node.dict])
        else:
            self.known_nodes_memory.store_known_nodes([self.node.dict])

    def advertise_to_all_known_nodes(self):
        logging.info("Advertising to all known nodes")
        for node in self.known_nodes_memory.known_nodes:
            if node.hostname != self.node.hostname:
                try:
                    node.advertise(self.node.hostname)
                except requests.exceptions.ConnectionError:
                    logging.info(f"Node not answering: {node.hostname}")

    def advertise_to_default_node(self) -> bool:
        logging.info(f"Advertising to default node: {self.FIRST_KNOWN_NODE_HOSTNAME}")
        default_node = Node(hostname=self.FIRST_KNOWN_NODE_HOSTNAME)
        try:
            default_node.advertise(self.node.hostname)
            logging.info("Default node answered to advertising!")
            return True
        except requests.exceptions.ConnectionError:
            logging.info(f"Default node not answering: {self.FIRST_KNOWN_NODE_HOSTNAME}")
            return False

    def ask_known_nodes_for_their_known_nodes(self) -> list:
        logging.info("Asking known nodes for their own known nodes")
        known_nodes_of_known_nodes = []
        for currently_known_node in self.known_nodes_memory.known_nodes:
            if currently_known_node.hostname != self.node.hostname:
                try:
                    known_nodes_of_known_node = currently_known_node.known_node_request()
                    for node in known_nodes_of_known_node:
                        if node["hostname"] != self.node.hostname:
                            known_nodes_of_known_nodes.append(Node(node["hostname"]))
                except requests.exceptions.ConnectionError:
                    logging.info(f"Node not answering: {currently_known_node.hostname}")
        return known_nodes_of_known_nodes

    def initialize_blockchain(self):
        longest_blockchain = self.get_longest_blockchain()
        self.blockchain_memory.store_blockchain_dict_in_memory(longest_blockchain)

    def get_longest_blockchain(self):
        logging.info("Retrieving the longest blockchain")
        longest_blockchain_size = 0
        longest_blockchain = None
        for node in self.known_nodes_memory.known_nodes:
            if node.hostname != self.node.hostname:
                try:
                    blockchain = node.get_blockchain()
                    blockchain_length = len(blockchain)
                    if blockchain_length > longest_blockchain_size:
                        longest_blockchain_size = blockchain_length
                        longest_blockchain = blockchain
                except requests.exceptions.ConnectionError:
                    logging.info(f"Node not answering: {node.hostname}")
        logging.info(f"Longest blockchain has a size of {longest_blockchain_size} blocks")
        return longest_blockchain

    @property
    def other_nodes_exist(self) -> bool:
        if len(self.known_nodes_memory.known_nodes) == 0:
            return False
        elif len(self.known_nodes_memory.known_nodes) == 1 and \
                self.known_nodes_memory.known_nodes[0].hostname == self.node.hostname:
            return False
        else:
            return True

    def join_network(self):
        logging.info("Joining network")
        if self.other_nodes_exist:
            default_node_answered = self.advertise_to_default_node()
            if default_node_answered:
                known_nodes_of_known_node = self.ask_known_nodes_for_their_known_nodes()
                self.known_nodes_memory.store_nodes(known_nodes_of_known_node)
                self.advertise_to_all_known_nodes()
                self.initialize_blockchain()
            else:
                logging.info("Default node didn't answer. This could be caused by a network issue.")
                initialize_default_blockchain(self.blockchain_memory)
        else:
            logging.info("No other node exists. We might be the first node out here.")
            initialize_default_blockchain(self.blockchain_memory)

    def return_known_nodes(self) -> []:
        return self.known_nodes_memory.return_known_nodes()
