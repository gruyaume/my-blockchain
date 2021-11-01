import requests


class Node:
    def __init__(self, ip: str, port: int):
        self.ip = ip
        self.port = port
        self.base_url = f"http://{ip}:{port}/"

    def __eq__(self, other):
        return self.ip == other.ip and self.port == other.port

    @property
    def dict(self):
        return {
            "ip": self.ip,
            "port": self.port
        }

    def post(self, endpoint: str, data: dict) -> requests.Response:
        url = f"{self.base_url}{endpoint}"
        req_return = requests.post(url, json=data)
        req_return.raise_for_status()
        return req_return

    def get(self, endpoint: str, data: dict) -> requests.Response:
        url = f"{self.base_url}{endpoint}"
        req_return = requests.get(url, json=data)
        req_return.raise_for_status()
        return req_return

    def advertise(self, ip, port):
        data = {"ip": ip, "port": port}
        return self.post(endpoint="new_node_advertisement", data=data)

    def known_node_request(self, ip, port):
        data = {"ip": ip, "port": port}
        return self.get(endpoint="known_node_request", data=data)
