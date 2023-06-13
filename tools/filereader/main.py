
#Example Plugin
import os

def run(parameters):
    # Load Parameters
    filename = parameters.get('filename')
    
    # Logic Goes Here
    with open(filename, 'r') as file:
        content = file.read()
    
    # Return Status
    return content