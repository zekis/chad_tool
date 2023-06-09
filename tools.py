import json
import pickle
import subprocess
#example 
#File Writer
#
class Tool:
    def __init__(self, name, description, parameters, editable=False):
        self.name = name
        
        self.editable = editable
        self.description = description
        self.parameters = parameters
    
    def to_dict(self):
        return {
            'name': self.name,
            'description': self.description,
            'parameters': self.parameters
        }

class ToolRegistry:
    def __init__(self):
        self.tools = []
        self.user_processes = {}

    def add_tool(self, name, description, parameters):
        #Register tool
        for tool in self.tools:
            if tool.name == name:
                raise ValueError(f"A tool with the name '{name}' already exists.")

        self.tools.append(Tool(name, description, parameters))

        example_tool = "tools/filewriter.py"
        
    def start_tool(self, toolname, user_id):
        if user_id in self.user_processes and self.user_processes[user_id].poll() is None:
            return(f"Tool is already running for user {user_id}")
        else:
            command_channel = f"CMD:{user_id}"
            response_channel = f"RES:{user_id}"
            print(f"Starting process - tools/tool_wrapper.py  {toolname} {command_channel} {response_channel}")
            process = subprocess.Popen(['python', "tools/tool_wrapper.py", toolname, command_channel, response_channel ])
            self.user_processes[user_id] = process
            return(f"Tool started for user {user_id}")

    def stop_tool(self, user_id):
        if user_id in self.user_processes:
            self.user_processes[user_id].terminate()
            self.user_processes[user_id].wait()
            del self.user_processes[user_id]
            print(f"Ending process - tools/tool_wrapper.py")
            return(f"Tool stopped for user {user_id}")
        else:
            publish(f"No tool to stop for {user_id}")


    def save_tools(self, file_path):
        with open(file_path, 'wb') as f:
            pickle.dump(self.tools, f)

    def load_tools(self, file_path):
        with open(file_path, 'rb') as f:
            self.tools = pickle.load(f)

    def to_json(self):
        if not self.tools:
            return "No Tools Loaded, Use the ADD_TOOL tool to commission a new tool"
        else:
            return json.dumps([tool.to_dict() for tool in self.tools])

