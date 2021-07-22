import json
from logs.log import print
def load():
    with open("count_keeper_data/tests_config.json") as json_tests_config_file:
        config_tests_data = json.load(json_tests_config_file)
    for key, value in config_tests_data.items():
        globals()[key] = value
    print("tests_config.json file read")
load()