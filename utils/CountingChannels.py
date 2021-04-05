import discord
from utils import sqlite3
#This file contains helper functions for updating the channels
async def calculateChannels(member, mode, ctx, guild):
    if mode == "startup":
        print(f"Performing startup updates for channels in guild: {guild.name}")
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
            #Every member has at least one role: @everyone
            sumOfRoles["norole"] += 1

    channelRoles = sqlite3.getChannelRoles(guild.id)
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
    await channel.edit(name=output)
    print(f"channel {previousName} renamed to {channel.name} in guild {guild}")

def roleValidityChecker(ctx, input):
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
    if (input == "everyone"):
        return True
    return False