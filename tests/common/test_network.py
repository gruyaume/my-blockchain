import pytest

from common.network import Network
from common.node import Node


class TestNetwork:

    @pytest.fixture(scope="module")
    def self_node(self):
        return Node("0.0.0.0", 1234)

    def test_given_newly_initialized_node_when_known_nodes_then_hardcoded_node_is_returned(self, self_node):
        network = Network(self_node)
        nodes = network.known_nodes

        assert nodes == [Node(ip="127.0.0.1", port=5000)]

    def test_given_new_unique_node_when_store_new_node_then_new_node_is_stored(self, self_node):
        network = Network(self_node)
        new_node = Node(ip="1.1.1.1", port=5000)
        network.store_new_node(new_node)

        nodes = network.known_nodes
        assert len(nodes) == 2
        assert nodes[-1] == new_node

    def test_given_new_identical_node_when_store_new_node_then_new_node_is_not_stored(self, self_node):
        network = Network(self_node)
        new_node = Node(ip="127.0.0.1", port=5000)
        network.store_new_node(new_node)

        nodes = network.known_nodes
        assert len(nodes) == 1

    def test_given_known_hosts_when_advertise_to_all_known_nodes_then_http_post_is_sent_to_all_known_hosts(self):
        # TODO
        raise
