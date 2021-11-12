from common.node import Node

NODE00_HOSTNAME = "node00.my-blockchain.gruyaume.com"
NODE01_HOSTNAME = "node01.my-blockchain.gruyaume.com"
NODE02_HOSTNAME = "node02.my-blockchain.gruyaume.com"


class DefaultBlockchainNetwork:
    def __init__(self):
        self.node_list = [Node(NODE00_HOSTNAME), Node(NODE01_HOSTNAME), Node(NODE02_HOSTNAME)]

    def restart(self):
        for node in self.node_list:
            node.restart()
