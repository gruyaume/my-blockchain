import time

import pytest

from common.node import Node
from integration_tests.common.blockchain_network import DefaultBlockchainNetwork, NODE00_HOSTNAME


@pytest.fixture(scope="module")
def default_node():
    return Node(NODE00_HOSTNAME)


@pytest.fixture(scope="module")
def blockchain_network():
    return DefaultBlockchainNetwork()


def test_given_only_default_node_is_up_when_new_node_advertises_then_node_information_is_stored(
    default_node, blockchain_network
):
    time.sleep(2)
    new_node_hostname = "1.1.1.1:1234"
    blockchain_network.restart()
    time.sleep(2)
    default_node.advertise(new_node_hostname)
    time.sleep(1)
    final_default_server_known_nodes = default_node.known_node_request()
    expected_dict = {'hostname': new_node_hostname}
    assert expected_dict in final_default_server_known_nodes
