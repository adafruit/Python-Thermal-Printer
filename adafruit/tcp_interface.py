__author__ = 'frza'

import SocketServer
import threading
from adafruit.iotp_pool import enqueue, job_state
from adafruit.iotp_pool_job import create_job
import msgpack


class IotpTCPHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        unpacker = msgpack.Unpacker()
        while True:
            try:
                r = self.request.recv(1000)
                if len(r) == 0:
                    break
                unpacker.feed(r)
                for obj in unpacker:
                    if obj.get('type', None) is None:
                        self.send_err()

                    if obj['type'] == 'query_job_state':
                        job_id = obj.get('job_id', 'foo')
                        state = job_state(job_id)
                        if state is False:
                            rsp = {'query_state': 'job_not_found'}
                        else:
                            rsp = {'query_state': 'ok', 'job_id': job_id, 'job_state': state}
                        self.request.send(msgpack.packb(rsp))
                    else:
                        j = create_job(obj)
                        if j is not None:
                            if enqueue(j):
                                rsp = msgpack.packb({'status': 'queued', 'job_id': str(j.id)})
                            else:
                                rsp = msgpack.packb({'status': 'rejected', 'reason': 'queue_full', 'job_id': str(j.id)})
                            self.request.send(rsp)
                        else:
                            self.send_err()
            except Exception as err:
                print "Exception: {}".format(err)
                self.send_err()
                break

    def send_err(self):
        self.request.send(msgpack.packb({'status': 'do_not_understand'}))


class ThreadingTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass


class IotpTCPServer(object):
    def __init__(self, config):
        self._config = config
        self._server = None
        self._thread = None

    def start(self):
        host = self._config.get('TCP_HOST', 'localhost')
        port = self._config.get('TCP_PORT', 9999)

        self._server = ThreadingTCPServer((host, port), IotpTCPHandler)
        print "interface.TCP - started"
        th = threading.Thread(target=self._server.serve_forever)
        th.daemon = True
        th.start()
        self._thread = th
        print "interface.TCP - serving"

    def stop(self):
        self._server.shutdown()
        print "interface.TCP - stopped"
