from discord.guild import Guild
from db import db
from logs.log import print
def add_prefix_to_guild_if_none(guild: Guild):
    #Called on_guild_join
    #Sets the prefix of a guild to the default prefix if it doesn't have one
    result = db.get_prefix(guild.id)
    if result is None:
        db.add_prefix(guild.id)

def remove_deleted_channels_from_db(guild: Guild):
    #Removes deleted channels from the DB that the bot might have previously been tracking when it was in the guild previously
    counting_channel_ids = db.get_channels(guild.id)
    for counting_channel_id in counting_channel_ids:
        exists = False
        for voiceChannel in guild.voice_channels:
            if str(counting_channel_id) == str(voiceChannel.id):
                exists = True
        if exists is False:
            #Remove it from the DB
            db.delete_channel(counting_channel_id)

async def print_and_send(ctx, message):
    #Prints and sends a message --- This func is here to make it so I don't have to do both one after the other constantly
    print(message)
    await ctx.send(message)
#These two functions are using in the cleanupType func in CountingChannels.py
def remove_parenthesis(word):
    opening_parenthesis = 0
    while word[opening_parenthesis] == "(":
        opening_parenthesis += 1
        word = word[1:]
    closing_parenthesis = 0
    for char in range(len(word)-1, 0, -1):
        if word[char] != ")":
            break
        closing_parenthesis += 1
        word = word[:-1]
    return word, opening_parenthesis, closing_parenthesis


def add_parenthesis(word, opening_parenthesis, closing_parenthesis):
    for x in range(opening_parenthesis):
        word = "(" + word
    for y in range(closing_parenthesis):
        word = word + ")"
    return word

def check_parenthesis(type):
    #Checks if the parenthesis in a type makes sense
    parenthesis = 0
    words = type.split()
    last_parenthesis = ""
    for word in words:
        for char in word:
            if char == "(":
                last_parenthesis = "("
                parenthesis += 1
            elif char == ")":
                last_parenthesis = ")"
                parenthesis -= 1
    if parenthesis != 0:
        #If there are more of one type of parenthesis than the other, we have a problem
        return False
    #Next we'll check if the last parenthesis is a "(". If it is, the type must invalid, since a sensible type should always end with a ")" if it contains parenthesis
    if last_parenthesis == "(":
        return False
    return True