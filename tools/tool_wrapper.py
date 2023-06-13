from rabbitmq_comms import notify_bot, consume, notify_manager
import argparse
import importlib
import os
import json
import subprocess
import time

if __name__ == "__main__":
    par = argparse.ArgumentParser(description="Tool")
    par.add_argument("name", type=str)
    par.add_argument("inp_chnl", type=str)
    par.add_argument("out_chnl", type=str)
    args = par.parse_args()
    inp_chnl = args.inp_chnl
    out_chnl = args.out_chnl
    tool_name = args.name

    subprocess.run(['pip', 'install', 'pipreqs'])
    subprocess.run(['pipreqs', f'tools/{tool_name}', '--force'])
    print (f"pip install -r requirements.txt")
    subprocess.run(['pip', 'install', '-r',  f'tools/{tool_name}/requirements.txt'])
    
    notify_manager(tool_name, {'state': 'start'})
    notify_bot({'state': 'start'},out_chnl)
    #Listen to channel
    while True:
        parameters = consume(inp_chnl)
        if parameters:
            print(f"TOOL - Got Parameters {parameters}")
            if isinstance(parameters, dict):
                break
            else:
                error = f"Not a DICT: {parameters}"
                notify_bot({'result': error}, out_chnl)
                #notify_manager(tool_name, {'state': 'error', 'error': error})
        time.sleep(0.5)
    
    #Load Module
    try:
        print(f"TOOL - Loading {tool_name} - {parameters}")
        pkg = importlib.import_module(f'{tool_name}.main')
        

    except Exception as e:
        # Handle the error
        print(f"TOOL - Error loading tool {e}")
        error_message = str(e)
        notify_bot({'result': error_message}, out_chnl)
        notify_manager(tool_name, {'state': 'error', 'error': error_message})
        
    #Run Tool
    try:
        print(f"TOOL - Running {tool_name} - {parameters}")
        result = pkg.run(parameters)
        notify_bot({'result': result}, out_chnl)
    except Exception as e:
        # Handle the error
        print(f"TOOL - Error Running tool {e}")
        error_message = str(e)
        notify_bot({'result': error_message}, out_chnl)
        notify_manager(tool_name, {'state': 'error', 'error': error_message})
    
    #Notify
    notify_bot({'state': 'finish'}, out_chnl)
    notify_manager(tool_name, {'state': 'finish'})
        
            
        
    

    