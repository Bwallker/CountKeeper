from asyncio.events import AbstractEventLoop
from cogs.init import Init
from logs import init_logs
init_logs.init()

from inspect import getmembers, isclass
from discord.flags import Intents
from abc import ABC
from db import db
from events import events
from commands import commands as commands
import discord
from discord.ext import commands
from utils import config

from discord import Message
from logs.log import print
from typing import Callable
import os
import pytest
import importlib.util

import asyncio



                   


class CountKeeper(commands.Bot):
    def __init__(self, loop: AbstractEventLoop = None, command_prefix: Callable[[commands.Bot, Message], str] = None, intents: Intents = None):
        if loop is not None:
            self.loop = loop
        if command_prefix is None:
            command_prefix = self.command_prefix
        if intents is None:
            intents: Intents = discord.Intents.all()
        
        super().__init__(command_prefix=command_prefix, intents=intents)
        
        self.add_cog(Init(self))
        for cog in self.get_cogs():
            self.add_cog(cog(self))
            
        self.remove_command("help")


    def command_prefix(self, bot: commands.bot, message: Message) -> str:
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
            
    def load(self, cog_name: str, path_to_cogs: str = f'{os.getcwd()}/cogs'):
        cog = self.find_cog(cog_name, path_to_cogs=path_to_cogs)
        self.add_cog(cog(self))
        
    
    def unload(self, cog_name: str):
        self.remove_cog(cog_name)

if __name__ == '__main__':
    keeper = CountKeeper()
    keeper.run(config.BOT_TOKEN)