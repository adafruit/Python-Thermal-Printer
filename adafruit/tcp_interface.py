__author__ = 'frza'

import SocketServer
from adafruit.iotp_pool import enqueue
from adafruit.iotp_pool_job import create_job
import msgpack


class IotpTCPHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        unpacker = msgpack.Unpacker()
        while True:
            r = self.request.recv(1000)
            if len(r) == 0:
                break
            unpacker.feed(r)
            for obj in unpacker:
                j = create_job(obj)
                if j is not None:
                    enqueue(j)


class ThreadingTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass


class IotpTCPServer(object):
    def __init__(self, config):
        self._config = config
        self._server = None

    def start(self):
        host = self._config.get('TCP_HOST', 'localhost')
        port = self._config.get('TCP_PORT', 9999)

        self._server = ThreadingTCPServer((host, port), IotpTCPHandler)
        self._server.serve_forever()

    def stop(self):
        self._server.shutdown()
