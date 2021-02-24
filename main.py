# bot.py
import json
import discord
from discord.ext import commands
with open ("config.json") as json_config_file:
    configData = json.load(json_config_file)
    print("Config file read")
    json_config_file.close()
TOKEN = configData['BOT_TOKEN']
GUILD_ID = configData['GUILD_ID']
PREFIX = configData['PREFIX']
PLEB_ID = configData['ROLE1_ID']
BOT_ID = configData['ROLE2_ID']
BOT_CHANNEL_ID = configData['BOT_CHANNEL_ID']
PLEB_CHANNEL_ID = configData['PLEB_CHANNEL_ID']
ROLELESS_CHANNEL_ID = configData['ROLELESS_CHANNEL_ID']
intents = discord.Intents.default()
intents.members = True
intents.presences = True
bot = commands.Bot(command_prefix=PREFIX, intents=intents)
BOT_CHANNEL = None
PLEB_CHANNEL = None
ROLELESS_CHANNEL = None
GUILD = None


@bot.event
async def on_ready():
    global GUILD, BOT_CHANNEL, BOT_CHANNEL_ID, PLEB_CHANNEL, PLEB_CHANNEL_ID, ROLELESS_CHANNEL, ROLELESS_CHANNEL_ID
    with open("variables.json", 'r') as jsonfile:
        variablesJson = json.load(jsonfile)
        jsonfile.close()
    with open("config.json", 'r') as jsonfile:
        configJson = json.load(jsonfile)
        jsonfile.close()
    variablesJson["PREFIX"] = configJson["PREFIX"]
    PATH_TO_JSON = "variables.json"
    with open (PATH_TO_JSON, 'w') as json_variable_file:
        json.dump(variablesJson, json_variable_file, indent=4)
        json_variable_file.close()
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

async def calculateChannels(member, mode, ctx):
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
    await BOT_CHANNEL.edit(name=botTemp)
    await PLEB_CHANNEL.edit(name=plebTemp)
    await ROLELESS_CHANNEL.edit(name=roleLessTemp)
    if (mode == "forced update"):
        await ctx.send("Channels updated!")
    print ("Channels updated!")



async def on_member_join(member):
    calculateChannels(member, "member joined", None)

async def on_member_remove(member):
    calculateChannels(member, "member left", None)

@bot.command(name='forceUpdate',help='Forces an update to channel names')
async def forceUpdate(ctx):
    calculateChannels(None, "forced update", ctx)

@bot.command(name='listMembers')
async def listMembers(ctx):
    global GUILD
    GUILD.fetch_members()
    for member in GUILD.members:
        await ctx.send(member)
        print(member)
@bot.command(name='prefix', help='Changes the bots prefix')
async def prefixChange(ctx, args):
    args = str(args)
    PATH_TO_JSON = "variables.json"
    with open(PATH_TO_JSON, 'r') as jsonfile:
        json_content = json.load(jsonfile)
        jsonfile.close()
    json_content["PREFIX"] = str(args)
    with open (PATH_TO_JSON, 'w') as json_variable_file:
        json.dump(json_content, json_variable_file, indent=4)
        json_variable_file.close()
    bot.command_prefix = args
    print(f"prefix updated to {args}")
    message = "Prefix changed to " + args
    await ctx.send(message)
@prefixChange.error
async def prefixHelp(ctx, args):
    prefix = None
    with open ("variables.json", 'r') as json_variable_file:
        variableData = json.load(json_variable_file)
        prefix = variableData["PREFIX"]
        print("prefix retrieved")
        json_variable_file.close()

    answer = "To change prefix, you must supply a new prefix as an argument.\nThe command call should look like \"stat/prefix !\",\nasuming your current prefix is /stat and you want to change it to !\n\n Your current prefix is \"" + prefix + "\""
    await  ctx.send(answer)


bot.run(TOKEN)
