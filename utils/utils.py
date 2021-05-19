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

async def printAndSend(ctx, message):
    #Prints and sends a message --- This func is here to make it so I don't have to do both one after the other constantly
    print(message)
    await ctx.send(message)
#These two functions are using in the cleanupType func in CountingChannels.py
def removeParenthesis(word):
    openingParenthesis = 0
    while word[openingParenthesis] == "(":
        openingParenthesis += 1
        word = word[1:]
    closingParenthesis = 0
    for char in range(len(word)-1, 0, -1):
        if word[char] != ")":
            break
        closingParenthesis += 1
        word = word[:-1]
    return word, openingParenthesis, closingParenthesis


def addParenthesis(word, openingParenthesis, closingParenthesis):
    for x in range(openingParenthesis):
        word = "(" + word
    for y in range(closingParenthesis):
        word = word + ")"
    return word

def checkParenthesis(type):
    #Checks if the parenthesis in a type makes sense
    parenthesis = 0
    words = type.split()
    lastParenthesis = ""
    for word in words:
        for char in word:
            if char == "(":
                lastParenthesis = "("
                parenthesis += 1
            elif char == ")":
                lastParenthesis = ")"
                parenthesis -= 1
    if parenthesis != 0:
        #If there are more of one type of parenthesis than the other, we have a problem
        return False
    #Next we'll check if the last parenthesis is a "(". If it is, the type must invalid, since a sensible type should always end with a ")" if it contains parenthesis
    if lastParenthesis == "(":
        return False
    return True