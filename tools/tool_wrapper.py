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
    #subprocess.run("pip install pipreqs")
    #os.chdir(f"tools/{tool_name}")
    
    subprocess.run(['pipreqs', f'tools/{tool_name}', '--force'])
    print (f"pip install -r requirements.txt")
    subprocess.run(['pip', 'install', '-r',  f'tools/{tool_name}/requirements.txt'])
    


    notify_manager(tool_name, {'state': 'start'})
    notify_bot({'state': 'start'},out_chnl)
    #Listen to channel
    while True:
        parameters = consume(inp_chnl)
        if parameters:
            try:
                pkg = importlib.import_module(f'{tool_name}.main')
                result = pkg.run(parameters)
            except Exception as e:
                # Handle the error
                print(e)
                error_message = str(e)
                notify_bot({'result': error_message}, out_chnl)
                notify_manager(tool_name, {'state': 'error', 'error': error_message})
            else:
                # This block will be executed if no exception was thrown
                notify_bot({'result': result}, out_chnl)
                notify_bot({'state': 'finish'}, out_chnl)
                notify_manager(tool_name, {'state': 'finish'})
                break  
        time.sleep(0.5)
    

    