import json

import requests
from pytest import fixture

from common.network import Network
from integration_tests.common.flask import Server
from node.main import MY_HOSTNAME as SERVER_HOSTNAME


def advertise(current_node_hostname: str, new_node_hostname: str):
    base_url = f"http://{current_node_hostname}/"
    endpoint = "new_node_advertisement"
    data = {"hostname": new_node_hostname}
    url = f"{base_url}{endpoint}"
    req_return = requests.post(url, json=data)
    req_return.raise_for_status()


def request_known_nodes(current_node_hostname: str) -> list:
    base_url = f"http://{current_node_hostname}/"
    endpoint = "known_node_request"
    url = f"{base_url}{endpoint}"
    req_return = requests.get(url)
    req_return.raise_for_status()
    return req_return.json()


@fixture(scope="module")
def server():
    server = Server()
    return server


def test_given_only_1_node_when_new_node_advertises_then_node_information_is_stored(server):
    new_node_hostname = "1.1.1.1:1234"

    server.start()

    advertise(SERVER_HOSTNAME, new_node_hostname)

    with open(Network.KNOWN_NODES_FILE) as f:
        nodes = json.load(f)

    assert nodes == [
        {
            'hostname': SERVER_HOSTNAME,
        },
        {
            'hostname': new_node_hostname,
        }
    ]

    server.stop()


def test_given_existing_node_when_known_node_request_then_known_nodes_are_returned(server):
    new_node_hostname = "1.1.1.1:1234"
    server.start()
    advertise(SERVER_HOSTNAME, new_node_hostname)
    known_nodes = request_known_nodes(SERVER_HOSTNAME)

    assert known_nodes == [
        {
            'hostname': SERVER_HOSTNAME,
        },
        {
            'hostname': new_node_hostname,
        }
    ]

    server.stop()
