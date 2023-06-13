import config
import traceback
from rabbit_comms import consume, publish
import subprocess
from tools import Tool, ToolRegistry

tool_registry = ToolRegistry()
firstscan = True

def initialise():
    tool_registry.load_tools()
    #setup base tools
    print(tool_registry.to_json())


def process_requests():
    """Process requests on the Rabbit tool channel

    Bots should request an index of known tools first
    GET_TOOLS()
    Returns: JSON Array of Tools (Names, Descriptions, parameters)
    """
    bot_channel, command, param = consume(config.TOOL_MANAGER_CHANNEL)
    #Test Command
    if bot_channel:
        try:
            if command:
                if command == 'GET_TOOLS':
                    #Respond with all available commands
                    # Convert tools to json string
                    tools_json = tool_registry.to_json()
                    publish(tools_json, bot_channel)
                    return

                if command == 'NEW_TOOL':
                    name = param.get('toolname').lower()
                    description = param.get('description')
                    parameters = param.get('parameters')
                    result = tool_registry.add_tool(name, description, parameters)
                    publish(result, bot_channel)
                    return

                if command == 'TEST_TOOL':
                    name = param.get('toolname').lower()
                    values = param.get('values', None)
                    result = tool_registry.test_tool(name, None, values)
                    publish(result, bot_channel)
                    return

                if command == 'EDIT_TOOL':
                    name = param.get('toolname').lower()
                    description = param.get('description')
                    parameters = param.get('parameters')
                    changes = param.get('changes')
                    feedback = param.get('feedback')
                    result = tool_registry.edit_tool(name, description, parameters, changes, feedback)
                    publish(result, bot_channel)
                    return

                if command == 'TUNE_TOOL':
                    name = param.get('toolname').lower()
                    feedback = param.get('feedback')
                    result = tool_registry.tune_tool(name, feedback)
                    publish(result, bot_channel)
                    return

                if command == 'START_TOOL':
                    toolname = param.get('toolname').lower()
                    result = tool_registry.start_tool(toolname, bot_channel)
                    publish(result, bot_channel)
                    return

                

                if command == 'STOP_TOOL':
                    toolname = param.get('toolname').lower()
                    result = tool_registry.stop_tool(bot_channel)
                    publish(result, bot_channel)
                    return
                
                if command == 'REMOVE_TOOL':
                    toolname = param.get('toolname').lower()
                    result = tool_registry.delete_tool(toolname, bot_channel)
                    publish(result, bot_channel)
                    return
                
                if param:
                    error = param.get('error')
                    if error:
                        #tool is broken, lets edit it
                        toolname = command
                        name = command
                        feedback = error
                        result = tool_registry.tune_tool(name, feedback)
                        publish(result, bot_channel)
        except Exception as e:
            traceback.print_exc()
            print( f"An exception occurred: {e}", bot_channel)


    
