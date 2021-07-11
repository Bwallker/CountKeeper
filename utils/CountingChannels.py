import discord
from db import db
from utils import utils
from logs.log import print
# This file contains helper functions for updating the channels

validOperands = (
    "and",
    "nand",
    "or",
    "nor",
    "xor",
    "nxor"
)


async def calculateChannels(member, mode, ctx, guild):
    if mode == "startup":
        print(
            f"Performing startup updates for channels in guild: {guild.name}")
    if mode == "member left":
        print(f"{member} left guild: {guild.name}!")

    elif mode == "member joined":
        print(f"{member} joined guild: {guild.name}!")

    elif mode == "forced update":
        print(f"Forced update commencing in guild: {guild.name}!")

    elif mode == "role changed":
        print(f"{member} updated a role in guild: {guild.name}")
    print("updating channels...")
    sumOfRoles = {}
    sumOfRoles["norole"] = 0
    for role in guild.roles:
        sumOfRoles[str(role.id)] = 0
    for member in guild.members:
        numberOfRoles = 0
        for role in member.roles:
            numberOfRoles += 1
            sumOfRoles[str(role.id)] += 1
        if numberOfRoles == 1:
            # Every member has at least one role: @everyone
            sumOfRoles["norole"] += 1

    channelRoles = db.getChannelTypes(guild.id)
    if channelRoles is not None:
        for channelId in channelRoles:
            role = channelRoles.get(channelId)
            roleNumber = sumOfRoles.get(role)
            targetChannel = None
            for channel in guild.voice_channels:
                if channel.id == channelId:
                    targetChannel = channel

            await updateChannel(targetChannel, roleNumber, guild)

    print(f"Channels updated in guild {guild}!")
    if (mode == "forced update"):
        await ctx.send("Channels updated!")


async def updateChannel(channel, roleNumber, guild):
    firstNumber = None
    words = channel.name.split()
    for i, word in enumerate(words):
        if word.isdigit():
            firstNumber = word
            words[i] = str(roleNumber)
            break
    words = " ".join(words)
    print(words)
    output = None
    if firstNumber is None:
        output = channel.name + str(roleNumber)
    else:
        output = words
    previousName = channel.name
    try:
        await channel.edit(name=output)
        print(f"channel {previousName} renamed to {channel.name} in guild {guild}")
    except discord.errors.Forbidden as e:
        print(f"discord Forbidden exception raised while trying to rename channel {previousName} in guild {guild.name}")
    


def cleanUpType(ctx, type):
    global validOperands
    type = str(type)
    type = type.lower()
    words = type.split()
    for i, word in enumerate(words):
        word, openingParenthesis, closingParenthesis = utils.removeParenthesis(word)
        isEveryone = False
        if word == "@everyone":
            word = ctx.guild.default_role.id
            isEveryone = True
        word = word.lower()
        isRole = False
        try:
            if isEveryone is True:
                raise Exception()
                #So we don't waste time checking if it's a role
                #I also just relized this try except blocks eats keyboard interupts, but it shouldn't run for long enough for that to really be a problem.
            maybeRole = word[3:-1]
            for role in ctx.guild.roles:
                roleId = str(role.id)
                if roleId == maybeRole:
                    isRole = True
                    break
            if isRole is True:
                word = maybeRole
        except:
            pass
        word = utils.addParenthesis(word, openingParenthesis, closingParenthesis)
        words[i] = word
    type = " ".join(words)
    return type

def roleValidityChecker(ctx, input):
    #DEPRECATED. Used to be in use when types only consisted of a role for the bot to track
    if isinstance(input, str) is False:
        return False
    words = input.split()
    if len(words) != 1:
        return False
    isRole = False
    for role in ctx.guild.roles:
        roleId = str(role.id)
        if roleId == input:
            isRole = True
            break
    if isRole:
        return True
    if (input == "norole"):
        return True
    if (input == "@everyone"):
        return True
    return False

def typeValidityChecker(ctx, type):
    if isinstance(type, str) is False:
        return False
    if utils.checkParenthesis(type) is False:
        return False
    
    words = type.split()
    for i, word in enumerate(words):
        word, openingParenthesis, closingParenthesis = utils.removeParenthesis(word)
        
        