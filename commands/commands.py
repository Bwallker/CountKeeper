from utils import sqlite3
from discord.ext import commands, tasks
import discord
from discord import message as msg
from utils import CountingChannels
from utils import utils
from utils import DiscordUtils

async def forceUpdate(ctx):
    await CountingChannels.calculateChannels(None, "forced update", ctx, ctx.guild)

# -----------------------------------------------------------------------------------------
async def prefix(ctx, prefix):
    prefix = str(prefix)
    sqlite3.changePrefix(ctx.guild.id, prefix)
    print(f"prefix updated to {prefix} in guild: {ctx.guild}")
    message = f"Prefix changed to ( {prefix} )"
    await ctx.send(message)

def prefixHelpText():

    return "The prefix command changes the prefix of your server. To change prefix, you must supply a new prefix as an argument.\nThe command call should look like {prefix}prefix !\n\nAssuming you want to change your prefix to !"

async def prefixError(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        prefix = sqlite3.getPrefix(ctx.guild.id)
        answer = prefixHelpText()
        await ctx.send(answer)
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send(
            "To change prefix for the bot you must have the manage server permission"
        )
    else:
        raise error
# -----------------------------------------------------------------------------------------
async def create(ctx, name, role):
    role = CountingChannels.cleanUpType(ctx, role)
    prefix = sqlite3.getPrefix(ctx.guild.id)
    e = commands.BadArgument("The role you included as an argument is invalid")
    if (CountingChannels.roleValidityChecker(ctx, role) is False):
        raise e
    try:
        channel = await ctx.guild.create_voice_channel(name)
    except:
        raise commands.BotMissingPermissions('The bot must have the Manage Channels permission in order for it to be able to create channels')
    sqlite3.addRole(channel, role)

    answer = f'Channel {name} tracking roleId {role} created successfully!\n\nUse command {prefix}edit "name of channel" "role you wish to track instead" to change the role that your channel tracks.\n\n NOTE: The edit command will change the first channel it finds with name you supplied. If you have more than one channel with the same name then use the channel ID instead of its name.\n\nNOTE2: You can freely change the name of your channel without issue. Just take care to include a number in your new name that the bot can change when it updates the role totals'
    await ctx.send(answer)
    print(f'Channel {name} created in guild {ctx.guild}')

def createHelpText():
    return "This command creates a new Counting Channel.\n\nCounting Channels are the channels the bot uses to count roles.\n\nThe command call should look like {prefix}/create \"Members: 0\" \"@myRole\" Assuming you want your channel to be called Members: and you want it to track the @myRole role.\n\n Instead of pinging a role you can use \"everyone\" and \"norole\" to track everyone in your server or the people without any roles."

async def createError(ctx, error):
    prefix = sqlite3.getPrefix(ctx.guild.id)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(createHelpText())
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
# -----------------------------------------------------------------------------------------
async def edit(ctx, name, role, newName):
    role = CountingChannels.cleanUpType(ctx, role)
    e = commands.BadArgument("The role you included as an argument is invalid")
    if (CountingChannels.roleValidityChecker(ctx, role) is False):
        raise e
    if isinstance(name, int) is True:
        name = int(name)
        targetChannel = None
        for channel in ctx.guild.voice_channels:
            if channel.id == name:
                targetChannel = channel
    else:
        name = str(name)
        targetChannel = None
        for channel in ctx.guild.voice_channels:
            if channel.name == name:
                targetChannel = channel
    try:
        sqlite3.changeRole(targetChannel, role)
        await targetChannel.edit(name=newName)
        message = f'Channel {name} changed to tracking role {role} with new name {newName} successfully!'
        print(f'Channel {newName} edited in guild {ctx.guild}')
    except:
        message = f'Failed to edit channel. This is likely because the name or ID you supplied is incorrect'
    await ctx.send(message)
def editHelpText():
    return "This command edits a Counting Channel.\n\nCounting Channels are the channels that the bot uses to count roles.\n\nTo edit a Counting Channel you must supply (the name or the id) of your old channel, a new role for it to track, and a new name for the channel as arguments, so if you want to edit the channel named \"Everyone: 1\" and make it track users that have the @everyone role, but you don\'t want to change its name, then enter\n\n\n{prefix}edit \"Everyone: 1\" \"everyone\" \"Everyone: 1\".\n\nNOTE: The roles you wish to track must be pinged!!!\n\n\n Note2: If you wish to track the @everyone role or track people without any roles then use \"everyone\" or \"norole\" instead of pinging a role."

async def editError(ctx, error):
    prefix = sqlite3.getPrefix(ctx.guild.id)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(editHelpText())
        print(error)
    elif isinstance(error, commands.BadArgument):
        await ctx.send(f'The role you included as an argument is invalid')
        print(error)
    else:
        raise error
# -----------------------------------------------------------------------------------------

async def listChannels(ctx):
    channelIdRoles = sqlite3.getChannelRoles(ctx.guild.id)
    if channelIdRoles is None:
        message = f"guild {ctx.guild.name} contains no Counting Channels"
        await ctx.send(message)
        print(message)
        return
    channelRoles = {}
    for channelId in channelIdRoles:
        for channel in ctx.guild.voice_channels:
            if channelId == channel.id:
                channelRoles[channel] = channelIdRoles[channelId]
    print(channelRoles)
    i = 0
    message = f"Counting Channels in guild {ctx.guild.name}:\n\n"
    for channel in channelRoles:
        role = channelRoles[channel]
        i += 1
        message += "Channel number " + str(i) + ":\n\t" + "Channel name: (" + channel.name + ") and ID: (" + str(channel.id) + ") tracking role: (" + role + ")\n"
    await ctx.send(message)
    print(message)
# -----------------------------------------------------------------------------------------

async def listGuilds(ctx, bot):
    print("Printing guild names...")
    for guild in bot.guilds:
        print("Guild name: " + guild.name)
        print("Guild ID: " + str(guild.id))
        print()
    print("Done printing guilds")

async def listGuildsError(ctx, error):
    if isinstance(error, commands.NotOwner):
        await ctx.send("You must be the bot owner to use this command")
    elif isinstance(error, commands.TooManyArguments):
        await ctx.send("You gave this command arguments, even though it doesn't take any")
    else:
        raise error
# -----------------------------------------------------------------------------------------

async def listChannelsInAllGuilds(ctx, bot):
    print("Printing channels in guild...")
    for guild in bot.guilds:
        print("Printing channels in guild " + guild.name)
        i = 0
        for channel in guild.voice_channels:
            i+=1
            print("Channel number " + str(i) + ": \n")
            print("\tChannel name: " + channel.name)
            print("\tChannel id: " + str(channel.id))
            print("Done printing channel number " + str(i))
        print("Done printing channels in guild " + guild.name)


async def listChannelsinAllGuildsError(ctx, error):
    if isinstance(error, commands.NotOwner):
        await ctx.send("You must be the bot owner to use this command")
    elif isinstance(error, commands.TooManyArguments):
        await ctx.send("You gave this command arguments, even though it doesn't take any")
    else:
        raise error
# -----------------------------------------------------------------------------------------

async def listRoles(ctx):
    await utils.printAndSend(ctx, f"Listing roles in guild {ctx.guild.name}...")
    i = 0
    message = ""
    for role in ctx.guild.roles:
        i += 1
        message += f"Role number {i} in guild {ctx.guild.name}:\n"
        message += f"\tRole name: {role.name}\n"
        message += f"\tRole ID: {role.id}\n"
    await utils.printAndSend(ctx, message)
        
async def listRolesError(ctx, error):
    if isinstance(error, commands.TooManyArguments):
        await ctx.send("You gave this command arguments, even though it doesn't take any")
        
# -----------------------------------------------------------------------------------------

async def testUtils(ctx):
    test = DiscordUtils.find(lambda m: str(m.id) == '184170364757213186', ctx.guild.members)
    test = str(test.name)
    await utils.printAndSend(ctx, test)

async def testUtilsError(ctx, error):            
    if isinstance(error, commands.NotOwner):
        await ctx.send("You must be the bot owner to use this command")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("You must include the name of the utility function you wish to call as well as all the argument that function takes")
    else:
        raise error