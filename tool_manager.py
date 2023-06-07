from rabbit_comms import consume, publish
import subprocess
from tools import Tool, ToolRegistry

tool_registry = ToolRegistry()

def initialise():
    tool_registry.load_tools(config.DATA_DIR)

def process_requests():
    """Process requests on the Rabbit tool channel

    Bots should request an index of known tools first
    GET_TOOLS()
    Returns: JSON Array of Tools (Names, Descriptions, Instructions)
    """

    try:
        sender_channel, send_to_channel, command, parameters = consume(config.TOOL_CHANNEL)
        if command:
            if command == 'GET_TOOLS':
                #Respond with all available commands
                # Convert tools to json string
                tools_json = tool_registry.to_json()
                publish(tools_json, send_to_channel)
                return

            if command == 'START_TOOL':
                return

            if command == 'STOP_TOOL':
                return

            if command == 'EDIT_TOOL':
                return

    except Exception as e:
        traceback.print_exc()
        publish( f"An exception occurred: {e}")


class BotManager:
    def __init__(self):
        self.user_processes = {}

    def handle_command(self, command, parameters):
        if command.lower() == "start":
            return