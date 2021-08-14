from count_keeper import CountKeeper
import os
import cogs.cogs_manager as cogs_manager
import pytest
import discord.ext.test as dpytest
from discord import Client


@pytest.fixture
def bot(event_loop) -> Client:
    bot = CountKeeper(loop=event_loop)
    dpytest.configure(bot)
    return bot


@pytest.mark.asyncio
async def test_load_and_unload(bot: CountKeeper):
    path_to_test_cogs = f'{os.getcwd()}/cogs_for_testing'
    manager = cogs_manager.CogsManager(bot)
    cog1 = "Cog1"

    manager.load_helper(cog1, path_to_cogs=path_to_test_cogs)
    contains_after_adding: bool = False
    for cog in bot.cogs:
        if cog == cog1:
            contains_after_adding = True
    assert contains_after_adding

    manager.unload_helper(cog1)
    contains_after_removal: bool = False
    for cog in bot.cogs:
        if cog == cog1:
            contains_after_removal = True
    assert not contains_after_removal
