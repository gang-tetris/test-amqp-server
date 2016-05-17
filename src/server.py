#!/usr/bin/env python
from pika import BlockingConnection, ConnectionParameters
from .client import PersonRpcClient
from pika import BasicProperties
import json

DEFAULT_QUEUE = 'rpc_queue'
DEFAULT_HOST = 'rabbit'

class Server(object):
    def __init__(self, hostname):
        self.__hostname = hostname
        self.connect()


    def connect(self):
        self.connection = BlockingConnection(
                          ConnectionParameters(host=DEFAULT_HOST))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=DEFAULT_QUEUE)
        self.channel.basic_qos(prefetch_count=1)
        self.client = PersonRpcClient()
        self.channel.basic_consume(self.on_request, queue=DEFAULT_QUEUE)

        print(" [x] Awaiting RPC requests")
        self.channel.start_consuming()


    def on_request(self, ch, method, props, body):
        body = json.loads(body.decode('utf-8'))

        try:
            name = body['name']
            operation = body['op']
            if operation == 'insert':
                age = body['age']
        except Exception as e:
            response = {
                'success': False,
                'error': {
                    'status': 400,
                    'message': 'Invalid request "{}"'.format(body)
                }
            }
            self.respond(ch, props, method.delivery_tag, response)

        print("{}: {}; {}".format(method, props, body))

        if operation == 'select':
            response = self.select(name)
        elif operation == 'insert':
            response = self.insert(name, age)

        self.respond(ch, props, method.delivery_tag, response)


    def respond(self, ch, props, delivery_tag, response):
        properties = BasicProperties(correlation_id=props.correlation_id)
        ch.basic_publish(exchange='', routing_key=props.reply_to,
                         properties=properties,
                         body=json.dumps(response))
        ch.basic_ack(delivery_tag=delivery_tag)

    def select(self, name):
        response = json.loads(self.client.call(json.dumps({
            'op': 'select',
            'name': name
        })).decode('utf-8'))
        if 'response' not in response:
            response['response'] = {}
        response['response']['logic'] = self.__hostname
        return response


    def insert(self, name, age):
        response = json.loads(self.client.call(json.dumps({
            'op': 'insert',
            'name': name,
            'age': age
        })).decode('utf-8'))
        if 'response' not in response:
            response['response'] = {}
        response['response']['logic'] = self.__hostname
        return response

