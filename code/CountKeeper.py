from inspect import getmembers, isclass
from discord.ext.commands.errors import ExtensionAlreadyLoaded, ExtensionFailed, ExtensionNotFound, ExtensionNotLoaded, NoEntryPointError
from discord.flags import Intents
from logs import init_logs
init_logs.init()
#TODO:
#- Implement more advanced Counting Channels (Track several roles in one channel)
#- Split main.py into several files. probably utils.py, bot.py, commands.py, and maybe one file for every command
#- 
from abc import ABC
from db import db
from events import events
from commands import commands as commands
import discord
from discord.ext import commands as discordCommands
from utils import config
from utils import utils

from discord import Message
from logs.log import print
from DiscordOverrides.Bot import Bot
from cogs import init
from typing import Callable, ClassVar, TypeVar
import os

import importlib.util
DEFAULT_PREFIX = config.DEFAULT_PREFIX
BOT_TOKEN = config.BOT_TOKEN
intents: Intents = discord.Intents.default()
# Intents.members is needed for the bot to be able to see what roles every member has
intents.members = True
# Intents.presences is needed for the bot to be able to see what members are online
intents.presences = True
def get_prefix(bot: discordCommands.bot, message: Message) -> str:
    return db.getPrefix(message.guild.id)



                   


class CountKeeper(discordCommands.Bot):
    def __init__(self, command_prefix: Callable[[discordCommands.Bot, Message], str] = get_prefix, intents: Intents = intents):
        super().__init__(command_prefix=command_prefix, intents=intents)
        dir = os.getcwd()
        dir += "/cogs"
        for cog in self.get_cogs(dir):
            self.add_cog(cog(self))
        
    def get_cogs(self, path_to_cogs: str) -> list:
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

    def find_cog(self, cog_name: str):
        cogs = self.get_cogs()
        for cog in cogs:
            if cog.__name__.lower() == cog_name.lower():
                return cog
            
    def load(self, cog_name: str):
        cog = self.find_cog(cog_name)
        self.add_cog(cog(self))
        
    
    def unload(self, cog_name: str):
        self.remove_cog(cog_name)

CountKeeper()