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

def publish_to_tool(command_channel, toolname, parameters):
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
    print(f"TESTER ENCODING: {response}")
    return json.dumps(response)

def encode_tool_message(parameters):
    #actions = [action.__dict__ for action in actions] if actions else []
    response = {
        "parameters": parameters
    }
    print(f"TESTER ENCODING: {response}")
    return json.dumps(response)

if __name__ == "__main__":
    bot_channel = "test"
    toolname = 'filewriter'
    command_channel = f"CMD:{toolname}:{bot_channel}"
    # response_channel = f"RES:{toolname}:{bot_channel}"
    
    # command = "NEW_TOOL"
    # toolname = 'filereader'
    # parameters = {'toolname': toolname, 'description': 'read content from a file', 'parameters': ['filename']}
    # publish_to_manager(bot_channel, command, parameters)

    # command = "NEW_TOOL"
    # toolname = 'filewriter'
    # parameters = {'toolname': toolname, 'description': 'write content to a file', 'parameters': ['filename', 'content']}
    # publish_to_manager(bot_channel, command, parameters)

    # command = "NEW_TOOL"
    # toolname = 'listfiles'
    # parameters = {'toolname': toolname, 'description': 'list the files in the specified folder', 'parameters': ['folder']}
    # publish_to_manager(bot_channel, command, parameters)
    # command = "TUNE_TOOL"
    # toolname = 'filewriter'
    # parameters = {'toolname': toolname, 'feedback': "successful test will return hello world from test.txt"}
    # publish_to_manager(bot_channel, command, parameters)


    command = "START_TOOL"
    
    parameters = {'toolname': toolname}
    publish_to_manager(bot_channel, command, parameters)

    # command = "GET_TOOLS"
    # publish_to_manager(bot_channel, command)


    # command = "START_TOOL"
    # parameters = {'toolname': toolname}
    # publish_to_manager(bot_channel, command, parameters)

    time.sleep(2)
    parameters = {'toolname': toolname, 'filename': "test1.txt", "content": "hello world1"}
    publish_to_tool(command_channel, toolname, parameters)

    # time.sleep(5)

    # command = "EDIT_TOOL"
    # changes = "import os"
    # parameters = {'toolname': toolname, 'description': 'list the files in the specified folder', 'parameters': ['folder'], 'changes': changes}
    # publish_to_manager(bot_channel, command, parameters)

    # time.sleep(10)
    # parameters = {'folder': 'tools'}
    # publish_to_tool(command_channel, toolname, parameters)

    # time.sleep(5)
    # command = "STOP_TOOL"
    # parameters = {'toolname': 'filereader'}
    # publish_to_manager(bot_channel, command, parameters)


