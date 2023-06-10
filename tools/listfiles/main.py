
#Altered Plugin
def run(parameters):
    try:
        # Load Parameters
        folder = parameters.get('folder')
        
        # Logic Goes Here
        files = os.listdir(folder)
        
        # Return Status
        return files
    except Exception as e:
        return str(e)