import discord
from discord.channel import VoiceChannel
from db import db
from utils import utils
from logs.log import print
# This file contains helper functions for updating the channels

valid_operands = (
    "and",
    "nand",
    "or",
    "nor",
    "xor",
    "nxor"
)


async def calculate_channels(member, mode, ctx, guild):
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
    sum_of_patterns = {}
    sum_of_patterns["norole"] = 0
    for role in guild.roles:
        sum_of_patterns[str(role.id)] = 0
    for member in guild.members:
        number_of_patterns = 0
        for role in member.roles:
            number_of_patterns += 1
            sum_of_patterns[str(role.id)] += 1
        if number_of_patterns == 1:
            # Every member has at least one role: @everyone
            sum_of_patterns["norole"] += 1

    channel_patterns = db.get_channel_patterns(guild.id)
    if channel_patterns is not None:
        for channelId in channel_patterns:
            role = channel_patterns.get(channelId)
            role_number = sum_of_patterns.get(role)
            channel: VoiceChannel
            for channel in guild.voice_channels:
                if channel.id == channelId:
                    break

            await update_channel(channel, role_number, guild)

    print(f"Channels updated in guild {guild}!")
    if (mode == "forced update"):
        await ctx.send("Channels updated!")


async def update_channel(channel, role_number, guild):
    first_number = None
    words = channel.name.split()
    for i, word in enumerate(words):
        if word.isdigit():
            first_number = word
            words[i] = str(role_number)
            break
    words = " ".join(words)
    print(words)
    output = None
    if first_number is None:
        output = channel.name + str(role_number)
    else:
        output = words
    previous_name = channel.name
    try:
        await channel.edit(name=output)
        print(f"channel {previous_name} renamed to {channel.name} in guild {guild}")
    except discord.errors.Forbidden as e:
        print(f"discord Forbidden exception raised while trying to rename channel {previous_name} in guild {guild.name}")
    


def clean_up_pattern(ctx, pattern):
    global valid_operands
    pattern = str(pattern)
    pattern = pattern.lower()
    words = pattern.split()
    for i, word in enumerate(words):
        word, opening_parenthesis, closing_parenthesis = utils.remove_parenthesis(word)
        is_everyone = False
        if word == "@everyone":
            word = ctx.guild.default_role.id
            is_everyone = True
        word = word.lower()
        is_role = False
        try:
            if is_everyone is True:
                raise Exception()
                #So we don't waste time checking if it's a role
                #I also just relized this try except blocks eats keyboard interupts, but it shouldn't run for long enough for that to really be a problem.
            maybe_role = word[3:-1]
            for role in ctx.guild.roles:
                role_id = str(role.id)
                if role_id == maybe_role:
                    is_role = True
                    break
            if is_role is True:
                word = maybe_role
        except:
            pass
        word = utils.add_parenthesis(word, opening_parenthesis, closing_parenthesis)
        words[i] = word
    pattern = " ".join(words)
    return pattern

def role_validity_checker(ctx, input):
    #DEPRECATED. Used to be in use when types only consisted of a role for the bot to track
    if isinstance(input, str) is False:
        return False
    words = input.split()
    if len(words) != 1:
        return False
    is_role = False
    for role in ctx.guild.roles:
        role_id = str(role.id)
        if role_id == input:
            is_role = True
            break
    if is_role:
        return True
    if (input == "norole"):
        return True
    if (input == "@everyone"):
        return True
    return False
