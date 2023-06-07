import json
import pickle

class Tool:
    def __init__(self, name, description, instruction):
        self.name = name
        self.description = description
        self.Instruction = instruction
    
    def to_dict(self):
        return {
            'name': self.name,
            'description': self.description,
            'instructions': self.instructions
        }

class ToolRegistry:
    def __init__(self, name, description, instruction):
        self.tools = []

    def add_tool(self, name, description, instructions):
        self.tools.append(Tool(name, description, instructions))

    def save_tools(self, file_path):
        with open(file_path, 'wb') as f:
            pickle.dump(self.tools, f)

    def load_tools(self, file_path):
        with open(file_path, 'rb') as f:
            self.tools = pickle.load(f)

    def to_json(self):
        return json.dumps([tool.to_dict() for tool in self.tools])