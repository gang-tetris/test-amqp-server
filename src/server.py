#!/usr/bin/env python
from pika import BlockingConnection, ConnectionParameters
from .remote_greeting import on_request
from .client import PersonRpcClient

DEFAULT_QUEUE = 'rpc_queue'
DEFAULT_HOST = 'rabbit'

connection = BlockingConnection(ConnectionParameters(host=DEFAULT_HOST))

channel = connection.channel()

channel.queue_declare(queue=DEFAULT_QUEUE)

channel.basic_qos(prefetch_count=1)

client = PersonRpcClient(connection)
def on_request_wrapper(ch, method, props, body):
    return on_request(client, ch, method, props, body)

channel.basic_consume(on_request_wrapper, queue=DEFAULT_QUEUE)

print(" [x] Awaiting RPC requests")
channel.start_consuming()

