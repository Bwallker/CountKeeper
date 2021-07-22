import pytest
import discord.ext.test as dpytest
from count_keeper import CountKeeper
@pytest.fixture
def bot(event_loop):
    bot = CountKeeper(loop=event_loop)
    dpytest.configure(bot)
    return bot