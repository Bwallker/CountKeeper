import json
def load():
    with open("CountKeeperData/config.json") as json_config_file:
        config_data = json.load(json_config_file)
        for key, value in config_data.items():
            globals()[key] = value
        print("Config file read")
    json_config_file.close()
load()