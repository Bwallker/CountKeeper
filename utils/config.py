import json
from logs.log import print
from os import getenv
def load_var(var_name: str, mapper = None) -> None:
    v = getenv(var_name)
    if mapper is not None:
        v = mapper(v)
    globals()[var_name] = v

def load():
    with open("count_keeper_data/config.json") as json_config_file:
        config_data = json.load(json_config_file)
    for key, value in config_data.items():
        globals()[key] = value
    print("Config file read")
load_var('LOG_LIMIT', int)
load_var('BOT_TOKEN')
load_var('DEFAULT_PREFIX')
load_var('BOT_WEBSITE')
load_var('BOT_NAME')
