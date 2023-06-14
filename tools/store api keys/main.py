
import json
import pickle

#Example Plugin
def run(parameters):
    try:
        # Load Parameters
        filename = parameters.get('filename', 'keys.pkl')
        data = parameters.get('data')
        
        # Logic Goes Here
        with open(filename, 'wb') as file:
            pickle.dump(data, file)
        
        # Return Status
        return 'API keys, secrets and URLs stored successfully'
    except Exception as e:
        print('An error occurred while attempting to store the API keys, secrets and URLs: {}'.format(e))
        return 'Task Failed'