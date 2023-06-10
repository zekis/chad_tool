import json
import pika
import traceback

def notify_manager(toolname, parameters):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    manager = connection.channel()
    manager.queue_declare(queue="TOOL_CHANNEL")
    message = encode_manager_message(toolname, parameters)

    manager.basic_publish(exchange='',
                      routing_key="TOOL_CHANNEL",
                      body=message)
    #print(message)
    manager.close()
    


#Consume bot messages
def consume(channel):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    tool_channel = connection.channel()
    tool_channel.queue_declare(queue=channel)
    method, properties, body = tool_channel.basic_get(queue=channel, auto_ack=True)
    tool_channel.close()

    if body:
        parameters = decode_message(body)
        print(f"Parameters: {parameters}")
        return parameters
    else:
        return None

def decode_message(message):
    try:
        message = message.decode("utf-8")
        print(f"TOOL - DECODING: {message}")
        message_dict = json.loads(message)

        parameters = message_dict.get('parameters')
        
        return parameters
    except Exception as e:
        traceback.print_exc()
        return "prompt", f"error: {e}", None

def notify_bot(message, channel):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    message = encode_message(message)
    publish_channel = connection.channel()
    publish_channel.basic_publish(exchange='',
                      routing_key=channel,
                      body=message)
    #print(message)
    publish_channel.close()

def encode_message(message):
    #actions = [action.__dict__ for action in actions] if actions else []
    response = {
        "message": message
    }
    print(f"TOOL - ENCODING: {response}")
    return json.dumps(response)


def encode_manager_message(command, parameters):
    #actions = [action.__dict__ for action in actions] if actions else []
    response = {
        "command": command,
        "parameters": parameters
    }
    print(f"TOOL - ENCODING: {response}")
    return json.dumps(response)