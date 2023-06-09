import json

#Example Plugin
def run(parameters):
    try:
        # Logic goes here
        x = parameters.get('x')
        y = parameters.get('y')
        
        # Instead of multiplying, write parameters to a file
        with open('parameters.txt', 'w') as file:
            file.write(f'x = {x}, y = {y}\n')
        
        # Optionally, you can also save them in JSON format
        with open('parameters.json', 'w') as file:
            json.dump(parameters, file)
            return x*y
    except Exception as e:
        return e 