
#Example Plugin
import os

def run(parameters):
    try:
        # Load Parameters
        filename = parameters.get('filename')
        
        # Logic Goes Here
        with open(filename, 'r') as file:
            content = file.read()
        
        # Return Status
        return content
    except Exception as e:
        return str(e)
