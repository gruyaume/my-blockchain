import requests


SERVER_1_IP = SERVER_2_IP = SERVER_3_IP = "127.0.0.1"
SERVER_1_PORT = 5000
SERVER_2_PORT = 5001
SERVER_3_PORT = 5002


def get_known_hosts(ip, port):
    url = f"http://{ip}:{port}/known_node_request"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def test_given_when_then_2():
    server_1_known_hosts = get_known_hosts(SERVER_1_IP, SERVER_1_PORT)
    server_2_known_hosts = get_known_hosts(SERVER_2_IP, SERVER_2_PORT)
    server_3_known_hosts = get_known_hosts(SERVER_3_IP, SERVER_3_PORT)

    assert len(server_1_known_hosts) == len(server_2_known_hosts) == len(server_3_known_hosts)
    for known_host in server_1_known_hosts:
        assert known_host in server_2_known_hosts
        assert known_host in server_3_known_hosts


def test_given_when_then_1():
    # TODO
    # validate that when transaction is sent, it is broadcasted by all nodes
    pass
