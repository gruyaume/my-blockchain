import time

from common.node import Node
from integration_tests.common.default_values import SERVER_HOSTNAME


def test_given_only_default_node_is_up_when_new_node_advertises_then_node_information_is_stored():
    new_node_hostname = "1.1.1.1:1234"
    default_server = Node(SERVER_HOSTNAME)
    default_server.restart()
    time.sleep(3)
    default_server.advertise(new_node_hostname)
    time.sleep(1)
    final_default_server_known_nodes = default_server.known_node_request()
    assert final_default_server_known_nodes == [
        {'hostname': 'node00.my-blockchain.gruyaume.com'}, {'hostname': '1.1.1.1:1234'}]
