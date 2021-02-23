# bot.py
import json
import discord
with open ("config.json", "r") as json_config_file:
    configData = json.load(json_config_file)
    print("Config file read")
    json_config_file.close()
TOKEN = configData['BOT_TOKEN']
print("Printing config token")
print(TOKEN)
print("Printing whole config file")
print(configData)

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

client.run(TOKEN)
