import discord
from utils import config
TESTER_TOKEN = config.TESTER_TOKEN

client = discord.Client

def getId():
    if TESTER_TOKEN == 0:
        client.close()
        print(0)
        return 0
    ID = client.user.id
    client.close()
    print(ID)
    return ID


ID = getId()



client.run(TESTER_TOKEN)