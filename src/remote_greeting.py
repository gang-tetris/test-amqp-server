from pika import BasicProperties
import json

def on_request(client, ch, method, props, body):
    name = body.decode('utf-8')

    print(" [.] Greet %s"%name)
    print("{}: {}; {}".format(method, props, body))

    #response = 'Hi {name}'.format(name=name)
    response = json.loads(client.call(json.dumps({
        'op': 'select',
        'name': name
    })).decode('utf-8'))
    if response['success']:
        response = {
            'success': True,
            'text': 'Hi {}'.format(response['person']['name'])
        }
    else:
        response = {
            'success': False
        }
    #response = '{"success": true}'
    properties = BasicProperties(correlation_id = props.correlation_id)

    ch.basic_publish(exchange='', routing_key=props.reply_to,
                     properties=properties,
                     body=json.dumps(response))
    ch.basic_ack(delivery_tag = method.delivery_tag)

