import sqlite3
from logs.log import print
from discord import channel as ChannelClass
from utils import config
DEFAULT_PREFIX = config.DEFAULT_PREFIX
PATH_TO_PREFIXES = "count_keeper_data/prefixes.sqlite"
PATH_TO_CHANNELS = "count_keeper_data/channels.sqlite"
PATH_TO_NOTIFIED = "count_keeper_data/notify.sqlite"

def get_prefix (guild_id: int):
    global PATH_TO_PREFIXES
    try:
        prefixes = sqlite3.connect(PATH_TO_PREFIXES)
        cursor = prefixes.cursor()
        guild_id = str(guild_id)
        cursor.execute(f"""SELECT prefix FROM prefixes WHERE guild_id = ?""", (guild_id,))
        #cursor.fetchone() returns a touple containing one item
        prefix = cursor.fetchone()
    except sqlite3.Error as e:
        print(e)
        prefix = None
    if prefix is not None:
        prefix = prefix[0]
    cursor.close()
    prefixes.close()
    return prefix

def add_prefix (guild_id: int):
    global DEFAULT_PREFIX, pathToPrefixes
    guild_id = str(guild_id)
    try:
        prefixes = sqlite3.connect(PATH_TO_PREFIXES)
        cursor = prefixes.cursor()
        cursor.execute("""INSERT INTO prefixes (guild_id, prefix) VALUES(?,?)""", (guild_id, DEFAULT_PREFIX))
        prefixes.commit()
        successful = True
    except sqlite3.Error as e:
        successful = False
    cursor.close()
    prefixes.close()
    return successful

def change_prefix (guild_id: int, prefix):
    global PATH_TO_PREFIXES
    guild_id = str(guild_id)
    if (isinstance(prefix, int) is False and isinstance(prefix, str) is False):
        #Should never happen. Pretty sure all the args in a command call get converted to strings by discord anyway.
        raise TypeError("prefix must be of type int or str")
    if (isinstance(prefix, int)):
        #Just to be safe
        prefix = str(prefix)
    try:
        prefixes = sqlite3.connect(PATH_TO_PREFIXES)
        cursor = prefixes.cursor()
        cursor.execute("""UPDATE prefixes SET prefix = ? WHERE guild_id = ?""", (prefix, guild_id))
        prefixes.commit()
        successful = True
    except sqlite3.Error as e:
        successful = False
    cursor.close()
    prefixes.close()
    return successful

def remove_prefix (guild_id: int):
    global PATH_TO_PREFIXES
    guild_id = str(guild_id)
    try:
        prefixes = sqlite3.connect(PATH_TO_PREFIXES)
        cursor = prefixes.cursor()
        cursor.execute("""DELETE FROM prefixes WHERE guild_id = ?""", (guild_id,))
        prefixes.commit()
        successful = True
    except sqlite3.Error as e:
        successful = False
    cursor.close()
    prefixes.close()
    return successful
    
def get_pattern (channel_id: int):
    global PATH_TO_CHANNELS
    channels = sqlite3.connect(PATH_TO_CHANNELS)
    cursor = channels.cursor()
    channel_id = str(channel_id)
    print(channel_id)
    try:
        cursor.execute(f"""SELECT pattern FROM channels WHERE channel_id = ?""", (channel_id,))
        pattern = cursor.fetchone()[0]
    except sqlite3.Error as e:
        pattern = None
    cursor.close()
    channels.close()
    return pattern

def add_pattern (channel: ChannelClass, pattern: str):
    global PATH_TO_CHANNELS
    try:
        channels = sqlite3.connect(PATH_TO_CHANNELS)
        cursor = channels.cursor()
        cursor.execute("""INSERT INTO channels (guild_id, channel_id, pattern) VALUES(?,?,?)""", (channel.guild.id, channel.id, pattern))
        channels.commit()
        successful = True
    except sqlite3.Error as e:
        successful = False
    cursor.close()
    channels.close()
    return successful

def change_pattern (channel: ChannelClass, pattern: str):
    global PATH_TO_CHANNELS
    target_pattern = get_pattern(channel.id)
    if target_pattern is None:
        return add_pattern(channel, pattern)
    try:
        channels = sqlite3.connect(PATH_TO_CHANNELS)
        cursor = channels.cursor()
        cursor.execute("""UPDATE channels SET pattern = ? WHERE channel_id = ?""", (pattern, channel.id))
        channels.commit()
        successful = True
    except sqlite3.Error as e:
        successful = False
    cursor.close()
    channels.close()
    return successful

def delete_channel (channel_id: int):
    global PATH_TO_CHANNELS
    channel_id = str(channel_id)
    try:
        channels = sqlite3.connect(PATH_TO_CHANNELS)
        cursor = channels.cursor()
        cursor.execute(f"""DELETE FROM channels WHERE channel_id = ?""", (channel_id,))
        channels.commit()
        successful = True
    except sqlite3.Error as e:
        successful = False
    cursor.close()
    channels.close()
    return successful

def get_channel_patterns (guild_id: int):
    global PATH_TO_CHANNELS
    guild_id = str(guild_id)
    channels = sqlite3.connect(PATH_TO_CHANNELS)
    cursor = channels.cursor()
    try:
        cursor.execute(f"""SELECT channel_id FROM channels WHERE guild_id = ?""", (guild_id,))
        channel_ids = cursor.fetchall()
    except sqlite3.Error as e:
        print(e)
        cursor.close()
        channels.close()
        return None
    channel_pattern = {}
    for channel_id in channel_ids:
        cursor.execute("""SELECT pattern FROM channels WHERE channel_id = ?""", channel_id)
        channel_id = channel_id[0]
        pattern = cursor.fetchone()
        if pattern is not None:
            pattern = pattern[0]
        channel_pattern[channel_id] = pattern
    cursor.close()
    channels.close()
    return channel_pattern

def get_channels (guild_id: int):
    global PATH_TO_CHANNELS
    guild_id = str(guild_id)
    channels = sqlite3.connect(PATH_TO_CHANNELS)
    cursor = channels.cursor()
    try:
        cursor.execute(f"""SELECT channel_id FROM channels WHERE guild_id = ?""", (guild_id,))
        channel_ids = cursor.fetchall()
        for i, channel_id in enumerate(channel_ids):
            channel_ids[i] = channel_id[0]
    except Exception as e:
        channel_ids = None
    cursor.close()
    channels.close()
    return channel_ids

def add_notification_channel (channel: ChannelClass):
    global PATH_TO_NOTIFIED
    try:
        notified = sqlite3.connect(PATH_TO_NOTIFIED)
        cursor = notified.cursor()
        cursor.execute("""INSERT INTO notified (guild_id, channel_id VALUES(?,?)""", (channel.guild.id, channel.id))
        notified.commit()
        successful = True
    except sqlite3.Error as e:
        successful = False
    cursor.close()
    notified.close()
    return successful