from db import DBError
from db import db
from discord.ext import commands, tasks
import discord
from discord import message as msg
from utils import counting_channels
from utils import utils
from utils import discord_utils
from logs.log import print


async def force_update(ctx):
    await counting_channels.calculate_channels(None, "forced update", ctx, ctx.guild)

# -----------------------------------------------------------------------------------------
async def prefix(ctx, prefix):
    prefix = str(prefix)
    successful = db.change_prefix(ctx.guild.id, prefix)
    if not successful:
        raise DBError()
    print(f"prefix updated to {prefix} in guild: {ctx.guild}")
    message = f"Prefix changed to ( {prefix} )"
    await ctx.send(message)

def prefix_help_text():

    return "The prefix command changes the prefix of your server. To change prefix, you must supply a new prefix as an argument.\nThe command call should look like {prefix}prefix !\n\nAssuming you want to change your prefix to !"

async def prefix_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        prefix = db.getPrefix(ctx.guild.id)
        answer = prefix_help_text()
        await ctx.send(answer)
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send(
            "To change prefix for the bot you must have the manage server permission"
        )
    elif isinstance(error, DBError):
        await ctx.send("A database error occured while changing the prefix for your server! Try setting it to a different one")
    else:
        raise error
# -----------------------------------------------------------------------------------------
async def create(ctx, name, role):
    role = counting_channels.clean_up_pattern(ctx, role)
    prefix = db.get_prefix(ctx.guild.id)
    e = commands.BadArgument("The role you included as an argument is invalid")
    if (counting_channels.pattern_validity_checker(ctx, role) is False):
        raise e
    try:
        channel = await ctx.guild.create_voice_channel(name)
    except:
        raise commands.BotMissingPermissions('The bot must have the Manage Channels permission in order for it to be able to create channels')
    successful = db.add_pattern(channel, role)
    if not successful:
        raise DBError
    answer = f'Channel {name} tracking roleId {role} created successfully!\n\nUse command {prefix}edit "name of channel" "role you wish to track instead" to change the role that your channel tracks.\n\n NOTE: The edit command will change the first channel it finds with name you supplied. If you have more than one channel with the same name then use the channel ID instead of its name.\n\nNOTE2: You can freely change the name of your channel without issue. Just take care to include a number in your new name that the bot can change when it updates the role totals'
    await ctx.send(answer)
    print(f'Channel {name} created in guild {ctx.guild}')

def create_help_text():
    return "This command creates a new Counting Channel.\n\nCounting Channels are the channels the bot uses to count roles.\n\nThe command call should look like {prefix}/create \"Members: 0\" \"@myRole\" Assuming you want your channel to be called Members: and you want it to track the @myRole role.\n\n Instead of pinging a role you can use \"everyone\" and \"norole\" to track everyone in your server or the people without any roles."

async def create_error(ctx, error):
    prefix = db.getPrefix(ctx.guild.id)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(create_help_text())
        print(error)
    elif isinstance(error, commands.BadArgument):
        await ctx.send(f'The role you included as an argument is invalid')
        print(error)
    elif isinstance(error, commands.BotMissingPermissions):
        await ctx.send(f'The bot must have the Manage Channels permission for it to be able to create channels')
    elif isinstance(error, discord.Forbidden):
        await ctx.send(f'The bot must have the Manage Channels permission for it to be able to create channels')
    elif isinstance(error, DBError):
        await ctx.send()
    else:
        raise error
# -----------------------------------------------------------------------------------------
async def edit(ctx, name, pattern, newName):
    role = counting_channels.clean_up_pattern(ctx, pattern)
    e = commands.BadArgument("The role you included as an argument is invalid")
    if (counting_channels.pattern_validity_checker(ctx, pattern) is False):
        raise e
    if isinstance(name, int) is True:
        name = int(name)
        target_channel = None
        for channel in ctx.guild.voice_channels:
            if channel.id == name:
                target_channel = channel
    else:
        name = str(name)
        target_channel = None
        for channel in ctx.guild.voice_channels:
            if channel.name == name:
                target_channel = channel
    try:
        db.changeType(target_channel, role)
        await target_channel.edit(name=newName)
        message = f'Channel {name} changed to tracking role {role} with new name {newName} successfully!'
        print(f'Channel {newName} edited in guild {ctx.guild}')
    except:
        message = f'Failed to edit channel. This is likely because the name or ID you supplied is incorrect'
    await ctx.send(message)

def edit_help_text():
    return "This command edits a Counting Channel.\n\nCounting Channels are the channels that the bot uses to count roles.\n\nTo edit a Counting Channel you must supply (the name or the id) of your old channel, a new role for it to track, and a new name for the channel as arguments, so if you want to edit the channel named \"Everyone: 1\" and make it track users that have the @everyone role, but you don\'t want to change its name, then enter\n\n\n{prefix}edit \"Everyone: 1\" \"everyone\" \"Everyone: 1\".\n\nNOTE: The roles you wish to track must be pinged!!!\n\n\n Note2: If you wish to track the @everyone role or track people without any roles then use \"everyone\" or \"norole\" instead of pinging a role."

async def edit_error(ctx, error):
    prefix = db.get_prefix(ctx.guild.id)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(edit_help_text())
        print(error)
    elif isinstance(error, commands.BadArgument):
        await ctx.send(f'The role you included as an argument is invalid')
        print(error)
    else:
        raise error
# -----------------------------------------------------------------------------------------
async def notify(ctx, channel_id_or_name):
    try:
        channel_id = int(channel_id_or_name)
        channel = discord_utils.get(lambda channel, channelId: channel.id == channelId, ctx.guild.text_channels, channel_id)
        if channel is None:
            raise ValueError()
    except ValueError as e:
        channel_name = str(channel_id_or_name)
        channel = discord_utils.get(lambda channel, channelName: channel.name == channelName, ctx.guild.text_channels, channel_name)
        if channel is None:
            raise discord.InvalidArgument("The channel name or id you have provided is invalid")
    db.add_notification_channel(channel)
    message = f'Notification channel has been been set to channel with ID of ({str(channel.id)}) and name of ({channel.name}) in guild {channel.guild.name}'
    await utils.print_and_send(message)

def notify_help_text():
    return "TODO"

async def notify_error(ctx, error):
    await utils.print_and_send(error)
# -----------------------------------------------------------------------------------------
async def list_channels(ctx):
    channel_id_patterns = db.get_channel_patterns(ctx.guild.id)
    if channel_id_patterns is None:
        message = f"guild {ctx.guild.name} contains no Counting Channels"
        await ctx.send(message)
        print(message)
        return
    channel_patterns = {}
    for channelId in channel_id_patterns:
        for channel in ctx.guild.voice_channels:
            if channelId == channel.id:
                channel_patterns[channel] = channel_id_patterns[channelId]
    print(channel_patterns)
    i = 0
    message = f"Counting Channels in guild {ctx.guild.name}:\n\n"
    for channel in channel_patterns:
        role = channel_patterns[channel]
        i += 1
        message += "Channel number " + str(i) + ":\n\t" + "Channel name: (" + channel.name + ") and ID: (" + str(channel.id) + ") tracking role: (" + role + ")\n"
    await ctx.send(message)
    print(message)
# -----------------------------------------------------------------------------------------

async def list_guilds(ctx, bot):
    print("Printing guild names...")
    for guild in bot.guilds:
        print("Guild name: " + guild.name)
        print("Guild ID: " + str(guild.id))
        print()
    print("Done printing guilds")

async def list_guilds_error(ctx, error):
    if isinstance(error, commands.NotOwner):
        await ctx.send("You must be the bot owner to use this command")
    elif isinstance(error, commands.TooManyArguments):
        await ctx.send("You gave this command arguments, even though it doesn't take any")
    else:
        raise error
# -----------------------------------------------------------------------------------------

async def list_channels_in_all_guilds(ctx, bot):
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


async def list_channels_in_all_guilds_error(ctx, error):
    if isinstance(error, commands.NotOwner):
        await ctx.send("You must be the bot owner to use this command")
    elif isinstance(error, commands.TooManyArguments):
        await ctx.send("You gave this command arguments, even though it doesn't take any")
    else:
        raise error
# -----------------------------------------------------------------------------------------

async def list_roles(ctx):
    await utils.print_and_send(ctx, f"Listing roles in guild {ctx.guild.name}...")
    i = 0
    message = ""
    for role in ctx.guild.roles:
        i += 1
        message += f"Role number {i} in guild {ctx.guild.name}:\n"
        message += f"\tRole name: {role.name}\n"
        message += f"\tRole ID: {role.id}\n"
    await utils.print_and_send(ctx, message)
        
async def listRolesError(ctx, error):
    if isinstance(error, commands.TooManyArguments):
        await ctx.send("You gave this command arguments, even though it doesn't take any")