import unittest
from db import db
import discord
from discord.channel import TextChannel, ChannelType
from discord.client import Client
from discord.message import Message
from discord import Guild
from count_keeper import CountKeeper
import os
from utils import config, tests_config
import pytest
import asyncio
import discord.ext.test as dpytest
class MissingGetPrefixTestGuildId(Exception):
    """Exception that gets thrown if this test is run without there being a valid PREFIX_TEST_GUILD_ID in tests_config.json"""
class MissingGetPrefixTestTextChannelId(Exception):
    """Exception that gets thrown if this test is run without there being a valid PREFIX_TEST_TEXT_CHANNEL_ID in tests_config.json"""
class MissingGetPrefixTestMessageId(Exception):
    """Exception that gets thrown if this test is run without there being a valid PREFIX_TEST_MESSAGE_ID in tests_config.json"""







class CountKeeperTest(unittest.TestCase):
    def test_add_cogs(self):
        keeper = CountKeeper()
        cogs = keeper.get_cogs(f'{os.getcwd()}/cogs_for_testing')
        cogs_names = [cog.__name__ for cog in cogs]
        # Here we are testing both that it gets all the cogs, and that it doesn't grab any noncogs
        compare_list = ["Cog1", "Cog2", "Cog3", "Cog4"]
        self.assertEqual(cogs_names, compare_list)
    def test_find_cogs(self):
        path_to_test_cogs = f'{os.getcwd()}/cogs_for_testing'
        keeper = CountKeeper()
        cog = keeper.find_cog("Cog1", path_to_cogs=path_to_test_cogs)
        self.assertIsNotNone(cog)
        
        cog = keeper.find_cog("Cog2", path_to_cogs=path_to_test_cogs)
        self.assertIsNotNone(cog)
        
        cog = keeper.find_cog("Cog3", path_to_cogs=path_to_test_cogs)
        self.assertIsNotNone(cog)
        
        cog = keeper.find_cog("Cog4", path_to_cogs=path_to_test_cogs)
        self.assertIsNotNone(cog)
        
        
        cog = keeper.find_cog("nonsense", path_to_cogs=path_to_test_cogs)
        self.assertTrue(cog is None)
    
    def test_load_and_unload(self):
        path_to_test_cogs = f'{os.getcwd()}/cogs_for_testing'
        keeper = CountKeeper()
        cog1 = "Cog1"
        
        
        keeper.load(cog1, path_to_cogs=path_to_test_cogs)
        contains_after_adding: bool = False
        for cog in keeper.cogs:
            if cog == cog1:
                contains_after_adding = True
        self.assertTrue(contains_after_adding)
        
        
        keeper.unload(cog1)
        contains_after_removal: bool = False
        for cog in keeper.cogs:
            if cog == cog1:
                contains_after_removal = True
        self.assertFalse(contains_after_removal)
    
@pytest.fixture
def bot(event_loop) -> Client:
    bot = CountKeeper(loop=event_loop)
    dpytest.configure(bot)
    return bot
    
@pytest.mark.asyncio
async def test_get_prefix(bot: CountKeeper):
    guild: Guild = bot.guilds[0]
    assert db.add_prefix(guild.id)
    channel: ChannelType = guild.channels[0]
    await channel.send('junk')
    message: Message = dpytest.get_message()
    prefix = bot.command_prefix(bot, message)
    assert db.remove_prefix(guild.id)
    assert prefix is not None
        
if __name__ == '__main__':
    pytest.main()