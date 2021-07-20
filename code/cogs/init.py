from discord.ext.commands import Cog, Bot
from db import db
from utils import DiscordUtils, CountingChannels
from logs.log import print
class Init(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        print("Init cog linked to bot!")
    
    @Cog.listener()
    async def on_ready(self):
        print(f"{self.bot.user} has connected to Discord!")
        for guild in self.bot.guilds:
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