
import json

#Example Plugin
def run(parameters):
    try:
        # Load Parameters
        api_key_id = parameters.get('api_key_id')
        api_secret = parameters.get('api_secret')
        url = parameters.get('url')
        
        # Logic Goes Here
        data = {
            'api_key_id': api_key_id,
            'api_secret': api_secret,
            'url': url
        }
        with open('data.json', 'w') as file:
            json.dump(data, file)
        
        # Return Status
        return 'Task Complete'
    except Exception as e:
        return str(e)