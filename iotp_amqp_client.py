__author__ = 'frza'

import pika
import uuid
import msgpack


class IotpAmqpClient(object):
    def __init__(self, host, rk):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))

        self._rk = rk
        self.response = None

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(self.on_response, no_ack=True,
                                   queue=self.callback_queue)

    def on_response(self, _ch, _method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def _call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(exchange='',
                                   routing_key=self._rk,
                                   properties=pika.BasicProperties(
                                       reply_to=self.callback_queue,
                                       correlation_id=self.corr_id),
                                   body=msgpack.packb(n))
        while self.response is None:
            self.connection.process_data_events()
        return msgpack.unpackb(self.response)

    def send_img_job(self, image_contents):
        return self._call({'type': 'image', 'image_file': image_contents})

    def send_simpletext_job(self, text):
        return self._call({'type': 'simple_text', 'text': text})

    def query_job_state(self, job_id):
        return self._call({'type': 'query_job_state', 'job_id': job_id})
