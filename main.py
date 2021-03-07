# bot.py
import json
import sqlite3

import discord
from discord import channel as channelClass
from discord import guild as guildClass
from discord.errors import Forbidden
from discord.ext import commands, tasks

with open("config.json") as json_config_file:
    configData = json.load(json_config_file)
    print("Config file read")
    json_config_file.close()
TOKEN = configData["BOT_TOKEN"]
DEFAULT_PREFIX = configData["DEFAULT_PREFIX"]
intents = discord.Intents.default()
intents.members = True
intents.presences = True


def get_prefix(bot, message):
    prefixes = sqlite3.connect("prefixes.sqlite")
    cursor = prefixes.cursor()
    cursor.execute(f"SELECT prefix FROM prefixes WHERE guild_id = {message.guild.id}")
    result = cursor.fetchone()[0]
    cursor.close()
    prefixes.close()
    return result


bot = commands.Bot(command_prefix=get_prefix, intents=intents)


def getPrefix(guildId: int):
    try:
        prefixes = sqlite3.connect("prefixes.sqlite")
        cursor = prefixes.cursor()
        cursor.execute(f"SELECT prefix FROM prefixes WHERE guild_id = {guildId}")
        prefix = cursor.fetchone()
    except:
        prefix = None
    cursor.close()
    prefixes.close()

    if (prefix is None):
        return None
    prefix = prefix[0]
    return prefix

def addPrefix(guildId: int):
    global DEFAULT_PREFIX
    prefixes = sqlite3.connect("prefixes.sqlite")
    cursor = prefixes.cursor()
    cursor.execute(f"""INSERT INTO prefixes (guild_id, prefix) VALUES({guildId},{DEFAULT_PREFIX})""")
    prefixes.commit()
    cursor.close()
    prefixes.close()

def changePrefix(guildId: int, prefix):
    if (isinstance(prefix, int) is False and isinstance(prefix, str) is False):
        raise TypeError("prefix must be of type int or str")
    if (isinstance(prefix, int)):
        prefix = str(prefix)
    prefixes = sqlite3.connect("prefixes.sqlite")
    cursor = prefixes.cursor()
    cursor.execute(f"""UPDATE prefixes SET prefix = ? WHERE guild_id = ?""", (prefix, guildId))
    prefixes.commit()
    cursor.close()
    prefixes.close()

def getRole(channel: channelClass):
    guildId = channel.guild.id
    channels = sqlite3.connect("channels.sqlite")
    cursor = channels.cursor()
    cursor.execute(f"""SELECT role FROM channels WHERE channel_id = {channel.id}""")
    role = cursor.fetchone()
    if (role is None):
        return None
    role = role[0]
    return role

def addRole(channel: channelClass, role: str):
    guildId = channel.guild.id
    channels = sqlite3.connect("channels.sqlite")
    cursor = channels.cursor()
    cursor.execute(f"""INSERT INTO channels (guild_id, channel_id, role) VALUES(?,?,?)""", (channel.guild.id, channel.id, role))
    channels.commit()
    cursor.close()
    channels.close()

def changeRole(channel: channelClass, role: str):
    targetRole = getRole(channel)
    if targetRole is None:
        addRole(channel, role)
        return
    guildId = channel.guild.id
    channels = sqlite3.connect("channels.sqlite")
    cursor = channels.cursor()
    cursor.execute(f"""UPDATE channels SET role = {role} WHERE channel_id = {channel.id}""")
    channels.commit()
    cursor.close()
    channels.close()

def deleteChannel(guildId: int, channelId: int):
    channels = sqlite3.connect("channels.sqlite")
    cursor = channels.cursor()
    cursor.execute(f"""DELETE FROM channels WHERE channel_id = {channelId}""")
    channels.commit()
    cursor.close()
    channels.close()

def getChannelRoles(guildId: int):
    channels = sqlite3.connect("channels.sqlite")
    cursor = channels.cursor()
    cursor.execute(f"""SELECT channel_id FROM channels WHERE guild_id = {guildId}""")
    channelIds = cursor.fetchall()
    channelRole = {}
    for channelId in channelIds:
        cursor.execute(f"""SELECT role FROM channels WHERE channel_id = ?""", (channelId))
        channelId = channelId[0]
        role = cursor.fetchone()
        if role is not None:
            role = role[0]
        channelRole[channelId] = role
    cursor.close()
    channels.close()
    return channelRole

@bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord!")
    for guild in bot.guilds:
        await calculateChannels(None, "startup", None, guild)
    print("Standing by")

async def calculateChannels(member, mode, ctx, guild):
    print("entered calculate channels func")
    if mode == "startup":
        print(f"Performing startup updates for channels in guild: {guild.name}")
    if mode == "member left":
        print(f"{member} left guild: {guild.name}!")

    elif mode == "member joined":
        print(f"{member} joined guild: {guild.name}!")

    elif mode == "forced update":
        print(f"Forced update commencing in guild: {guild.name}!")

    elif mode == "role changed":
        print(f"{member} updated a role in guild: {guild.name}")
    print("updating channels...")
    sumOfRoles = {}
    sumOfRoles["norole"] = 0
    for role in guild.roles:
        print(role.id)
        sumOfRoles[str(role.id)] = 0
    for member in guild.members:
        numberOfRoles = 0
        for role in member.roles:
            numberOfRoles += 1
            sumOfRoles[str(role.id)] += 1
        if numberOfRoles == 1:
            #Every member has at least one role: @everyone
            sumOfRoles["norole"] += 1

    channelRoles = getChannelRoles(guild.id)
    for channelId in channelRoles:
        role = channelRoles.get(channelId)
        roleNumber = sumOfRoles.get(role)
        targetChannel = None
        for channel in guild.voice_channels:
            if channel.id == channelId:
                targetChannel = channel
        
        await updateChannel(targetChannel, roleNumber, guild)

    print(f"Channels updated in guild {guild}!")
    if (mode == "forced update"):
        await ctx.send("Channels updated!")

async def updateChannel(channel, roleNumber, guild):
    if bot.is_ws_ratelimited:
        print("The bot is currently being rate limited. Updating channels will slow down")
    firstNumber = None
    words = channel.name.split()
    print(f"updating name for channel {channel.name}")
    for i, word in enumerate(words):
        print (f"current word is: {word}")
        if word.isdigit():
            firstNumber = word
            words[i] = str(roleNumber)
            print(f"previous word was: {word}")
            print(f"changed word is: {words[i]}")
            break
    words = " ".join(words)
    print(words)
    output = None
    if firstNumber is None:
        print("no number in name")
        output = channel.name + str(roleNumber)
    else:
        print("OK")
        output = words
    previousName = channel.name
    await channel.edit(name=output)
    print(f"channel {previousName} renamed to {channel.name} in guild {guild}")


@bot.event
async def on_guild_join(guild):
    result = getPrefix(guild.id)
    if result is None:
        addPrefix(guild.id)


@bot.listen('on_message')
async def on_message(msg):
    if not msg.mentions:
        return
    if msg.mentions[0] == bot.user:
        prefix = getPrefix(msg.guild.id)
        await msg.channel.send("My prefix for this server is: " + prefix)

@bot.event
async def on_member_update(before, after):
    if before.roles != after.roles:
        await calculateChannels(after, "role changed", None, after.guild)

@bot.event
async def on_member_join(member):
    await calculateChannels(member, "member joined", None, member.guild)


@bot.event
async def on_member_remove(member):
    await calculateChannels(member, "member left", None, member.guild)


@bot.event
async def on_guild_channel_delete(channel):
    role = getRole(channel)
    if (role != None):
        check = True
    else:
        check = False
    deleteChannel(channel.guild.id, channel.id)
    print(f"Channel {channel} deleted in guild {channel.guild}: Tracked = {check}")

@bot.command(name="forceUpdate", help="Forces an update to channel names")
async def forceUpdate(ctx):
    await calculateChannels(None, "forced update", ctx, ctx.guild)


@bot.command(name="prefix", help="Changes the bot's prefix")
@commands.has_permissions(manage_guild=True)
async def prefixChange(ctx, prefix):
    prefix = str(prefix)
    changePrefix(ctx.guild.id, prefix)
    print(f"prefix updated to {prefix} in guild: {ctx.guild}")
    message = f"Prefix changed to ( {prefix} )"
    await ctx.send(message)


@prefixChange.error
async def prefixHelp(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        prefix = getPrefix(ctx.guild.id)
        answer = f"To change prefix, you must supply a new prefix as an argument.\nThe command call should look like \"{prefix}prefix !\",\nassuming  you want to change your prefix to !"
        await ctx.send(answer)
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send(
            "To change prefix for the bot you must have the manage server permission"
        )
    else:
        raise error


@bot.command(name="create", help="Creates a Counting Channel")
@commands.has_permissions(manage_channels=True)
async def create(ctx, name, role):

    name = str(name)
    prefix = getPrefix(ctx.guild.id)
    e = commands.BadArgument("The role you included as an argument is invalid")
    try:
        if (role != "everyone" and role != "norole"):
            role = str(role)
            role = role.lower()
            role = role[3:-1]
    except:
        raise e
    if (roleValidityChecker(ctx, role) is False):
        raise e
    try:
        channel = await ctx.guild.create_voice_channel(name)
    except:
        raise commands.BotMissingPermissions('The bot must have the Manage Channels permission in order for it to be able to create channels')
    if (role == "everyone"):
        role = ctx.guild.default_role.id
    addRole(channel, role)

    prefix = getPrefix(ctx.guild.id)
    answer = f'Channel {name} tracking roleId {role} created successfully!\n\nUse command {prefix}edit "name of channel" "role you wish to track instead" to change the role that your channel tracks.\n\n NOTE: The edit command will change the first channel it finds with name you supplied. If you have more than one channel with the same name then use the channel ID instead of its name.\n\nNOTE2: You can freely change the name of your channel without issue. Just take care to include a number in your new name that the bot can change when it updates the role totals'
    await ctx.send(answer)
    print(f'Channel {name} created in guild {ctx.guild}')


@create.error
async def createHelp(ctx, error):
    prefix = getPrefix(ctx.guild.id)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'To create a counting channel you must supply a name and a role as arguments,\n\n so if you want to create a channel named Everyone: and have it track the @everyone role then enter {prefix}create "Everyone: 1" "@everyone".\n\n Make note of the 1 that I included in the name. The bot will change the first number in the name of your channel when it is updating it, so it is important that you include a number in your name at the location that you want your tracking number at\n\nNOTE: The roles you wish to track must be pinged!!!')
        print(error)
    elif isinstance(error, commands.BadArgument):
        await ctx.send(f'The role you included as an argument is invalid')
        print(error)
    elif isinstance(error, commands.BotMissingPermissions):
        await ctx.send(f'The bot must have the Manage Channels permission for it to be able to create channels')
    elif isinstance(error, discord.Forbidden):
        await ctx.send(f'The bot must have the Manage Channels permission for it to be able to create channels')
    else:
        raise error

def roleValidityChecker(ctx, input):
    if isinstance(input, str) is False:
        return False
    words = input.split()
    if len(words) != 1:
        return False
    isRole = False
    for role in ctx.guild.roles:
        roleId = str(role.id)
        if roleId == input:
            isRole = True
            break
    if isRole:
        return True
    if (input == "norole"):
        return True
    if (input == "everyone"):
        return True
    return False

@bot.command(name="edit", help="Changes what role a channel tracks")
async def edit(ctx, name, role):
    name = str(name)
    e = commands.BadArgument("The role you included as an argument is invalid")
    try:
        if (role != "everyone" and role != "norole"):
            role = str(role)
            role = role.lower()
            role = role[3:-1]
    except:
        raise e
    if (roleValidityChecker(ctx, role) is False):
        raise e
    try:
        name = int(name)
        targetChannel = None
        for channel in ctx.guild.voice_channels:
            if channel.id == name:
                targetChannel = channel
    except:
        name = str(name)
        targetChannel = None
        for channel in ctx.guild.voice_channels:
            if channel.name == name:
                targetChannel = channel
    try:
        if (role == "everyone"):
            role = ctx.guild.default_role.id
        changeRole(targetChannel, role)
        message = f'Channel {name} changed to tracking role {role} successfully!'
        print(f'Channel {name} edited in guild {ctx.guild}')
    except:
        message = f'Failed to edit channel. This is likely because the name or ID you supplied is incorrect'
    await ctx.send(message)

@edit.error
async def editHelp(ctx, error):
    prefix = getPrefix(ctx.guild.id)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'To edit a counting channel you must supply (a name or an id) and a role as arguments, so if you want to edit the channel named Everyone: and make it track users that have both the @everyone role then enter\n\n\n{prefix}edit "Everyone:" "@everyone".\n\nNOTE: The roles you wish to track must be pinged!!!\n\n\nYou supplied {name} as your channel name or id and {role} as your channel role')
        print(error)
    elif isinstance(error, commands.BadArgument):
        await ctx.send(f'The role you included as an argument is invalid')
        print(error)
    else:
        raise error
@bot.command(name="@Test")
async def test(ctx, arg):
    arg = arg[3:-1]
    print(arg)
    await ctx.send(arg)
bot.run(TOKEN)
