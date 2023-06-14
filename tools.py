import json
import pickle
import subprocess
import os
import config
import shutil
import time
from tool_builder import ai_new_tool, ai_edit_tool, ai_review_response, ai_suggest_test_parameters
from tool_tester import ai_test_tool, roleback_tool_code

#example 
#File Writer
template = """
import json

#Example Plugin
def run(parameters):
    try:
        # Load Parameters
        filename = parameters.get('filename')
        content = parameters.get('content')
        
        # Logic Goes Here
        with open(filename, 'w') as file:
            file.write(content)
        
        # Return Status
        return 'Task Complete'
    except Exception as e:
        return str(e)
"""
#
class Tool:
    def __init__(self, name, description, parameters, editable=False):
        self.name = name
        self.editable = editable
        self.description = description
        self.parameters = parameters
        self.test_result = False
        self.feedback = ""
    
    def to_dict(self):
        return {
            'name': self.name.lower(),
            'description': self.description,
            'parameters': self.parameters,
            'test_result': self.test_result
        }

class ToolRegistry:
    def __init__(self):
        self.tools = []
        self.user_processes = {}

    def cleanup(self):
        #if path doesnt exist. delete the tool
        #ensure tools are all lowercase
        for tool in self.tools:
            tool.name = tool.name.lower()
            folder_path = f"tools/{tool.name}"
            if not os.path.exists(folder_path):
                print(f"Deleting tool {tool.name}")
                self.delete_tool(tool.name)
                
        self.save_tools()

    def add_tool(self, name, description, parameters):
        #Register tool
        for tool in self.tools:
            if tool.name.lower() == name.lower():
                return(f"A tool with the name '{name}' already exists.")

        
        #if a tool is not registered then its path is fair game.
        folder_path = f"tools/{name.lower()}"
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)
            time.sleep(1)
        
        os.makedirs(folder_path)

        file_path = f"tools/{name.lower()}/main.py"
        # if os.path.exists(file_path):
        #     self.tools.append(Tool(name, description, parameters))
        #     self.save_tools()
            #raise ValueError(f"The file '{file_path}' already exists.")
        
        code = ai_new_tool(template, name.lower(), description, parameters)
        # Instead of multiplying, write parameters to a file
        with open(file_path, 'w') as file:
            file.write(code)

        self.tools.append(Tool(name.lower(), description, parameters))
        result = self.test_tool(name.lower())
        
        return f"'result': {result}, 'code': {code}"
        
    
    def test_tool(self, toolname, feedback=None, values=None):
        bot_channel = "test"
        for tool in self.tools:
            if tool.name.lower() == toolname.lower():
                count = 10
                while count > 0:
                    self.start_tool(tool.name.lower(), bot_channel)
                    test_result = ai_test_tool(tool.name.lower(), tool.description, tool.parameters, tool.feedback, values)
                    if test_result:
                        tool.test_result = True
                        self.save_tools()
                        return f"Tool test passed after {11 - count} attempts"
                    self.stop_tool(bot_channel)
                    count -= 1
                test_result = False
                roleback_tool_code(tool.name.lower())
                return "Tool test failed after 10 attempts"
        else:
            return "Tool not found"



    def edit_tool(self, name, description, parameters, changes, feedback):
        #Register tool
        for tool in self.tools:
            if tool.name.lower() == name.lower():
                #raise ValueError(f"A tool with the name '{name}' already exists.")
                tool.description = description
                tool.parameters = parameters
                tool.feedback = feedback
                #self.tools.append(Tool(name, description, parameters))

                folder_path = f"tools/{name.lower()}"
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)

                file_path = f"tools/{name.lower()}/main.py"
                
                if os.path.exists(file_path):
                    # Logic Goes Here
                    with open(file_path, 'r') as file:
                        content = file.read()

                    code = ai_edit_tool(content, name.lower(), description, parameters, changes, tool.feedback)
                    # Instead of multiplying, write parameters to a file
                    with open(file_path, 'w') as file:
                        file.write(code)
                        #return(f"{name.lower()} Tool Updated")
                    
                    result = self.test_tool(name.lower())
                    return f"'result': {result}, 'code': {code}"
                return "File not found"
        return "Tool not found"

    def tune_tool(self, name, feedback):
        #Register tool
        for tool in self.tools:
            if tool.name.lower() == name.lower():
                #raise ValueError(f"A tool with the name '{name}' already exists.")
                tool.feedback = feedback
                result = self.test_tool(name.lower(), feedback)
                return result
                #self.tools.append(Tool(name, description, parameters))
        return "Tool not found"

    def start_tool(self, toolname, user_id):
        if user_id in self.user_processes and self.user_processes[user_id].poll() is None:
            self.stop_tool(user_id)
            #return(f"Tool is already running for user {user_id}")
    
        command_channel = f"CMD:{toolname.lower()}:{user_id}"
        response_channel = f"RES:{toolname.lower()}:{user_id}"
        print(f"Starting process - tools/tool_wrapper.py   {toolname.lower()} {user_id} {command_channel} {response_channel}")
        process = subprocess.Popen(['python', "tools/tool_wrapper.py", toolname.lower(), user_id, command_channel, response_channel ])
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
            return(f"No tool to stop for {user_id}")

    def delete_tool(self, name, user_id=None):
        if user_id:
            self.stop_tool(user_id)
        # Iterate through the list of tools
        try:
            for tool in self.tools:
                # If the name matches, remove the tool from the list
                if tool.name.lower() == name.lower():
                    self.tools.remove(tool)
                    
                    folder_path = f"tools/{name.lower()}"
                    if os.path.exists(folder_path):
                        shutil.rmtree(folder_path)
                        return(f"Tool {name} removed.")
                    
            return(f"Tool {name} not found.")
        except Exception as e:
            return(f"Error deleting {name} error: {e}")

    def save_tools(self):
        file_path = f"{config.DATA_DIR}/tool_registry.pkl"
        with open(file_path, 'wb') as f:
            pickle.dump(self.tools, f)

    def load_tools(self):
        file_path = f"{config.DATA_DIR}/tool_registry.pkl"
        if os.path.exists(file_path):
            with open(file_path, 'rb') as f:
                self.tools = pickle.load(f)
        self.cleanup()
        

    def to_json(self):
        if not self.tools:
            return "No Tools Loaded, Use the ADD_TOOL tool to commission a new tool"
        else:
            return json.dumps([tool.to_dict() for tool in self.tools])

