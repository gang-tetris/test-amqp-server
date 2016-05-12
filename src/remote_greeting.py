from pika import BasicProperties
import json

def on_request(client, ch, method, props, body):
    body = json.loads(body.decode('utf-8'))

    name = body['name']
    operation = body['op']

    print(" [.] Greet %s"%name)
    print("{}: {}; {}".format(method, props, body))

    if operation == 'select':
        response = json.loads(client.call(json.dumps({
            'op': operation,
            'name': name
        })).decode('utf-8'))
    elif operation == 'insert':
        age = body['age']
        response = json.loads(client.call(json.dumps({
            'op': operation,
            'name': name,
            'age': age
        })).decode('utf-8'))

    if response['success'] and operation == 'select':
        response = {
            'success': True,
            'text': 'Hi {}'.format(response['person']['name'])
        }

    properties = BasicProperties(correlation_id = props.correlation_id)

    ch.basic_publish(exchange='', routing_key=props.reply_to,
                     properties=properties,
                     body=json.dumps(response))
    ch.basic_ack(delivery_tag = method.delivery_tag)

