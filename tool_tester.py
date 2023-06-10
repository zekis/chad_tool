import config
import traceback
import json
import pika
import time
import shutil
import os
from tool_builder import ai_new_tool, ai_edit_tool, ai_review_response, ai_suggest_test_parameters

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
    print(f"TESTER - ENCODING: {response}")
    return json.dumps(response)

def encode_tool_message(parameters):
    #actions = [action.__dict__ for action in actions] if actions else []
    response = {
        "parameters": parameters
    }
    print(f"TESTER - ENCODING: {response}")
    return json.dumps(response)

#Consume tool messages
def consume(channel):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    tool_channel = connection.channel()
    tool_channel.queue_declare(queue=channel)
    method, properties, body = tool_channel.basic_get(queue=channel, auto_ack=True)
    tool_channel.close()
    if body:
        message = decode_message(body)
        return message
    else:
        return None

def decode_message(message):
    try:
        message = message.decode("utf-8")
        print(f"DECODING: {message}")
        message_dict = json.loads(message)

        message = message_dict.get('message')
        return message
    except Exception as e:
        traceback.print_exc()



def ai_test_tool(toolname, description, parameters, feedback=None):
        bot_channel = "test"
        
        command_channel = f"CMD:{toolname}:{bot_channel}"
        response_channel = f"RES:{toolname}:{bot_channel}"

        file_path = f"tools/{toolname}/main.py"
        print(f'Testing {file_path}')
        if os.path.exists(file_path):
            # Logic Goes Here
            with open(file_path, 'r') as file:
                original = file.read()
        else:
            return "Failed"
        
        # Set the start time before entering the loop
        start_time = time.time()

        while True:
            #wait for tool to tell us it has started
            response = consume(response_channel)
            if response:
                state = response.get('state')
                if state=='start':
                    values = ai_suggest_test_parameters(original, toolname, description, parameters)
                    #parameters = {'folder': 'tools'}
                    publish_to_tool(command_channel, toolname, values)
                    
                    start_time = time.time()

                    while True:
                        response = consume(response_channel)
                        if response:
                            result = response.get('result')
                            if result:
                                review = ai_review_response(original, toolname, description, parameters, values, response, feedback)
                                print(review)
                                
                                test_result = review.get('test_result', None)
                                recommended_changes = review.get('recommended_changes', None)
                                if test_result == 'pass':
                                    return True
                                else:
                                    code = ai_edit_tool(original, toolname, description, parameters, recommended_changes, feedback)
                                    update_tool_code(toolname, code)
                                    return False
                        # Check if the elapsed time has exceeded 30 seconds
                        elapsed_time = time.time() - start_time
                        if elapsed_time > 30:
                            print("Timed out waiting for response.")
                            return False
            # Check if the elapsed time has exceeded 30 seconds
            elapsed_time = time.time() - start_time
            if elapsed_time > 30:
                print("Timed out waiting for tool to start.")
                return False

def update_tool_code(toolname, code):
    file_path = f"tools/{toolname}/main.py"
    backup_path = f"tools/{toolname}/main.bak"

    # Create a backup of the file
    shutil.copy(file_path, backup_path)

    with open(file_path, 'w') as file:
        file.write(code)


def roleback_tool_code(toolname):
    file_path = f"tools/{toolname}/main.py"
    backup_path = f"tools/{toolname}/main.bak"

    if os.path.exists(backup_path):
     # Copy the contents of the backup file back to the original file
        shutil.copy(backup_path, file_path)
