
import json

#Example Plugin
def run(parameters):
    try:
        # Load Parameters
        filename = parameters.get('filename')
        content = parameters.get('content')
        
        # Logic Goes Here
        with open(filename, 'w') as file:
            json.dump(content, file)
        
        # Return Status
        return 'Task Complete'
    except Exception as e:
        return str(e)