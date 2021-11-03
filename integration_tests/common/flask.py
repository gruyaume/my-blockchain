import time
from multiprocessing import Process

from node.main import main


class Server:
    def __init__(self):
        self.server = None

    def start(self):
        self.server = Process(target=main)
        self.server.start()
        time.sleep(0.5)

    def stop(self):
        self.server.terminate()
        self.server.join()
