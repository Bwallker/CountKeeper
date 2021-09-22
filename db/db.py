from pattern_parts.components import Component
import db.pickle_handler as pickle_handler
from utils import config
from logs.log import print
from unittest.signals import installHandler
import sqlite3
DEFAULT_PREFIX = config.DEFAULT_PREFIX
PATH_TO_PREFIXES = "count_keeper_data/prefixes.sqlite"
PATH_TO_CHANNELS = "count_keeper_data/channels.sqlite"
PATH_TO_NOTIFIED = "count_keeper_data/notified.sqlite"


def get_prefix(guild_id: int) -> str:
    global PATH_TO_PREFIXES
    try:
        prefixes = sqlite3.connect(PATH_TO_PREFIXES)
        cursor = prefixes.cursor()
        guild_id = str(guild_id)
        cursor.execute(
            """SELECT prefix FROM prefixes WHERE guild_id = ?""", (guild_id,))
        # cursor.fetchone() returns a tuple containing one item
        prefix = cursor.fetchone()
    except sqlite3.OperationalError:
        prefix = None
    if prefix is not None:
        prefix = prefix[0]
    cursor.close()
    prefixes.close()
    return prefix


def add_prefix(guild_id: int) -> bool:
    global DEFAULT_PREFIX, PATH_TO_PREFIXES
    guild_id = str(guild_id)
    try:
        prefixes = sqlite3.connect(PATH_TO_PREFIXES)
        cursor = prefixes.cursor()
        cursor.execute(
            """INSERT INTO prefixes (guild_id, prefix) VALUES(?,?)""", (guild_id, DEFAULT_PREFIX))
        prefixes.commit()
        successful = True
    except sqlite3.OperationalError:
        successful = False
    except sqlite3.Error as e:
        cursor.close()
        prefixes.close()
        raise e
    cursor.close()
    prefixes.close()
    return successful


def change_prefix(guild_id: int, prefix: str) -> bool:
    global PATH_TO_PREFIXES
    if get_prefix(guild_id) is None:
        return add_prefix(guild_id)
    try:
        prefixes = sqlite3.connect(PATH_TO_PREFIXES)
        cursor = prefixes.cursor()
        cursor.execute(
            """UPDATE prefixes SET prefix = ? WHERE guild_id = ?""", (prefix, guild_id))
        prefixes.commit()
        successful = True
    except sqlite3.OperationalError:
        successful = False
    except sqlite3.Error as e:
        cursor.close()
        prefixes.close()
        raise e
    cursor.close()
    prefixes.close()
    return successful


def remove_prefix(guild_id: int) -> bool:
    global PATH_TO_PREFIXES
    try:
        prefixes = sqlite3.connect(PATH_TO_PREFIXES)
        cursor = prefixes.cursor()
        cursor.execute(
            """DELETE FROM prefixes WHERE guild_id = ?""", (guild_id,))
        prefixes.commit()
        successful = True
    except sqlite3.OperationalError:
        successful = False
    except sqlite3.Error as e:
        cursor.close()
        prefixes.close()
        raise e
    cursor.close()
    prefixes.close()
    return successful


def get_pattern(channel_id: int) -> Component:
    global PATH_TO_CHANNELS
    channels = sqlite3.connect(PATH_TO_CHANNELS)
    cursor = channels.cursor()
    try:
        cursor.execute(
            """SELECT pattern FROM channels WHERE channel_id = ?""", (channel_id,))
        pattern = cursor.fetchone()
        if pattern is not None:
            pattern = pattern[0]
            pattern = pickle_handler.unpickle_pattern(pattern)
    except sqlite3.OperationalError:
        cursor.close()
        channels.close()
        return None
    except sqlite3.Error as e:
        cursor.close()
        channels.close()
        raise e
    cursor.close()
    channels.close()
    return pattern


def add_pattern(guild_id: int, channel_id: int, pattern: Component) -> bool:
    global PATH_TO_CHANNELS
    as_bytes = pickle_handler.pickle_pattern(pattern)
    try:
        channels = sqlite3.connect(PATH_TO_CHANNELS)
        cursor = channels.cursor()
        cursor.execute("""INSERT INTO channels (guild_id, channel_id, pattern) VALUES(?,?,?)""",
                       (guild_id, channel_id, as_bytes))
        channels.commit()
        successful = True
    except sqlite3.OperationalError:
        successful = False
    except sqlite3.Error as e:
        cursor.close()
        channels.close()
        raise e
    cursor.close()
    channels.close()
    return successful


def change_pattern(guild_id: int, channel_id: int, pattern: Component) -> bool:
    global PATH_TO_CHANNELS
    as_bytes = pickle_handler.pickle_pattern(pattern)
    if get_pattern(channel_id) is None:
        return add_pattern(guild_id, channel_id, pattern)
    try:
        channels = sqlite3.connect(PATH_TO_CHANNELS)
        cursor = channels.cursor()
        cursor.execute(
            """UPDATE channels SET pattern = ? WHERE channel_id = ?""", (as_bytes, channel_id))
        channels.commit()
        successful = True
    except sqlite3.OperationalError:
        successful = False
    except sqlite3.Error as e:
        cursor.close()
        channels.close()
        raise e
    cursor.close()
    channels.close()
    return successful


def remove_pattern(channel_id: int) -> bool:
    global PATH_TO_CHANNELS
    try:
        channels = sqlite3.connect(PATH_TO_CHANNELS)
        cursor = channels.cursor()
        cursor.execute(
            """DELETE FROM channels WHERE channel_id = ?""", (channel_id,))
        channels.commit()
        successful = True
    except sqlite3.OperationalError:
        successful = False
    except sqlite3.Error as e:
        cursor.close()
        channels.close()
        raise e
    cursor.close()
    channels.close()
    return successful


def get_channel_patterns(guild_id: int) -> dict[int, Component]:
    global PATH_TO_CHANNELS
    channels = sqlite3.connect(PATH_TO_CHANNELS)
    cursor = channels.cursor()
    try:
        cursor.execute(
            """SELECT channel_id, pattern FROM channels WHERE guild_id = ?""", (guild_id,))
        channel_ids = cursor.fetchall()
    except sqlite3.OperationalError:
        cursor.close()
        channels.close()
        return {}
    except sqlite3.Error as e:
        cursor.close()
        channels.close()
        raise e
    as_dict = {}
    for channel_id_and_pattern in channel_ids:
        channel_id = channel_id_and_pattern[0]
        pattern = pickle_handler.unpickle_pattern(channel_id_and_pattern[1])
        as_dict[channel_id] = pattern
    cursor.close()
    channels.close()
    return as_dict


def get_channels(guild_id: int) -> list[int]:
    global PATH_TO_CHANNELS
    guild_id = str(guild_id)
    channels = sqlite3.connect(PATH_TO_CHANNELS)
    cursor = channels.cursor()
    try:
        cursor.execute(
            """SELECT channel_id FROM channels WHERE guild_id = ?""", (guild_id,))
        channel_ids = cursor.fetchall()
        for i, channel_id in enumerate(channel_ids):
            channel_ids[i] = channel_id[0]
    except sqlite3.OperationalError:
        channel_ids = []
    except sqlite3.Error as e:
        cursor.close()
        channels.close()
        raise e
    cursor.close()
    channels.close()
    return channel_ids


def add_notification_channel(guild_id: int, channel_id: int) -> bool:
    global PATH_TO_NOTIFIED
    try:
        notified = sqlite3.connect(PATH_TO_NOTIFIED)
        cursor = notified.cursor()
        cursor.execute(
            """INSERT INTO notified (guild_id, channel_id) VALUES(?,?)""", (guild_id, channel_id))
        notified.commit()
        successful = True
    except sqlite3.OperationalError:
        successful = False
    except sqlite3.Error as e:
        cursor.close()
        notified.close()
        raise e
    cursor.close()
    notified.close()
    return successful


def change_notification_channel(guild_id: int, new_channel_id: int) -> bool:
    global PATH_TO_NOTIFIED
    try:
        notified = sqlite3.connect(PATH_TO_NOTIFIED)
        cursor = notified.cursor()
        cursor.execute(
            """UPDATE notified SET channel_id = ? WHERE guild_id = ?""", (new_channel_id, guild_id))
        notified.commit()
        successful = True
    except sqlite3.OperationalError:
        successful = False
    except sqlite3.Error as e:
        cursor.close()
        notified.close()
        raise e
    cursor.close()
    notified.close()
    return successful


def remove_notification_channel(guild_id: int) -> bool:
    global PATH_TO_NOTIFIED
    try:
        notified = sqlite3.connect(PATH_TO_NOTIFIED)
        cursor = notified.cursor()
        cursor.execute(
            """DELETE FROM notified WHERE guild_id = ?""", (guild_id,))
        notified.commit()
        successful = True
    except sqlite3.OperationalError:
        successful = False
    except sqlite3.Error as e:
        cursor.close()
        notified.close()
        raise e
    cursor.close()
    notified.close()
    return successful


def get_notification_channel(guild_id: int) -> int:
    global PATH_TO_NOTIFIED
    try:
        notified = sqlite3.connect(PATH_TO_NOTIFIED)
        cursor = notified.cursor()
        cursor.execute(
            """SELECT channel_id FROM notified WHERE guild_id = ?""", (
                guild_id,)
        )
        channel_id = cursor.fetchone()
        if channel_id is not None:
            channel_id = channel_id[0]
    except sqlite3.OperationalError:
        channel_id = None
    except sqlite3.Error as e:
        cursor.close()
        notified.close()
        raise e
    cursor.close()
    notified.close()
    return channel_id


def get_all_channel_patterns() -> dict[int, Component]:
    global PATH_TO_CHANNELS
    channels = sqlite3.connect(PATH_TO_CHANNELS)
    cursor = channels.cursor()
    try:
        cursor.execute(
            """SELECT channel_id, pattern FROM channels""")
        channel_ids = cursor.fetchall()
    except sqlite3.OperationalError:
        cursor.close()
        channels.close()
        return None
    except sqlite3.Error as e:
        cursor.close()
        channels.close()
        raise e
    as_dict = {}
    for channel_id_and_pattern in channel_ids:
        channel_id = channel_id_and_pattern[0]
        pattern = pickle_handler.unpickle_pattern(channel_id_and_pattern[1])
        as_dict[channel_id] = pattern
    cursor.close()
    channels.close()
    return as_dict


def update_channels():
    all_patterns = get_all_channel_patterns()
    for key, value in all_patterns.items():
        print(key)
        print(value.to_dict())
