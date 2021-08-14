from discord import Guild
from discord.channel import TextChannel
from db import db
from logs.log import print


def get_notified_channel(guild: Guild):
    """
        Returns the notification channel for the guild
    """
    notified_channel_id = db.get_notification_channel(guild.id)
    if notified_channel_id is None:
        return None
    channel: TextChannel
    for channel in guild.text_channels:
        if channel.id == notified_channel_id:
            return channel
    db.remove_notification_channel(guild.id)
    return None


async def send_to_notified_channel(guild: Guild, message: str) -> bool:
    """
        Sends a message to the notification channel of the guild
        Returns a bool representing whether the guild has a notification channel
    """
    notified_channel = get_notified_channel(guild)
    if notified_channel is None:
        return
    await notified_channel.send(message)


async def print_and_send(guild: Guild, message: str) -> None:
    """
        Sends a message to the notification channel of the guild and logs and prints it
    """
    await send_to_notified_channel(guild, message)
    print(message)
