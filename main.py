# bot.py
import json
import discord
from discord.ext import commands
with open ("config.json", "r") as json_config_file:
    configData = json.load(json_config_file)
    print("Config file read")
    json_config_file.close()
TOKEN = configData['BOT_TOKEN']
GUILD_ID = int(configData['GUILD_ID'])
PREFIX = configData['PREFIX']
PLEB_ID = int(configData['ROLE1_ID'])
BOT_ID = int(configData['ROLE2_ID'])
BOT_CHANNEL_ID = int(configData['BOT_CHANNEL_ID'])
PLEB_CHANNEL_ID = int(configData['PLEB_CHANNEL_ID'])
ROLELESS_CHANNEL_ID = int(configData['ROLELESS_CHANNEL_ID'])
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix=PREFIX, intents=intents)
BOT_CHANNEL = None
PLEB_CHANNEL = None
ROLELESS_CHANNEL = None
GUILD = None


@bot.event
async def on_ready():
    global GUILD, BOT_CHANNEL, BOT_CHANNEL_ID, PLEB_CHANNEL, PLEB_CHANNEL_ID, ROLELESS_CHANNEL, ROLELESS_CHANNEL_ID
    for guild in bot.guilds:
        if guild.id == GUILD_ID:
            GUILD = guild
            break
    for channel in guild.voice_channels:
        if channel.id == BOT_CHANNEL_ID:
            BOT_CHANNEL = channel
            print(BOT_CHANNEL)
        elif channel.id == PLEB_CHANNEL_ID:
            PLEB_CHANNEL = channel
            print(PLEB_CHANNEL)
        elif channel.id == ROLELESS_CHANNEL_ID:
            ROLELESS_CHANNEL = channel
            print(ROLELESS_CHANNEL)


    print(f'{bot.user} has connected to Discord!')
    print(f'Server name is {guild.name} and id is {guild.id}')
    print('Standing by')
def testFunc():
    global GUILD



def calculateChannels(member, mode):
    global GUILD, BOT_CHANNEL, PLEB_CHANNEL, ROLELESS_CHANNEL
    if (mode == "member left"):
        print(f'{member} left the server!')

    elif (mode == "member joined"):
        print(f'{member} joined the server!')

    elif (mode == "forced update"):
        print('Forced update commencing')

    print('updating channels...')
    plebAmount = 0
    botAmount = 0
    allMembers = GUILD.member_count
    print(f'All members: {allMembers}')
    for member in GUILD.members:
        for role in member.roles:
            if role.id == PLEB_ID:
                plebAmount += 1
            if role.id == BOT_ID:
                botAmount += 1
    print(f'Plebs: {plebAmount}')
    print(f'Bots: {botAmount}')
    roleLessAmount = allMembers - plebAmount - botAmount
    print(f'Roleless: {roleLessAmount}')
    botTemp = "Bottar: " + str(botAmount)
    plebTemp = "Pöblar: " + str(plebAmount)
    roleLessTemp = "Utan roller: " + str(roleLessAmount)
    returnArr = [botTemp, plebTemp, roleLessTemp]
    return returnArr



async def on_member_join(member):
    returnArr = calculateChannels(member, "member joined")
    botTemp = returnArr[0]
    plebtemp = returnArr[1]
    roleLessTemp = returnArr[2]
    await BOT_CHANNEL.edit(name=botTemp)
    await PLEB_CHANNEL.edit(name=plebTemp)
    await ROLELESS_CHANNEL.edit(name=roleLessTemp)
    print('Channels updated!')


async def on_member_remove(member):
    returnArr = calculateChannels(member, "member left")
    botTemp = returnArr[0]
    plebtemp = returnArr[1]
    roleLessTemp = returnArr[2]
    await BOT_CHANNEL.edit(name=botTemp)
    await PLEB_CHANNEL.edit(name=plebTemp)
    await ROLELESS_CHANNEL.edit(name=roleLessTemp)
    print('Channels updated!')

@bot.command(name='forceUpdate',help='Forces an update to channel names')
async def forceUpdate(ctx):
    returnArr = calculateChannels(None, "forced update")
    botTemp = returnArr[0]
    plebTemp = returnArr[1]
    roleLessTemp = returnArr[2]
    await BOT_CHANNEL.edit(name=botTemp)
    await PLEB_CHANNEL.edit(name=plebTemp)
    await ROLELESS_CHANNEL.edit(name=roleLessTemp)
    await ctx.send("Channels updated!")
    print('Channels updated!')
@bot.command(name='listMembers')
async def listMembers(ctx):
    global GUILD
    GUILD.fetch_members()
    for member in GUILD.members:
        await ctx.send(member)
        print(member)


bot.run(TOKEN)
