import config
import traceback
import json
import pika
import time

def publish_to_manager(bot_channel, command, parameters=None):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    message = encode_manager_message(bot_channel, command, parameters)

    publish_channel = connection.channel()
    publish_channel.basic_publish(exchange='',
                      routing_key=config.TOOL_MANAGER_CHANNEL,
                      body=message)
    #print(message)
    publish_channel.close()

def publish_to_tool(command_channel, bot_channel, toolname, parameters):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    message = encode_tool_message(parameters)

    publish_channel = connection.channel()
    publish_channel.basic_publish(exchange='',
                      routing_key=command_channel,
                      body=message)
    #print(message)
    publish_channel.close()


def encode_manager_message(bot_channel, command, parameters=None):
    #actions = [action.__dict__ for action in actions] if actions else []
    response = {
        "bot_channel": bot_channel,
        "command": command,
        "parameters": parameters
    }
    print(f"ENCODING: {response}")
    return json.dumps(response)

def encode_tool_message(parameters):
    #actions = [action.__dict__ for action in actions] if actions else []
    response = {
        "parameters": parameters
    }
    print(f"ENCODING: {response}")
    return json.dumps(response)

if __name__ == "__main__":
    bot_channel = "test"
    command_channel = f"CMD:{bot_channel}"
    response_channel = f"RES:{bot_channel}"
    
    
    command = "NEW_TOOL"
    parameters = {'toolname': 'filewriter', 'description': 'write content to a file', 'parameters': ['filename', 'content']}
    publish_to_manager(bot_channel, command, parameters)

    command = "GET_TOOLS"
    publish_to_manager(bot_channel, command)


    command = "START_TOOL"
    parameters = {'toolname': 'filewriter'}
    publish_to_manager(bot_channel, command, parameters)

    time.sleep(2)
    toolname = 'filewriter'
    parameters = {'filename': 'test.txt', 'content': 'hello world'}
    publish_to_tool(command_channel, response_channel, toolname, parameters)

    time.sleep(2)

    command = "STOP_TOOL"
    parameters = {'toolname': 'filewriter'}
    publish_to_manager(bot_channel, command, parameters)


