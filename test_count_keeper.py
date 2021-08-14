from db import db
from discord.channel import ChannelType
from discord.client import Client
from discord.message import Message
from discord import Guild
from count_keeper import CountKeeper
import os
import pytest
import discord.ext.test as dpytest
import logs.init_logs
logs.init_logs.init()

def test_add_cogs():
    keeper = CountKeeper()
    cogs = keeper.get_cogs(f'{os.getcwd()}/cogs_for_testing')
    cogs_names = [cog.__name__ for cog in cogs]
    # Here we are testing both that it gets all the cogs, and that it doesn't grab any noncogs
    compare_list = ["Cog1", "Cog2", "Cog3", "Cog4"]
    assert cogs_names == compare_list


def test_find_cogs():
    path_to_test_cogs = f'{os.getcwd()}/cogs_for_testing'
    keeper = CountKeeper()
    cog = keeper.find_cog("Cog1", path_to_cogs=path_to_test_cogs)
    assert cog is not None

    cog = keeper.find_cog("Cog2", path_to_cogs=path_to_test_cogs)
    assert cog is not None

    cog = keeper.find_cog("Cog3", path_to_cogs=path_to_test_cogs)
    assert cog is not None

    cog = keeper.find_cog("Cog4", path_to_cogs=path_to_test_cogs)
    assert cog is not None

    cog = keeper.find_cog("nonsense", path_to_cogs=path_to_test_cogs)
    assert cog is None


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
