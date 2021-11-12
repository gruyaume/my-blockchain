import time

from common.node import Node
from integration_tests.common.default_values import SERVER_HOSTNAME


def test_given_only_1_node_when_new_node_advertises_then_node_information_is_stored():
    default_server = Node(SERVER_HOSTNAME)
    default_server.restart()
    time.sleep(3)
    initial_default_server_known_nodes = default_server.known_node_request()

    assert initial_default_server_known_nodes == [{'hostname': 'node00.my-blockchain.gruyaume.com'}]
