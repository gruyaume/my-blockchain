import json

from common.node import Node
import requests


class Network:

    KNOWN_NODES_FILE = 'src/doc/known_nodes.json'
    FIRST_KNOWN_NODE_IP = "127.0.0.1"
    FIRST_KNOWN_NODE_PORT = 5000

    def __init__(self, node: Node):
        self.node = node
        self.initialize_known_nodes_file()

    def initialize_known_nodes_file(self):
        print("Initializing known nodes file")
        initial_known_node = Node(ip=self.FIRST_KNOWN_NODE_IP, port=self.FIRST_KNOWN_NODE_PORT)
        with open(self.KNOWN_NODES_FILE, "w") as jsonFile:
            json.dump([initial_known_node.dict], jsonFile)

    def advertise_to_all_known_nodes(self):
        print("advertising to all known nodes")
        for node in self.known_nodes:
            node.advertise(self.node.ip, self.node.port)

    def ask_known_nodes_for_their_known_nodes(self):
        print("Asking known nodes for their own known nodes")
        for node in self.known_nodes:
            node.known_node_request(self.node.ip, self.node.port)

    @property
    def known_nodes(self) -> [Node]:
        with open(self.KNOWN_NODES_FILE) as f:
            nodes = json.load(f)
            known_nodes = [Node(ip=node["ip"], port=int(node["port"])) for node in nodes]
        return known_nodes

    def store_new_node(self, new_node: Node):
        print(f"Storing new node: {new_node.ip}:{new_node.port}")
        with open(self.KNOWN_NODES_FILE, "r+") as f:
            current_nodes_json = json.load(f)
            current_nodes = [Node(ip=node["ip"], port=int(node["port"])) for node in current_nodes_json]
            if new_node not in current_nodes:
                current_nodes_json.append(new_node.dict)
                f.seek(0)
                json.dump(current_nodes_json, f)

    def join_network(self):
        print("Joining network")

        try:
            self.advertise_to_all_known_nodes()
            self.ask_known_nodes_for_their_known_nodes()
        except:
            print("Connection error when trying to join network. This could be caused by a network "
                  "issue or because we are the first node out here.")

    def validate_node_is_known(self, inquiring_node: Node) -> bool:
        if inquiring_node in self.known_nodes:
            return True
        else:
            return False

    def return_known_nodes(self) -> []:
        with open(self.KNOWN_NODES_FILE) as f:
            current_nodes_json = json.load(f)
        return current_nodes_json
