
import json

#Example Plugin
def run(parameters):
    # Load Parameters
    filename = parameters.get('filename')
    content = parameters.get('content')
    
    # Logic Goes Here
    with open(filename, 'w') as file:
        file.write(content)
    
    # Return Status
    return 'Task Complete'
    