import sqlite3
from logs.log import print
from discord import channel as channelClass
from utils import config
DEFAULT_PREFIX = config.DEFAULT_PREFIX
pathToPrefixes = "CountKeeperData/prefixes.sqlite"
pathToChannels = "CountKeeperData/channels.sqlite"
pathToNotified = "CountKeeperData/notify.sqlite"

def getPrefix (guildId: int):
    global pathToPrefixes
    try:
        prefixes = sqlite3.connect(pathToPrefixes)
        cursor = prefixes.cursor()
        guildId = str(guildId)
        cursor.execute(f"SELECT prefix FROM prefixes WHERE guild_id = {guildId}")
        #cursor.fetchone() returns a touple containing one item
        prefix = cursor.fetchone()
    except sqlite3.Error as e:
        prefix = None
    if prefix is not None:
        prefix = prefix[0]
    cursor.close()
    prefixes.close()
    return prefix

def addPrefix (guildId: int):
    global DEFAULT_PREFIX, pathToPrefixes
    guildId = str(guildId)
    try:
        prefixes = sqlite3.connect(pathToPrefixes)
        cursor = prefixes.cursor()
        cursor.execute("""INSERT INTO prefixes (guild_id, prefix) VALUES(?,?)""", (guildId, DEFAULT_PREFIX))
        prefixes.commit()
        successful = True
    except sqlite3.Error as e:
        successful = False
    cursor.close()
    prefixes.close()
    return successful

def changePrefix (guildId: int, prefix):
    global pathToPrefixes
    guildId = str(guildId)
    if (isinstance(prefix, int) is False and isinstance(prefix, str) is False):
        #Should never happen. Pretty sure all the args in a command call get converted to strings by discord anyway.
        raise TypeError("prefix must be of type int or str")
    if (isinstance(prefix, int)):
        #Just to be safe
        prefix = str(prefix)
    try:
        prefixes = sqlite3.connect(pathToPrefixes)
        cursor = prefixes.cursor()
        cursor.execute("""UPDATE prefixes SET prefix = ? WHERE guild_id = ?""", (prefix, guildId))
        prefixes.commit()
        successful = True
    except sqlite3.Error as e:
        successful = False
    cursor.close()
    prefixes.close()
    return successful

def getType (channel: channelClass):
    global pathToChannels
    channels = sqlite3.connect(pathToChannels)
    cursor = channels.cursor()
    try:
        cursor.execute(f"""SELECT type FROM channels WHERE channel_id = {channel.id}""")
        type = cursor.fetchone()[0]
    except sqlite3.Error as e:
        type = None
    cursor.close()
    channels.close()
    return type

def addType (channel: channelClass, type: str):
    global pathToChannels
    try:
        channels = sqlite3.connect(pathToChannels)
        cursor = channels.cursor()
        cursor.execute("""INSERT INTO channels (guild_id, channel_id, type) VALUES(?,?,?)""", (channel.guild.id, channel.id, type))
        channels.commit()
        successful = True
    except sqlite3.Error as e:
        successful = False
    cursor.close()
    channels.close()
    return successful

def changeType (channel: channelClass, type: str):
    global pathToChannels
    targetType = getType(channel)
    if targetType is None:
        return addType(channel, type)
    try:
        channels = sqlite3.connect(pathToChannels)
        cursor = channels.cursor()
        cursor.execute("""UPDATE channels SET type = ? WHERE channel_id = ?""", (type, channel.id))
        channels.commit()
        successful = True
    except sqlite3.Error as e:
        successful = False
    cursor.close()
    channels.close()
    return successful

def deleteChannel (channelId: int):
    global pathToChannels
    channelId = str(channelId)
    try:
        channels = sqlite3.connect(pathToChannels)
        cursor = channels.cursor()
        cursor.execute(f"""DELETE FROM channels WHERE channel_id = {channelId}""")
        channels.commit()
        successful = True
    except sqlite3.Error as e:
        successful = False
    cursor.close()
    channels.close()
    return successful

def getChannelTypes (guildId: int):
    global pathToChannels
    guildId = str(guildId)
    channels = sqlite3.connect(pathToChannels)
    cursor = channels.cursor()
    try:
        cursor.execute(f"""SELECT channel_id FROM channels WHERE guild_id = {guildId}""")
        channelIds = cursor.fetchall()
    except sqlite3.Error as e:
        cursor.close()
        channels.close()
        return None
    channelType = {}
    for channelId in channelIds:
        cursor.execute("""SELECT type FROM channels WHERE channel_id = ?""", (channelId))
        channelId = channelId[0]
        type = cursor.fetchone()
        if type is not None:
            type = type[0]
        channelType[channelId] = type
    cursor.close()
    channels.close()
    return channelType

def getChannels (guildId: int):
    global pathToChannels
    guildId = str(guildId)
    channels = sqlite3.connect(pathToChannels)
    cursor = channels.cursor()
    try:
        cursor.execute(f"""SELECT channel_id FROM channels WHERE guild_id = {guildId}""")
        channelIds = cursor.fetchall()
        for i, channelId in enumerate(channelIds):
            channelIds[i] = channelId[0]
    except Exception as e:
        channelIds = None
    cursor.close()
    channels.close()
    return channelIds

def addNotificationChannel(channel: channelClass):
    global pathToNotified
    try:
        notified = sqlite3.connect(pathToNotified)
        cursor = notified.cursor()
        cursor.execute("""INSERT INTO notified (guild_id, channel_id VALUES(?,?)""", (channel.guild.id, channel.id))
        notified.commit()
        successful = True
    except sqlite3.Error as e:
        successful = False
    cursor.close()
    notified.close()
    return successful