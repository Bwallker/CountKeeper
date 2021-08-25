from pattern_parts.simple_component import RoleNotInRolesError
from discord.abc import Messageable
from discord.guild import Guild
from discord.channel import VoiceChannel
from logs.log import print
import db.db as db
from pattern_parser.simple_discord import create_simple_guild
import pattern_parser.counting_channels as counting_channels


async def update_channels(guild: Guild, reply_target: Messageable) -> dict[str, str]:
    """
        Updates all the counting channels in a guild
    """

    simple_guild = create_simple_guild(guild)
    tracked_channels = db.get_channel_patterns(guild.id)
    results: dict[int, int] = {}
    for channel in tracked_channels:
        results[channel] = simple_guild.get_result(tracked_channels[channel])

        channel: VoiceChannel
    changes: dict[str, str] = {}
    for channel in guild.voice_channels:
        if channel.id in tracked_channels:
            try:
                result = await counting_channels.update_channel(channel, results[channel.id], guild)
                changes.update(result)
            except RoleNotInRolesError:
                db.remove_pattern(channel.id)
                await reply_target.send(f"Removed channel {channel.name} from tracked channels because its pattern contained a role that doesn't exist anymore")
    changes_as_str = ""
    for key, value in changes.items():
        changes_as_str += key + " -> " + value + "\n"
    if reply_target is None:
        return
    await reply_target.send(f"Updated counting channels in your server\nSummary:\n{changes_as_str}")


def successful_message(pattern: str, unoptimized_repr: str, optimized_repr: str):
    return f"Pattern parsed successfully!\n\
    \n\
    The pattern you put in was: {pattern}\n\
    \n\
    Below is both the unoptimized and optimized output. It's mostly there incase you want to make sure it all checks out.\n\
    \n\
    Also, this isn't the actual output. It's just its text representation\n\
    Keep in mind that the optimized may look quite different to what you put in. This does not necessarily mean that it is wrong.\n\
    \n\
    \n\
    Here is the unoptimized version: {unoptimized_repr}\n\
    \n\
    Here is the optimized version: {optimized_repr}"
