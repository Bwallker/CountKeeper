#TODO:
#- Implement more advanced Counting Channels (Track several roles in one channel)
#- Split main.py into several files. probably utils.py, bot.py, commands.py, and maybe one file for every command
#- 
from utils import sqlite3
from events import events
from commands import commands as commands
import discord
from discord.ext import commands as discordCommands
#Automatically takes every item in the config file and creates a global variable based on it.
#Makes it so I don't have to pull the info out of the config file manually every time I add a new thing to it
#Makes the IDE debugger unhappy because the variables aren't explicitly created
from utils import config
for (key, value) in config.configData.items():
        globals()[key] = value
intents = discord.Intents.default()
# Intents.members is needed for the bot to be able to see what roles every member has
intents.members = True
# Intents.presences is needed for the bot to be able to see what members are online
intents.presences = True
def get_prefix(bot, message):
    return sqlite3.getPrefix(message.guild.id)

bot = discordCommands.Bot(command_prefix=get_prefix, intents=intents)

@bot.event
async def on_ready():
    global bot
    await events.on_ready(bot)


@bot.event
async def on_guild_join(guild):
    await events.on_guild_join(guild)

@bot.event
async def on_guild_leave(guild):
    await events.on_guild_leave(guild)

@bot.listen('on_message')
async def on_message(message):
    global bot
    await events.on_message(bot, message)
@bot.event
async def on_member_update(before, after):
    await events.on_member_update(before, after)

@bot.event
async def on_member_join(member):
    await events.on_member_join(member)


@bot.event
async def on_member_remove(member):
    await events.on_member_remove(member)


@bot.event
async def on_guild_channel_delete(channel):
    await events.on_guild_channel_delete(channel)


@bot.command(name="forceUpdate", help="Forces an update to the Counting Channels in your guild")
async def forceUpdate(ctx):
    await commands.forceUpdate(ctx)


@bot.command(name="prefix", breif="Changes the bot's prefix", help=commands.prefixHelpText())
@discordCommands.has_permissions(manage_guild=True)
async def prefix(ctx, prefix):
    await commands.prefix(ctx, prefix)

@prefix.error
async def prefixError(ctx, error):
    await commands.prefixError(ctx, error)


@bot.command(name="create", breif="Creates a Counting Channel", help=commands.createHelpText())
@discordCommands.has_permissions(manage_channels=True)
async def create(ctx, name, role):
    await commands.create(ctx, name, role)

@create.error
async def createError(ctx, error):
    await commands.createError(ctx, error)

@bot.command(name="edit", breif="Changes what role a Counting Channel tracks", help=commands.editHelpText())
async def edit(ctx, name, role, newName):
    await commands.edit(ctx, name, role, newName)

@edit.error
async def editHelp(ctx, error):
    await commands.editError(ctx, error)

@bot.command(name="listChannels", help="Lists all the Counting Channels in your guild")
async def listChannels(ctx):
    await commands.listChannels(ctx)

@bot.command(name="listGuilds", help="Debugging command - Lists all the guilds the bot is in")
async def listGuilds(ctx):
    global bot
    await commands.listGuilds(ctx, bot)
@bot.command(name="listChannelsInAllGuilds", help="Debugging command - Lists all the channels in the guilds the bot is apart of")
async def listChannelsInAllGuilds(ctx):
    global bot
    await commands.listChannelsInAllGuilds(ctx, bot)

bot.run(BOT_TOKEN)
