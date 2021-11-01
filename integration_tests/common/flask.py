import threading
import time

from werkzeug.serving import make_server

from node.main import app


class ServerThread(threading.Thread):

    def __init__(self, app, ip, port):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.server = make_server(ip, port, app)
        self.ctx = app.app_context()
        self.ctx.push()

    def run(self):
        print(f"Starting server {self.ip}:{self.port}")
        self.server.serve_forever()

    def shutdown(self):
        print(f"Stopping server {self.ip}:{self.port}")
        self.server.shutdown()


class Server:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.app = app
        self.server = None

    def start(self):
        self.server = ServerThread(self.app, self.ip, self.port)
        self.server.start()
        time.sleep(1)

    def stop(self):
        self.server.shutdown()
