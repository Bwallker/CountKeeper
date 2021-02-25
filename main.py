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
BOT_ID = configData['BOT_ID']
MOD_ID = configData['MOD_ID']
SPONSOR_ID = configData['SPONSOR_ID']
OG_ID = configData['OG_ID']
MEMBER_ID = configData['MEMBER_ID']
TOTAL_CHANNEL_ID = configData['TOTAL_CHANNEL_ID']
BOT_CHANNEL_ID = configData['BOT_CHANNEL_ID']
MOD_CHANNEL_ID = configData['MOD_CHANNEL_ID']
SPONSOR_CHANNEL_ID = configData['SPONSOR_CHANNEL_ID']
OG_CHANNEL_ID = configData['OG_CHANNEL_ID']
MEMBER_CHANNEL_ID = configData['MEMBER_CHANNEL_ID']
ROLELESS_CHANNEL_ID = configData['ROLELESS_CHANNEL_ID']
intents = discord.Intents.default()
intents.members = True
intents.presences = True
bot = commands.Bot(command_prefix=PREFIX, intents=intents)
TOTAL_CHANNEL = None
BOT_CHANNEL = None
MOD_CHANNEL = None
SPONSOR_CHANNEL = None
OG_CHANNEL = None
MEMBER_CHANNEL = None
ROLELESS_CHANNEL = None
GUILD = None


@bot.event
async def on_ready():
    global GUILD, TOTAL_CHANNEL, TOTAL_CHANNEL_ID, BOT_CHANNEL, BOT_CHANNEL_ID, MOD_CHANNEL, MOD_CHANNEL_ID, SPONSOR_CHANNEL, SPONSOR_CHANNEL_ID, OG_CHANNEL, OG_CHANNEL_ID, MEMBER_CHANNEL, MEMBER_CHANNEL_ID, ROLELESS_CHANNEL, ROLELESS_CHANNEL_ID
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
        if channel.id == TOTAL_CHANNEL_ID:
            TOTAL_CHANNEL = channel
            print(TOTAL_CHANNEL)
        elif channel.id == BOT_CHANNEL_ID:
            BOT_CHANNEL = channel
            print(BOT_CHANNEL)
        elif channel.id == MOD_CHANNEL_ID:
            MOD_CHANNEL = channel
            print(MOD_CHANNEL)
        elif channel.id == SPONSOR_CHANNEL_ID:
            SPONSOR_CHANNEL = channel
            print(SPONSOR_CHANNEL)
        elif channel.id == OG_CHANNEL_ID:
            OG_CHANNEL = channel
            print(OG_CHANNEL)
        elif channel.id == MEMBER_CHANNEL_ID:
            MEMBER_CHANNEL = channel
            print(MEMBER_CHANNEL)
        elif channel.id == ROLELESS_CHANNEL_ID:
            ROLELESS_CHANNEL = channel
            print(ROLELESS_CHANNEL)



    print(f'{bot.user} has connected to Discord!')
    print(f'Server name is {guild.name} and id is {guild.id}')
    print('Standing by')

def calculateChannels(member, mode, ctx):
    global GUILD, TOTAL_CHANNEL, BOT_CHANNEL, MOD_CHANNEL, SPONSOR_CHANNEL, OG_CHANNEL, MEMBER_CHANNEL, ROLELESS_CHANNEL
    print("entered calculate channels func")
    if (mode == "member left"):
        print(f'{member} left the server!')

    elif (mode == "member joined"):
        print(f'{member} joined the server!')

    elif (mode == "forced update"):
        print('Forced update commencing')

    elif (mode == "role changed"):
        print(f'{member} updated a role')

    elif (mode == "startup"):
        print("initializing channels")
    print('updating channels...')
    allMembers = GUILD.member_count
    botAmount = 0
    modAmount = 0
    sponsorAmount = 0
    ogAmount = 0
    memberAmount = 0


    print(f'All members: {allMembers}')
    for member in GUILD.members:
        for role in member.roles:
            if role.id == BOT_ID:
                botAmount += 1
            if role.id == MOD_ID:
                modAmount += 1
            if role.id == SPONSOR_ID:
                sponsorAmount += 1
            if role.id == OG_ID:
                ogAmount += 1
            if role.id == MEMBER_ID:
                memberAmount += 1
    print(f'Bots: {botAmount}')
    print(f'Mods: {modAmount}')
    print(f'Sponsors: {sponsorAmount}')
    print(f'Ogs: {ogAmount}')
    print(f'Members: {memberAmount}')

    roleLessAmount = allMembers - memberAmount - botAmount
    print(f'Roleless: {roleLessAmount}')
    totalTemp = "Alla användare: " + str(allMembers)
    botTemp = "Bottar: " + str(botAmount)
    modTemp = "Moderatorer: " + str(modAmount)
    sponsorTemp = "Sponsorer: " + str(sponsorAmount)
    ogTemp = "OGn :" + str(ogAmount)
    memberTemp = "Medlemmar: " + str(memberAmount)
    roleLessTemp = "Utan roller: " + str(roleLessAmount)
    returnArray = [totalTemp, botTemp, modTemp, sponsorTemp, ogTemp, memberTemp, roleLessTemp]
    return returnArray


@bot.event
async def on_member_update(before, after):
    global TOTAL_CHANNEL, BOT_CHANNEL, MOD_CHANNEL, SPONSOR_CHANNEL, OG_CHANNEL, MEMBER_CHANNEL, ROLELESS_CHANNEL
    if (before.roles != after.roles):
        returnArray = calculateChannels(after, "role changed", None)
        totalTemp = returnArray[0]
        botTemp = returnArray[1]
        modTemp = returnArray[2]
        sponsorTemp = returnArray[3]
        ogTemp = returnArray[4]
        memberTemp = returnArray[5]
        roleLessTemp = returnArray[6]
        await TOTAL_CHANNEL.edit(name=totalTemp)
        await BOT_CHANNEL.edit(name=botTemp)
        await MOD_CHANNEL.edit(name=modTemp)
        await SPONSOR_CHANNEL.edit(name=sponsorTemp)
        await OG_CHANNEL.edit(name=ogTemp)
        await MEMBER_CHANNEL.edit(name=memberTemp)
        await ROLELESS_CHANNEL.edit(name=roleLessTemp)
        print ("Channels updated!")
@bot.event
async def on_member_join(member):
    global TOTAL_CHANNEL, BOT_CHANNEL, MOD_CHANNEL, SPONSOR_CHANNEL, OG_CHANNEL, MEMBER_CHANNEL, ROLELESS_CHANNEL
    returnArray = calculateChannels(member, "member joined", None)
    totalTemp = returnArray[0]
    botTemp = returnArray[1]
    modTemp = returnArray[2]
    sponsorTemp = returnArray[3]
    ogTemp = returnArray[4]
    memberTemp = returnArray[5]
    roleLessTemp = returnArray[6]
    await TOTAL_CHANNEL.edit(name=totalTemp)
    await BOT_CHANNEL.edit(name=botTemp)
    await MOD_CHANNEL.edit(name=modTemp)
    await SPONSOR_CHANNEL.edit(name=sponsorTemp)
    await OG_CHANNEL.edit(name=ogTemp)
    await MEMBER_CHANNEL.edit(name=memberTemp)
    await ROLELESS_CHANNEL.edit(name=roleLessTemp)
    print ("Channels updated!")
@bot.event
async def on_member_remove(member):
    global TOTAL_CHANNEL, BOT_CHANNEL, MOD_CHANNEL, SPONSOR_CHANNEL, OG_CHANNEL, MEMBER_CHANNEL, ROLELESS_CHANNEL
    returnArray = calculateChannels(member, "member left", None)
    totalTemp = returnArray[0]
    botTemp = returnArray[1]
    modTemp = returnArray[2]
    sponsorTemp = returnArray[3]
    ogTemp = returnArray[4]
    memberTemp = returnArray[5]
    roleLessTemp = returnArray[6]
    await TOTAL_CHANNEL.edit(name=totalTemp)
    await BOT_CHANNEL.edit(name=botTemp)
    await MOD_CHANNEL.edit(name=modTemp)
    await SPONSOR_CHANNEL.edit(name=sponsorTemp)
    await OG_CHANNEL.edit(name=ogTemp)
    await MEMBER_CHANNEL.edit(name=memberTemp)
    await ROLELESS_CHANNEL.edit(name=roleLessTemp)
    print ("Channels updated!")

@bot.command(name='forceUpdate',help='Forces an update to channel names')
async def forceUpdate(ctx):
    global TOTAL_CHANNEL, BOT_CHANNEL, MOD_CHANNEL, SPONSOR_CHANNEL, OG_CHANNEL, MEMBER_CHANNEL, ROLELESS_CHANNEL
    returnArray = calculateChannels(None, "forced update", ctx)
    totalTemp = returnArray[0]
    botTemp = returnArray[1]
    modTemp = returnArray[2]
    sponsorTemp = returnArray[3]
    ogTemp = returnArray[4]
    memberTemp = returnArray[5]
    roleLessTemp = returnArray[6]
    await TOTAL_CHANNEL.edit(name=totalTemp)
    await BOT_CHANNEL.edit(name=botTemp)
    await MOD_CHANNEL.edit(name=modTemp)
    await SPONSOR_CHANNEL.edit(name=sponsorTemp)
    await OG_CHANNEL.edit(name=ogTemp)
    await MEMBER_CHANNEL.edit(name=memberTemp)
    await ROLELESS_CHANNEL.edit(name=roleLessTemp)
    await ctx.send("Channels updated!")
    print ("Channels updated!")
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
    json_content["PREFIX"] = args
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
