import time

import pytest

from common.node import Node
from integration_tests.common.blockchain_network import DefaultBlockchainNetwork, NODE00_HOSTNAME, \
    NODE01_HOSTNAME, NODE02_HOSTNAME


@pytest.fixture(scope="module")
def node00():
    return Node(NODE00_HOSTNAME)


@pytest.fixture(scope="module")
def node01():
    return Node(NODE01_HOSTNAME)


@pytest.fixture(scope="module")
def node02():
    return Node(NODE02_HOSTNAME)


@pytest.fixture(scope="module")
def blockchain_network():
    return DefaultBlockchainNetwork()


def test_given_network_of_3_nodes_when_new_nodes_initialize_then_all_nodes_store_all_nodes(
        node00, node01, node02, blockchain_network):
    time.sleep(2)
    blockchain_network.restart()
    time.sleep(2)
    node_00_known_nodes = node00.known_node_request()
    node_01_known_nodes = node01.known_node_request()
    node_02_known_nodes = node02.known_node_request()

    expected_dicts = [
        {'hostname': 'node00.my-blockchain.gruyaume.com'},
        {'hostname': 'node01.my-blockchain.gruyaume.com'},
        {'hostname': 'node02.my-blockchain.gruyaume.com'}
    ]
    for node_dict in expected_dicts:
        assert node_dict in node_00_known_nodes
        assert node_dict in node_01_known_nodes
        assert node_dict in node_02_known_nodes
