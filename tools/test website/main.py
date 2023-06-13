
import json
import requests

#Example Plugin
def run(parameters):
    # Load Parameters
    url = parameters.get('url')
    
    # Logic Goes Here
    response = requests.get(url)
    if response.status_code == 200:
        return 'Website is responding'
    else:
        return 'Website is not responding'