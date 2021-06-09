import json
from utils.tester import TESTER_TOKEN
with open("CountKeeperData/config.json") as json_config_file:
    configData = json.load(json_config_file)
    print("Config file read")
    json_config_file.close()


for key, value in configData.items():
    globals()[key] = value
