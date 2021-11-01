import json

import pytest
import requests
from pytest import fixture

from common.network import Network
from integration_tests.common.flask import Server
from node.main import MY_IP as SERVER_IP
from node.main import MY_PORT as SERVER_PORT


def advertise(current_node_ip, current_node_port, new_node_ip, new_node_port):
    base_url = f"http://{current_node_ip}:{current_node_port}/"
    endpoint = "new_node_advertisement"
    data = {"ip": new_node_ip, "port": new_node_port}
    url = f"{base_url}{endpoint}"
    req_return = requests.post(url, json=data)
    req_return.raise_for_status()


def request_known_nodes(current_node_ip, current_node_port, new_node_ip, new_node_port) -> list:
    base_url = f"http://{current_node_ip}:{current_node_port}/"
    endpoint = "known_node_request"
    data = {"ip": new_node_ip, "port": new_node_port}
    url = f"{base_url}{endpoint}"
    req_return = requests.get(url, json=data)
    req_return.raise_for_status()
    return req_return.json()


@fixture(scope="module")
def server():
    server = Server(SERVER_IP, SERVER_PORT)
    return server


def test_given_only_1_node_when_new_node_advertises_then_node_information_is_stored(server):
    new_node_ip = "1.1.1.1"
    new_node_port = 1234

    server.start()

    advertise(SERVER_IP, SERVER_PORT, new_node_ip, new_node_port)

    with open(Network.KNOWN_NODES_FILE) as f:
        nodes = json.load(f)

    assert nodes == [
        {
            'ip': SERVER_IP,
            'port': SERVER_PORT
        },
        {
            'ip': new_node_ip,
            'port': new_node_port
        }
    ]

    server.stop()


def test_given_existing_node_doesnt_know_new_node_when_known_node_request_then_400_error_is_returned(server):
    new_node_ip = "1.1.1.1"
    new_node_port = 1234
    server.start()
    with pytest.raises(requests.exceptions.HTTPError):
        request_known_nodes(SERVER_IP, SERVER_PORT, new_node_ip, new_node_port)
    server.stop()


def test_given_existing_node_knows_new_node_when_known_node_request_then_known_nodes_are_returned(server):
    new_node_ip = "1.1.1.1"
    new_node_port = 1234
    server.start()
    advertise(SERVER_IP, SERVER_PORT, new_node_ip, new_node_port)
    known_nodes = request_known_nodes(SERVER_IP, SERVER_PORT, new_node_ip, new_node_port)

    assert known_nodes == [
        {
            'ip': SERVER_IP,
            'port': SERVER_PORT
        },
        {
            'ip': new_node_ip,
            'port': new_node_port
        }
    ]

    server.stop()
