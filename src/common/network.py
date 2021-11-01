import json
import requests
from common.node import Node


class Network:

    KNOWN_NODES_FILE = 'src/doc/known_nodes.json'

    def __init__(self, node: Node):
        self.node = node
        self.initialize_known_nodes_file()

    def initialize_known_nodes_file(self):
        initial_known_node = Node(ip="127.0.0.1", port=5000)
        with open(self.KNOWN_NODES_FILE, "w+") as jsonFile:
            json.dump([initial_known_node.dict], jsonFile)

    def advertise_to_all_known_nodes(self):
        for node in self.known_nodes:
            node.advertise(self.node.ip, self.node.port)

    @property
    def known_nodes(self) -> [Node]:
        with open(self.KNOWN_NODES_FILE) as f:
            nodes = json.load(f)
            known_nodes = [Node(ip=node["ip"], port=int(node["port"])) for node in nodes]
        return known_nodes

    def store_new_node(self, new_node: Node):
        with open(self.KNOWN_NODES_FILE, "r+") as f:
            current_nodes_json = json.load(f)
            current_nodes = [Node(ip=node["ip"], port=int(node["port"])) for node in current_nodes_json]
            if new_node not in current_nodes:
                current_nodes_json.append(new_node.dict)
                f.seek(0)
                json.dump(current_nodes_json, f)
