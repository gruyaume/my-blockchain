import os

from common.node import Node

NODE00_HOSTNAME = os.environ["NODE00_HOSTNAME"]
NODE01_HOSTNAME = os.environ["NODE01_HOSTNAME"]
NODE02_HOSTNAME = os.environ["NODE02_HOSTNAME"]


class DefaultBlockchainNetwork:
    def __init__(self):
        self.node_list = [Node(NODE00_HOSTNAME), Node(NODE01_HOSTNAME), Node(NODE02_HOSTNAME)]

    def restart(self):
        for node in self.node_list:
            node.restart()
