import json
from logs.log import print
def load():
    with open("count_keeper_data/config.json") as json_config_file:
        config_data = json.load(json_config_file)
    for key, value in config_data.items():
        globals()[key] = value
    print("Config file read")
load()