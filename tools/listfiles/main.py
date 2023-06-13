
import os

def run(parameters):

    # Load Parameters
    folder = parameters.get('folder')
    timeout = parameters.get('timeout', 60)
    
    # Logic Goes Here
    files = os.listdir(folder)
    
    # Return Status
    return files