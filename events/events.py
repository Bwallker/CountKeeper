from utils import CountingChannels
from utils import sqlite3
from utils import utils
#This file contains all the code for how the bot should handle different events
async def on_ready(bot):
    print(f"{bot.user} has connected to Discord!")
    for guild in bot.guilds:
        await CountingChannels.calculateChannels(None, "startup", None, guild)
    print("Standing by")

async def on_guild_join(guild):
    utils.addPrefixToGuildIfNone(guild)
    
    utils.removeDeletedChannelsFromDB
    print(f"Bot joined guild {guild.name} (ID:) {guild.id}")
async def on_guild_leave(guild):
    print(f"Bot left guild {guild.name} (ID:) {guild.id}")

async def on_message(bot, message):
    if not message.mentions:
        return
    for mention in message.mentions:
        if mention == bot.user:
            prefix = sqlite3.getPrefix(message.guild.id)
            await message.channel.send("My prefix for this server is: " + prefix)
    

async def on_member_update(before, after):
    if before.roles != after.roles:
        await CountingChannels.calculateChannels(after, "role changed", None, after.guild)

async def on_member_join(member):
    await CountingChannels.calculateChannels(member, "member joined", None, member.guild)

async def on_member_remove(member):
    await CountingChannels.calculateChannels(member, "member left", None, member.guild)

async def on_guild_channel_delete(channel):
    role = sqlite3.getRole(channel)
    if (role != None):
        check = True
    else:
        check = False
    sqlite3.deleteChannel(channel.id)
    if (check):
        print(f"Counting Channel {channel} deleted in guild {channel.guild}")

