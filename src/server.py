#!/usr/bin/env python
from pika import BlockingConnection, ConnectionParameters
from remote_greeting import on_request

DEFAULT_QUEUE = 'rpc_queue'
DEFAULT_HOST = 'rabbit'

connection = BlockingConnection(ConnectionParameters(host=DEFAULT_HOST))

channel = connection.channel()

channel.queue_declare(queue=DEFAULT_QUEUE)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(on_request, queue=DEFAULT_QUEUE)

print(" [x] Awaiting RPC requests")
channel.start_consuming()

