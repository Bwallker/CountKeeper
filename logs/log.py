from utils import std
import os
cwd = os.getcwd()
path_to_log_files = f'{cwd}/CountKeeperData/logs'
    
def print(message: str):
    log(message)
    std.print(message)



def log(message: str):
    global path_to_log_files
    with open(f'{path_to_log_files}/latest.log', 'a') as latest_log:
        latest_log.write(f'{message}\n')
        