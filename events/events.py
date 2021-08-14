from patterns import counting_channels
from db import db
from discord import Guild as GuildClass
from events import event_helpers
import discord
from utils import discord_utils, utils
from logs.log import print
#This file contains all the code for how the bot should handle different events
async def on_ready(bot):
    print(f"{bot.user} has connected to Discord!")
    for guild in bot.guilds:
        print(f"Performing startup for guild {guild.name}")
        print(f"Fetching channels from db...")
        channels = db.get_channels(guild.id)
        for channel_id in channels:
            print(f"Checking if channel with id {channel_id} still exists")
            channel = discord_utils.find(lambda channel, channel_id: channel.id == channel_id, guild.voice_channels, channel_id)
            if channel is None:
                print(f"Channel with id {channel_id} doesn't exist. Removing from DB")
                db.delete_channel(channel_id)
            else:
                print(f"Channel with id {channel_id} still exists")
        await counting_channels.calculate_channels(None, "startup", None, guild)
        print("Standing by")

async def on_guild_join(guild: GuildClass):
    utils.add_prefix_to_guild_if_none(guild)
    utils.remove_deleted_channels_from_db(guild)
    print(f"Bot joined guild {guild.name} (ID:) {guild.id}")
    logs = await guild.audit_logs(limit=1, action=discord.AuditLogAction.bot_add).flatten()
    inviter = logs[0].user
    await inviter.send(embed=event_helpers.guild_join_message(inviter, guild))
    
    
    
async def on_guild_leave(guild):
    print(f"Bot left guild {guild.name} (ID:) {guild.id}")

async def on_message(bot, message):
    if not message.mentions:
        return
    for mention in message.mentions:
        if mention == bot.user:
            prefix = db.get_prefix(message.guild.id)
            await message.channel.send(f"My prefix for this server is: {prefix}")
    

async def on_member_update(before, after):
    if before.roles != after.roles:
        await counting_channels.calculate_channels(after, "role changed", None, after.guild)

async def on_member_join(member):
    await counting_channels.calculate_channels(member, "member joined", None, member.guild)

async def on_member_remove(member):
    await counting_channels.calculate_channels(member, "member left", None, member.guild)

async def on_guild_channel_delete(channel):
    pattern = db.get_pattern(channel.id)
    if pattern != None:
        db.delete_channel(channel.id)
        print(f"Counting Channel {channel} deleted in guild {channel.guild}")

