from patterns.operators import AndOperator, OrOperator
from patterns.simple_component import BooleanComponent
from patterns.advanced_component import Statement
from db import db
import utils.config as config


def test_prefix():
    prefix = "123456"
    guild = 100
    assert db.add_prefix(guild)
    assert db.get_prefix(guild) == config.DEFAULT_PREFIX
    assert db.change_prefix(guild, prefix)
    assert db.get_prefix(guild) == prefix
    assert db.remove_prefix(guild)
    assert db.get_prefix(guild) is None


def test_pattern():
    test_pattern = Statement(
        BooleanComponent(True),
        AndOperator(),
        BooleanComponent(True)
    )

    test_pattern_2 = Statement(
        BooleanComponent(False),
        OrOperator(),
        BooleanComponent(False)
    )
    channel = 100
    guild = 100
    assert db.get_pattern(channel) is None
    assert db.add_pattern(guild, channel, test_pattern)
    assert db.get_pattern(channel) == test_pattern
    assert db.change_pattern(guild, channel, test_pattern_2)
    assert db.get_pattern(channel) == test_pattern_2
    assert db.remove_pattern(channel)
    assert db.get_pattern(channel) is None


def test_channels():
    guild = 100
    channels = [
        1,
        5,
        8,
        13,
        17
    ]
    pattern = BooleanComponent(True)

    channel_patterns = {}

    for channel in channels:
        channel_patterns[channel] = pattern

    assert db.get_channels(guild) == []
    for channel in channels:
        db.add_pattern(guild, channel, pattern)
    assert sorted(db.get_channels(guild)) == sorted(channels)
    for channel in channels:
        db.remove_pattern(channel)
    assert db.get_channels(guild) == []

    assert db.get_channel_patterns(guild) == {}
    for channel in channels:
        db.add_pattern(guild, channel, pattern)
    assert db.get_channel_patterns(guild) == channel_patterns
    for channel in channels:
        db.remove_pattern(channel)
    assert db.get_channel_patterns(guild) == {}


def test_notified():
    guild = 100
    channel = 500
    channel_2 = 200
    assert db.get_notification_channel(guild) is None
    assert db.add_notification_channel(guild, channel)
    assert db.get_notification_channel(guild) == channel
    assert db.change_notification_channel(guild, channel_2)
    assert db.get_notification_channel(guild) == channel_2
    assert db.remove_notification_channel(guild)
    assert db.get_notification_channel(guild) is None
