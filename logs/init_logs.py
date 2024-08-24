"""
from utils import config
from utils import std
from os.path import join, isfile
import os
from datetime import timezone
import datetime
start_time: datetime = datetime.datetime.now()
print(start_time)
# Here we are getting a timestamp right at the start of execution, so it is as accurate as possible
cwd = os.getcwd()
PATH_TO_LOG_FILES = f'{cwd}/count_keeper_data/logs'
PATH_TO_LAST_RUN_TIME = f'{PATH_TO_LOG_FILES}/util_files/last_run_time.txt'


def set_last_time(last_time: str) -> None:
    global PATH_TO_LAST_RUN_TIME
    with open(PATH_TO_LAST_RUN_TIME, 'w') as last_run_time_file:
        last_run_time_file.write(last_time)


def get_last_time() -> str:
    global PATH_TO_LAST_RUN_TIME
    with open(PATH_TO_LAST_RUN_TIME, 'r') as last_run_time_file:
        last_run_time = last_run_time_file.read()
    return last_run_time


def init():
    print("Entered logs.init")
    global start_time
    last_time = get_last_time()
    print(last_time)
    # Rename latest log to its permanent name, that is the time the bot started for that particular run
    latest_log = f'{PATH_TO_LOG_FILES}/latest.log'
    renamed_latest_log = f'{PATH_TO_LOG_FILES}/{last_time}.log'
    os.rename(latest_log, renamed_latest_log)
    start_time_str = make_start_time_file_name_friendly(start_time)
    print(start_time_str)
    set_last_time(start_time_str)
    log_files = get_log_files()
    delete_oldest_log(config.LOG_LIMIT, log_files)


def get_log_files() -> list[str]:
    global PATH_TO_LOG_FILES
    files: list[str] = []
    for file in os.listdir(PATH_TO_LOG_FILES):
        if isfile(join(PATH_TO_LOG_FILES, file)):
            files.append(file)
    return files


def delete_oldest_log(limit: int, log_files: list[str]) -> None:
    global PATH_TO_LOG_FILES
    if len(log_files) < limit:
        return
    datetimes: list[datetime.datetime] = []

    for file in log_files:
        file = file[:-4]
        format = "%Y-%m-%d %H-%M-%S"
        try:
            datetime_object = datetime.datetime.strptime(file, format)
            datetimes.append(datetime_object)
        except ValueError as e:
            print(f'{datetime_object} is not a valid datetime. Ignoring')

    datetimes.sort()
    dt: datetime.datetime
    i: int = 0
    length: int = len(datetimes)
    while length > limit:
        dt: datetime = datetimes[i]
        datetime_str: str = str(dt)
        datetime_str = make_start_time_file_name_friendly(datetime_str)
        datetime_str += ".log"

        print(datetime_str)
        os.remove(f'{PATH_TO_LOG_FILES}/{datetime_str}')
        i += 1
        length -= 1


def make_start_time_file_name_friendly(start_time: datetime) -> str:
    start_time_str = str(start_time)
    start_time_str = start_time_str.split(".")[0]
    new_start_time = ""
    for character in start_time_str:
        if(character == ':'):
            new_start_time += '-'
        else:
            new_start_time += character
    return new_start_time
"""
