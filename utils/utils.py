from discord.guild import Guild
from db import db
from logs.log import print


def add_prefix_to_guild_if_none(guild: Guild):
    # Called on_guild_join
    # Sets the prefix of a guild to the default prefix if it doesn't have one
    result = db.get_prefix(guild.id)
    if result is None:
        db.add_prefix(guild.id)


def remove_deleted_channels_from_db(guild: Guild):
    # Removes deleted channels from the DB that the bot might have previously been tracking when it was in the guild previously
    counting_channel_ids = db.get_channels(guild.id)
    for counting_channel_id in counting_channel_ids:
        exists = False
        for voice_channel in guild.voice_channels:
            if str(counting_channel_id) == str(voice_channel.id):
                exists = True
        if exists is False:
            # Remove it from the DB
            db.remove_pattern(counting_channel_id)


async def print_and_send(ctx, message):
    # Prints and sends a message --- This func is here to make it so I don't have to do both one after the other constantly
    print(message)
    await ctx.send(message)

