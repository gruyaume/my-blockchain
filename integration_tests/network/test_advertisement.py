import requests

import json
from integration_tests.common.flask import Server

KNOWN_NODES_FILE = 'src/doc/known_nodes.json'


def advertise(curren_node_ip, current_node_port, new_node_ip, new_node_port):
    base_url = f"http://{curren_node_ip}:{current_node_port}/"
    endpoint = "new_node_advertisement"
    data = {"ip": new_node_ip, "port": new_node_port}
    url = f"{base_url}{endpoint}"
    req_return = requests.post(url, json=data)
    req_return.raise_for_status()


def test_given_only_1_node_when_new_node_advertises_then_node_information_is_stored():

    current_node_ip = "127.0.0.1"
    current_node_port = 5000
    new_node_ip = "1.1.1.1"
    new_node_port = 1234
    server_0 = Server(current_node_ip, current_node_port)
    server_0.start()

    advertise(current_node_ip, current_node_port, new_node_ip, new_node_port)

    with open(KNOWN_NODES_FILE) as f:
        nodes = json.load(f)

    assert nodes == [
        {
            'ip': current_node_ip,
            'port': current_node_port
        },
        {
            'ip': new_node_ip,
            'port': new_node_port
        }
    ]

    server_0.stop()
