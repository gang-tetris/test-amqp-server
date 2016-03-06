from pika import BasicProperties

def on_request(ch, method, props, body):
    name = str(body)

    print(" [.] Greet %s"%name)

    response = 'Hi {name}'.format(name=name)
    properties = BasicProperties(correlation_id = props.correlation_id)

    ch.basic_publish(exchange='', routing_key=props.reply_to,
                     properties=properties,
                     body=response)
    ch.basic_ack(delivery_tag = method.delivery_tag)

