import requests


class Node:
    def __init__(self, ip: str, port: int):
        self.base_url = f"http://{ip}:{port}/"

    def post(self, endpoint: str, data: dict) -> requests.Response:
        url = f"{self.base_url}{endpoint}"
        req_return = requests.post(url, json=data)
        req_return.raise_for_status()
        return req_return
