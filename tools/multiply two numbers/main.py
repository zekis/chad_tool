
#Altered Plugin
def run(parameters):
        # Load Parameters
        num1 = parameters.get('num1')
        num2 = parameters.get('num2')
        
        # Logic Goes Here
        result = num1 * num2
        
        # Return Status
        return result
