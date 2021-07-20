from utils import CountingChannels
from db import db
from utils import utils
from discord import guild as guildClass
from events import EventHelpers
import discord
from utils import DiscordUtils
from logs.log import print
#This file contains all the code for how the bot should handle different events
async def on_ready(bot):
    
    print(f"{bot.user} has connected to Discord!")
    for guild in bot.guilds:
        print(f"Performing startup for guild {guild.name}")
        print(f"Fetching channels from db...")
        channels = db.getChannels(guild.id)
        for channelId in channels:
            print(f"Checking if channel with id {channelId} still exists")
            channel = DiscordUtils.find(lambda channel, channelId: channel.id == channelId, guild.voice_channels, channelId)
            if channel is None:
                print(f"Channel with id {channelId} doesn't exist. Removing from DB")
                db.deleteChannel(channelId)
            else:
                print(f"Channel with id {channelId} still exists")
        await CountingChannels.calculateChannels(None, "startup", None, guild)
    print("Standing by")

async def on_guild_join(guild: guildClass):
    utils.addPrefixToGuildIfNone(guild)
    utils.removeDeletedChannelsFromDB
    print(f"Bot joined guild {guild.name} (ID:) {guild.id}")
    logs = await guild.audit_logs(limit=1, action=discord.AuditLogAction.bot_add).flatten()
    inviter = logs[0].user
    await inviter.send(embed=EventHelpers.guildJoinMessage(inviter, guild))
    
    
    
async def on_guild_leave(guild):
    print(f"Bot left guild {guild.name} (ID:) {guild.id}")

async def on_message(bot, message):
    if not message.mentions:
        return
    for mention in message.mentions:
        if mention == bot.user:
            prefix = db.getPrefix(message.guild.id)
            await message.channel.send(f"My prefix for this server is: {prefix}")
    

async def on_member_update(before, after):
    if before.roles != after.roles:
        await CountingChannels.calculateChannels(after, "role changed", None, after.guild)

async def on_member_join(member):
    await CountingChannels.calculateChannels(member, "member joined", None, member.guild)

async def on_member_remove(member):
    await CountingChannels.calculateChannels(member, "member left", None, member.guild)

async def on_guild_channel_delete(channel):
    type = db.getType(channel)
    if (type != None):
        check = True
    else:
        check = False
    db.deleteChannel(channel.id)
    if (check):
        print(f"Counting Channel {channel} deleted in guild {channel.guild}")

