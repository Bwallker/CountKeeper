from utils import std
import os
cwd = os.getcwd()
PATH_TO_LOG_FILES = f'{cwd}/count_keeper_data/logs'
    
def print(message: str):
    log(message)
    std.print(message)


def log(message: str):
    global PATH_TO_LOG_FILES
    with open(f'{PATH_TO_LOG_FILES}/latest.log', 'a') as latest_log:
        latest_log.write(f'{message}\n')
        