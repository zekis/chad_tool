from rabbitmq_comms import publish, consume, notify_manager
import argparse
import importlib

if __name__ == "__main__":
    par = argparse.ArgumentParser(description="Tool")
    par.add_argument("name", type=str)
    par.add_argument("inp_chnl", type=str)
    par.add_argument("out_chnl", type=str)
    args = par.parse_args()
    
    inp_chnl = args.inp_chnl
    out_chnl = args.out_chnl
    tool_name = args.name

    notify_manager(tool_name, {'state': 'start'})
    #Listen to channel
    while True:
        parameters = consume(inp_chnl)
        if parameters:
            pkg = importlib.import_module(f'{tool_name}.main') 
            result = pkg.run(parameters)
            break

    #Publish to channel
    publish(result,out_chnl)
    notify_manager(tool_name, {'state': 'finish'})

    