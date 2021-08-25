from utils.utils import remove_deleted_channels_from_db
from discord.ext.commands import Cog, Bot
from db import db
from pattern_parser import channels_manager
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
            remove_deleted_channels_from_db(guild)
            print(f"Updating channels in guild {guild}")
            await channels_manager.update_channels(guild, self.bot.get_notified_channel(guild))
        print("Standing by")
