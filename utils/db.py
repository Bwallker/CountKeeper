import sqlite3
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
        prefix = cursor.fetchone()[0]
    except sqlite3.Error as e:
        prefix = None
    cursor.close()
    prefixes.close()
    return prefix

def addPrefix (guildId: int):
    global DEFAULT_PREFIX, pathToPrefixes
    guildId = str(guildId)
    prefixes = sqlite3.connect(pathToPrefixes)
    cursor = prefixes.cursor()
    cursor.execute("""INSERT INTO prefixes (guild_id, prefix) VALUES(?,?)""", (guildId, DEFAULT_PREFIX))
    prefixes.commit()
    cursor.close()
    prefixes.close()

def changePrefix (guildId: int, prefix):
    global pathToPrefixes
    guildId = str(guildId)
    if (isinstance(prefix, int) is False and isinstance(prefix, str) is False):
        #Should never happen. Pretty sure all the args in a command call get converted to strings by discord anyway.
        raise TypeError("prefix must be of type int or str")
    if (isinstance(prefix, int)):
        #Just to be safe
        prefix = str(prefix)
    prefixes = sqlite3.connect(pathToPrefixes)
    cursor = prefixes.cursor()
    cursor.execute("""UPDATE prefixes SET prefix = ? WHERE guild_id = ?""", (prefix, guildId))
    prefixes.commit()
    cursor.close()
    prefixes.close()

def getRole (channel: channelClass):
    global pathToChannels
    channels = sqlite3.connect(pathToChannels)
    cursor = channels.cursor()
    try:
        cursor.execute(f"""SELECT role FROM channels WHERE channel_id = {channel.id}""")
        role = cursor.fetchone()[0]
    except sqlite3.Error as e:
        role = None
    cursor.close()
    channels.close()
    return role

def addRole (channel: channelClass, role: str):
    global pathToChannels
    channels = sqlite3.connect(pathToChannels)
    cursor = channels.cursor()
    cursor.execute("""INSERT INTO channels (guild_id, channel_id, role) VALUES(?,?,?)""", (channel.guild.id, channel.id, role))
    channels.commit()
    cursor.close()
    channels.close()

def changeRole (channel: channelClass, role: str):
    global pathToChannels
    targetRole = getRole(channel)
    if targetRole is None:
        addRole(channel, role)
        return
    channels = sqlite3.connect(pathToChannels)
    cursor = channels.cursor()
    cursor.execute("""UPDATE channels SET role = ? WHERE channel_id = ?""", (role, channel.id))
    channels.commit()
    cursor.close()
    channels.close()

def deleteChannel (channelId: int):
    global pathToChannels
    channelId = str(channelId)
    channels = sqlite3.connect(pathToChannels)
    cursor = channels.cursor()
    cursor.execute(f"""DELETE FROM channels WHERE channel_id = {channelId}""")
    channels.commit()
    cursor.close()
    channels.close()

def getChannelRoles (guildId: int):
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
    channelRole = {}
    for channelId in channelIds:
        cursor.execute("""SELECT role FROM channels WHERE channel_id = ?""", (channelId))
        channelId = channelId[0]
        role = cursor.fetchone()
        if role is not None:
            role = role[0]
        channelRole[channelId] = role
    cursor.close()
    channels.close()
    return channelRole

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
    except:
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