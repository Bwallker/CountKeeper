from discord.abc import GuildChannel
from discord.channel import VoiceChannel
from discord.ext.commands import Cog, Bot
from discord.guild import Guild
from discord.member import Member
import discord
from db import db
from cogs import event_helpers
from utils import utils
from logs.log import print


class Events(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener('on_guild_join')
    async def on_guild_join(self, guild: Guild):
        utils.add_prefix_to_guild_if_none(guild)
        utils.remove_deleted_channels_from_db(guild)
        print(f"Bot joined guild {guild.name} (ID:) {guild.id}")
        logs = await guild.audit_logs(limit=1, action=discord.AuditLogAction.bot_add).flatten()
        inviter = logs[0].user
        await inviter.send(embed=event_helpers.guild_join_message(inviter, guild))

    @Cog.listener('on_guild_leave')
    async def on_guild_leave(self, guild):
        print(f"Bot left guild {guild.name} (ID:) {guild.id}")

    @Cog.listener('on_message')
    async def on_message(self, message):
        if not message.mentions:
            return
        for mention in message.mentions:
            if mention == self.bot.user:
                prefix = db.get_prefix(message.guild.id)
                await message.channel.send(f"My prefix for this server is: {prefix}")

    @Cog.listener('on_member_update')
    async def on_member_update(self, before: Member, after: Member):
        if before.roles == after.roles:
            return
        before_set = set(before.roles)
        after_set = set(after.roles)
        before_but_not_after = before_set - after_set
        after_but_not_before = after_set - before_set
        print(f"Member {after.display_name} in guild {after.guild.name} has lost the following roles:")
        for role in before_but_not_after:
            print(role.name)
        print(f"Member {after.display_name} in guild {after.guild.name} has gained the following roles:")
        for role in after_but_not_before:
            print(role.name)
        # if before.roles != after.roles:
        # await counting_channels.calculate_channels(after, "role changed", None, after.guild)

    @Cog.listener('on_member_join')
    async def on_member_join(self, member: Member):
        print(f"Member {member.display_name} joined guild {member.guild.name}")
        # await counting_channels.calculate_channels(member, "member joined", None, member.guild)

    @Cog.listener('on_member_remove')
    async def on_member_remove(self, member: Member):
        print(f"Member {member.display_name} left guild {member.guild.name}")
        # await counting_channels.calculate_channels(member, "member left", None, member.guild)

    @Cog.listener('on_guild_channel_delete')
    async def on_guild_channel_delete(self, channel: GuildChannel):
        print(f"Channel {channel.name} deleted in guild {channel.guild.name}")
        # if not isinstance(channel, VoiceChannel): return
        #pattern = db.get_pattern(channel.id)
        # if pattern != None:
        # db.delete_channel(channel.id)
        #print(f"Counting Channel {channel} deleted in guild {channel.guild}")
