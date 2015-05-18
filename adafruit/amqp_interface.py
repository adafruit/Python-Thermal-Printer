__author__ = 'frza'

from pika import BlockingConnection, ConnectionParameters, PlainCredentials, BasicProperties
from adafruit.iotp_pool import enqueue, job_state
from adafruit.iotp_pool_job import create_job
import msgpack
import threading
import time

err = msgpack.packb({'status': 'do_not_understand'})


def _on_request(ch, method, props, body):
    def send(m):
        ch.basic_publish(exchange='',
                         routing_key=props.reply_to,
                         properties=BasicProperties(correlation_id = \
                                                    props.correlation_id),
                         body=m)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def send_err():
        send(err)

    obj = msgpack.unpackb(body)
    try:
        if obj.get('type', None) is None:
            send_err()

        if obj['type'] == 'query_job_state':
            job_id = obj.get('job_id', 'foo')
            state = job_state(job_id)
            if state is False:
                rsp = {'query_state': 'job_not_found'}
            else:
                rsp = {'query_state': 'ok', 'job_id': job_id, 'job_state': state}
            send(msgpack.packb(rsp))
        else:
            j = create_job(obj)
            if j is not None:
                if enqueue(j):
                    rsp = msgpack.packb({'status': 'queued', 'job_id': str(j.id)})
                else:
                    rsp = msgpack.packb({'status': 'rejected', 'reason': 'queue_full', 'job_id': str(j.id)})
                send(rsp)
            else:
                send_err()
    except Exception as err:
        print "AMQP Exception: {}".format(err)
        send_err()


class IotpAMQPServer(object):
    def __init__(self, config):
        self._config = config
        self._conn = None
        self._chan = None
        self._thread = None

    def conf(self, item, defv):
        return self._config.get(item, defv)

    def start(self):
        conn_prms = ConnectionParameters(host=self.conf('AMQP_HOST', 'localhost'),
                                         port=self.conf('AMQP_PORT', 5672),
                                         credentials=PlainCredentials(username=self.conf('AMQP_USER', 'guest'),
                                                                      password=self.conf('AMQP_PASSWORD', 'guest')))
        self._conn = BlockingConnection(conn_prms)
        self._chan = self._conn.channel()

        queue_name = self.conf('AMQP_QUEUE_NAME', 'iotp_crocs_spooler')
        self._chan.queue_declare(queue=queue_name)
        self._chan.basic_qos(prefetch_count=1)
        self._chan.basic_consume(_on_request, queue=queue_name)

        print "interface.AMQP - started"
        self._thread = threading.Thread(target=self._chan.start_consuming)
        self._thread.daemon = True
        self._thread.start()
        print "interface.AMQP - serving"

    def stop(self):
        try:
            self._conn.close()
            while not self._conn.is_closed:
                time.sleep(1)
        except Exception:
            pass
        print "interface.AMQP - stopped"
