from discord.guild import Guild
import importlib.util
import os
from pattern_parser.simple_discord import SimpleMessage
from typing import Callable
from discord.channel import TextChannel

from discord.enums import NotificationLevel
from logs.log import print
from discord import Message
from utils import config
from discord.ext.commands import Bot
import discord
from db import db
from discord.flags import Intents
from inspect import getmembers, isclass
from asyncio.events import AbstractEventLoop
from logs import init_logs


class CountKeeper(Bot):
    def __init__(self, loop: AbstractEventLoop = None, command_prefix: Callable[[Bot, Message], str] = None, intents: Intents = None):
        if loop is not None:
            self.loop = loop
        if command_prefix is None:
            command_prefix = self.command_prefix
        if intents is None:
            intents: Intents = discord.Intents.all()

        super().__init__(command_prefix=command_prefix, intents=intents)

        self.remove_command("help")
        for cog in self.get_cogs():
            self.add_cog(cog(self))

    def command_prefix(self, bot: Bot, message: Message) -> str:
        return db.get_prefix(message.guild.id)

    def get_cogs(self, path_to_cogs: str = f'{os.getcwd()}/cogs') -> list:
        class_list = []
        for filename in os.listdir(path_to_cogs):
            if filename.endswith('.py'):
                path_dir = f"{path_to_cogs}/{filename}"
                name = f"cogs/{filename}"
                spec = importlib.util.spec_from_file_location(name, path_dir)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                for name, value in getmembers(module):
                    if isclass(value):
                        for base in value.__bases__:
                            if base.__name__ == "Cog":
                                class_list.append(value)
                                break
        return class_list

    def find_cog(self, cog_name: str, path_to_cogs: str = f'{os.getcwd()}/cogs'):
        cogs = self.get_cogs(path_to_cogs=path_to_cogs)
        for cog in cogs:
            if cog.__name__.lower() == cog_name.lower():
                return cog

    async def send_to_notified(self, guild: Guild, message: SimpleMessage) -> None:
        notification_channel = self.get_notified_channel(guild)
        if notification_channel is None:
            return
        await message.send_contents(notification_channel)

    def get_notified_channel(self, guild: Guild) -> None:
        channel_id = db.get_notification_channel(guild.id)
        channel: TextChannel
        for channel in guild.text_channels:
            if channel.id == channel_id:
                return channel
        return None


if __name__ == '__main__':
    init_logs.init()
    keeper = CountKeeper()
    keeper.run(config.BOT_TOKEN)
