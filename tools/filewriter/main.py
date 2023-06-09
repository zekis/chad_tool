import json

#Example Plugin
def run(parameters):
    try:
        # Logic goes here
        filename = parameters.get('filename')
        content = parameters.get('content')
        
        # Instead of multiplying, write parameters to a file
        with open(filename, 'w') as file:
            file.write(content)
        
        # Optionally, you can also save them in JSON format
        return 'Task Complete'
    except Exception as e:
        return str(e)