
import json

#Example Plugin
def run(parameters):
    try:
        # Load Parameters
        filename = parameters.get('filename')
        url = parameters.get('url')
        
        # Logic Goes Here
        with open(filename, 'r') as file:
            data = json.load(file)
            api_key = data[url]['api_key']
            api_secret = data[url]['api_secret']
        
        # Return Status
        return api_key, api_secret
    except Exception as e:
        return str(e)