from unittest.mock import patch

import pytest

from common.network import Network
from common.node import Node


class TestNetwork:

    @pytest.fixture(scope="module")
    def self_node(self):
        return Node("0.0.0.0:1234")

    def test_given_newly_initialized_node_when_known_nodes_then_hardcoded_node_is_returned(self, self_node):
        network = Network(self_node)
        nodes = network.known_nodes

        assert nodes == [Node(hostname="127.0.0.1:5000")]

    def test_given_new_unique_node_when_store_new_node_then_new_node_is_stored(self, self_node):
        network = Network(self_node)
        new_node = Node(hostname="1.1.1.1:5000")
        network.store_new_node(new_node)

        nodes = network.known_nodes
        assert len(nodes) == 2
        assert nodes[-1] == new_node

    def test_given_new_identical_node_when_store_new_node_then_new_node_is_not_stored(self, self_node):
        network = Network(self_node)
        new_node = Node(hostname="127.0.0.1:5000")
        network.store_new_node(new_node)

        nodes = network.known_nodes
        assert len(nodes) == 1

    @patch("requests.post")
    def test_given_known_hosts_when_advertise_to_all_known_nodes_then_http_post_is_sent_to_all_known_hosts(self, mock_post, self_node):
        network = Network(self_node)

        network.advertise_to_all_known_nodes()

        args, kwargs = mock_post.call_args

        assert mock_post.call_count == 1
        assert args[0] == f"http://{Network.FIRST_KNOWN_NODE_HOSTNAME}/new_node_advertisement"
        assert kwargs["json"] == {'hostname': self_node.hostname}
