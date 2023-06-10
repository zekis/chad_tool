import config
import json
import pika
import traceback


#Consume bot messages
def consume(channel):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    tool_channel = connection.channel()
    tool_channel.queue_declare(queue=channel)
    method, properties, body = tool_channel.basic_get(queue=channel, auto_ack=True)
    tool_channel.close()
    if body:
        bot_channel, command, parameters = decode_message(body)
        return bot_channel, command, parameters
    else:
        return None, None, None

def decode_message(message):
    try:
        message = message.decode("utf-8")
        print(f"MANAGER DECODING: {message}")
        message_dict = json.loads(message)

        bot_channel = message_dict.get('bot_channel')
        command = message_dict.get('command')
        parameters = message_dict.get('parameters')
        
        return bot_channel, command, parameters
    except Exception as e:
        traceback.print_exc()
        

def publish(message, channel):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    message = encode_message(message)
    publish_channel = connection.channel()
    publish_channel.basic_publish(exchange='',
                      routing_key=channel,
                      body=message)
    print(message)
    publish_channel.close()

def encode_message(message):
    #actions = [action.__dict__ for action in actions] if actions else []
    response = {
        "message": message
    }
    print(f"MANAGER ENCODING: {response}")
    return json.dumps(response)

