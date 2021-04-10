from utils import sqlite3

def addPrefixToGuildIfNone(guild):
    #Called on_guild_join
    #Sets the prefix of a guild to the default prefix if it doesn't have one
    result = sqlite3.getPrefix(guild.id)
    if result is None:
        sqlite3.addPrefix(guild.id)

def removeDeletedChannelsFromDB(guild):
    #Removes deleted channels from the DB that the bot might have previously been tracking when it was in the guild previously
    countingChannelIds = sqlite3.getChannels(guild.id)
    for countingChannelId in countingChannelIds:
        exists = False
        for voiceChannel in guild.voice_channels:
            if str(countingChannelId) == str(voiceChannel.id):
                exists = True
        if exists is False:
            #Remove it from the DB
            sqlite3.deleteChannel(countingChannelId)