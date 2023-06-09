import json

# Example Plugin
def run(parameters):
    try:
        # Logic goes here
        filename = parameters.get('filename')

        # Read content from the file
        with open(filename, 'r') as file:
            content = file.read()

        return content
    except Exception as e:
        return str(e)
