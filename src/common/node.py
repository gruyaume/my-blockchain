import requests


class Node:
    def __init__(self, hostname: str):
        self.hostname = hostname
        self.base_url = f"http://{hostname}/"

    def __eq__(self, other):
        return self.hostname == other.hostname

    @property
    def dict(self):
        return {
            "hostname": self.hostname
        }

    def post(self, endpoint: str, data: dict) -> requests.Response:
        url = f"{self.base_url}{endpoint}"
        req_return = requests.post(url, json=data)
        req_return.raise_for_status()
        return req_return

    def get(self, endpoint: str, data: dict = None) -> list:
        url = f"{self.base_url}{endpoint}"
        if data:
            req_return = requests.get(url, json=data)
        else:
            req_return = requests.get(url)
        req_return.raise_for_status()
        return req_return.json()

    def advertise(self, hostname: str):
        data = {"hostname": hostname}
        return self.post(endpoint="new_node_advertisement", data=data)

    def known_node_request(self, hostname: str):
        data = {"hostname": hostname}
        return self.get(endpoint="known_node_request", data=data)

    def send_new_block(self, block: dict) -> requests.Response:
        return self.post(endpoint="block", data=block)

    def send_transaction(self, transaction_data: dict) -> requests.Response:
        return self.post("transactions", transaction_data)

    def get_blockchain(self) -> list:
        return self.get(endpoint="block")
