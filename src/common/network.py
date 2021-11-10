import json

import requests

from common.initialize_default_blockchain import initialize_default_blockchain
from common.io_blockchain import store_blockchain_dict_in_memory
from common.node import Node


class Network:

    KNOWN_NODES_FILE = 'src/doc/known_nodes.json'
    FIRST_KNOWN_NODE_HOSTNAME = "my-blockchain.gruyaume.com"

    def __init__(self, node: Node):
        self.node = node
        self.initialize_known_nodes_file()

    def initialize_known_nodes_file(self):
        print("Initializing known nodes file")
        initial_known_node = Node(hostname=self.FIRST_KNOWN_NODE_HOSTNAME)
        with open(self.KNOWN_NODES_FILE, "w") as jsonFile:
            if self.node.dict != initial_known_node.dict:
                json.dump([self.node.dict, initial_known_node.dict], jsonFile)
            else:
                json.dump([self.node.dict], jsonFile)

    def advertise_to_all_known_nodes(self):
        print("Advertising to all known nodes")
        for node in self.known_nodes:
            if node.hostname != self.node.hostname:
                try:
                    node.advertise(self.node.hostname)
                except requests.exceptions.ConnectionError:
                    print(f"Node not answering: {node.hostname}")

    def ask_known_nodes_for_their_known_nodes(self) -> list:
        print("Asking known nodes for their own known nodes")
        known_nodes_of_known_nodes = []
        for currently_known_node in self.known_nodes:
            if currently_known_node.hostname != self.node.hostname:
                try:
                    known_nodes_of_known_node = currently_known_node.known_node_request(self.node.hostname)
                    for node in known_nodes_of_known_node:
                        if node["hostname"] != self.node.hostname:
                            known_nodes_of_known_nodes.append(Node(node["hostname"]))
                except requests.exceptions.ConnectionError:
                    print(f"Node not answering: {currently_known_node.hostname}")
        return known_nodes_of_known_nodes

    @property
    def known_nodes(self) -> [Node]:
        with open(self.KNOWN_NODES_FILE) as f:
            nodes = json.load(f)
            known_nodes = [Node(hostname=node["hostname"]) for node in nodes]
        return known_nodes

    def store_new_node(self, new_node: Node):
        print(f"Storing new node: {new_node.hostname}")
        with open(self.KNOWN_NODES_FILE, "r+") as f:
            current_nodes_json = json.load(f)
            current_nodes = [Node(hostname=node["hostname"]) for node in current_nodes_json]
            if new_node not in current_nodes:
                current_nodes_json.append(new_node.dict)
                f.seek(0)
                json.dump(current_nodes_json, f)

    def store_nodes(self, nodes: [Node]):
        for node in nodes:
            self.store_new_node(node)

    def initialize_blockchain(self):
        longest_blockchain = self.get_longest_blockchain()
        store_blockchain_dict_in_memory(longest_blockchain)

    def get_longest_blockchain(self):
        print("Retrieving the longest blockchain")
        longest_blockchain_size = 0
        longest_blockchain = None
        for node in self.known_nodes:
            if node.hostname != self.node.hostname:
                try:
                    blockchain = node.get_blockchain()
                    blockchain_length = len(blockchain)
                    if blockchain_length > longest_blockchain_size:
                        longest_blockchain_size = blockchain_length
                        longest_blockchain = blockchain
                except requests.exceptions.ConnectionError:
                    print(f"Node not answering: {node.hostname}")
        print(f"Longest blockchain has a size of {longest_blockchain_size} blocks")
        return longest_blockchain

    @property
    def other_nodes_exist(self) -> bool:
        if len(self.known_nodes) == 0:
            return False
        elif len(self.known_nodes) == 1 and self.known_nodes[0].hostname == self.node.hostname:
            return False
        else:
            return True

    def join_network(self):
        print("Joining network")
        if self.other_nodes_exist:
            self.advertise_to_all_known_nodes()
            known_nodes_of_known_node = self.ask_known_nodes_for_their_known_nodes()
            self.store_nodes(known_nodes_of_known_node)
            self.advertise_to_all_known_nodes()
            self.initialize_blockchain()
        else:
            print("No other node exists. This could be caused by a network issue or because we are the first node out here.")
            initialize_default_blockchain()

    def return_known_nodes(self) -> []:
        with open(self.KNOWN_NODES_FILE) as f:
            current_nodes_json = json.load(f)
        return current_nodes_json
