import config
import traceback
from rabbit_comms import consume, publish
import subprocess
from tools import Tool, ToolRegistry

tool_registry = ToolRegistry()
firstscan = True

def initialise():
    tool_registry.load_tools(config.DATA_DIR)

def process_requests():
    """Process requests on the Rabbit tool channel

    Bots should request an index of known tools first
    GET_TOOLS()
    Returns: JSON Array of Tools (Names, Descriptions, parameters)
    """

    try:
        bot_channel, command, parameters = consume(config.TOOL_MANAGER_CHANNEL)
        #Test Command
        

        if command:
            if command == 'GET_TOOLS':
                #Respond with all available commands
                # Convert tools to json string
                tools_json = tool_registry.to_json()
                publish(tools_json, bot_channel)
                return

            if command == 'NEW_TOOL':
                name = parameters.get('toolname')
                description = parameters.get('description')
                parameters = parameters.get('parameters')
                result = tool_registry.add_tool(name, description, parameters)
                publish(result, bot_channel)
                return

            if command == 'START_TOOL':
                toolname = parameters.get('toolname')
                result = tool_registry.start_tool(toolname, bot_channel)
                publish(result, bot_channel)
                return

            if command == 'STOP_TOOL':
                parameters.get('toolname')
                result = tool_registry.stop_tool(bot_channel)
                publish(result, bot_channel)
                return
                    

    except Exception as e:
        traceback.print_exc()
        publish( f"An exception occurred: {e}", bot_channel)
