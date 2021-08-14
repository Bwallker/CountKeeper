from discord.ext.commands import Cog, Bot
from db import db
from utils import discord_utils
from patterns import counting_channels
from logs.log import print
class Init(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        print("Init cog linked to bot!")
    
    @Cog.listener('on_ready')
    async def on_ready(self):
        print(f"{self.bot.user} has connected to Discord!")
        for guild in self.bot.guilds:
            if db.get_prefix(guild.id) is None:
                db.add_prefix(guild.id)
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