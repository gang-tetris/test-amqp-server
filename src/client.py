#!/usr/bin/env python
import pika
import uuid
from sys import argv
from json import dumps as stringify, loads as jsonify

DEFAULT_HOST = 'rabbit'
DEFAULT_CLIENT_QUEUE = 'java_queue'

class PersonRpcClient(object):
    def __init__(self):
        self.connect()

    def connect(self):
        self.connection = pika.BlockingConnection(
                          pika.ConnectionParameters(host=DEFAULT_HOST))
        self.channel = self.connection.channel()
        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(self.on_response, queue=self.callback_queue)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, person):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        if self.connection.is_closed:
            self.connect()

        self.channel.basic_publish(exchange='',
                                   routing_key=DEFAULT_CLIENT_QUEUE,
                                   properties=pika.BasicProperties(
                                         reply_to = self.callback_queue,
                                         correlation_id = self.corr_id,
                                         ),
                                   body=person)
        while self.response is None:
            self.connection.process_data_events()
        return self.response

if __name__ == '__main__':
    person_rpc = PersonRpcClient()

    print(" [x] Requesting {} person {} ({})".format(argv[1], argv[2], argv[3]))
    response = person_rpc.call(stringify({
        'op': argv[1],
        'name': argv[2],
        'age': int(argv[3])
    }))
    print(" [.] Got %r" % jsonify(response.decode("utf-8")))

