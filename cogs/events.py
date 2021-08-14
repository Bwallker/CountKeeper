from inspect import EndOfBlock
from discord.abc import GuildChannel
from discord.channel import VoiceChannel
from discord.errors import DiscordException
from discord.ext.commands import Cog, Bot
from discord.guild import Guild
from discord.member import Member
import discord
from db import db
from cogs import event_helpers
from utils import utils
from logs.log import print
import patterns.channels_manager as channel_manager
from patterns.simple_discord import SimpleMessage


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
        embeds = event_helpers.guild_join_message(self.bot.user.avatar_url)
        for embed in embeds:
            try:
                await inviter.send(embed=embed)
            except DiscordException as e:
                print(embed.__repr__())
                print(embed.__str__())
                print(e.__repr__())
                print(e.__str__())

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
        guild: Guild = before.guild
        if before.roles == after.roles:
            return
        before_set = set(before.roles)
        after_set = set(after.roles)
        before_but_not_after = before_set - after_set
        after_but_not_before = after_set - before_set
        await self.bot.send_to_notified(guild, SimpleMessage(content=f"Member {after.display_name} in guild {after.guild.name} has lost the following roles:"))
        print(
            f"Member {after.display_name} in guild {after.guild.name} has lost the following roles:")
        for role in before_but_not_after:
            print(role.name)
            await self.bot.send_to_notified(guild, SimpleMessage(content=role.name))
        await self.bot.send_to_notified(guild, SimpleMessage(content=f"Member {after.display_name} in guild {after.guild.name} has gained the following roles:"))
        print(
            f"Member {after.display_name} in guild {after.guild.name} has gained the following roles:")
        for role in after_but_not_before:
            print(role.name)
            await self.bot.send_to_notified(guild, SimpleMessage(content=role.name))
        await channel_manager.update_channels(guild, self.bot.get_notified_channel(guild))

    @Cog.listener('on_member_join')
    async def on_member_join(self, member: Member):
        guild: Guild = member.guild
        await self.bot.send_to_notified(guild, SimpleMessage(content=f"Member {member.display_name} joined guild {member.guild.name}"))
        print(f"Member {member.display_name} joined guild {member.guild.name}")
        await channel_manager.update_channels(guild, self.bot.get_notified_channel(guild))

    @Cog.listener('on_member_remove')
    async def on_member_remove(self, member: Member):
        guild: Guild = member.guild
        print(f"Member {member.display_name} left guild {member.guild.name}")
        await self.bot.send_to_notified(guild, SimpleMessage(content=f"Member {member.display_name} left guild {member.guild.name}"))
        await channel_manager.update_channels(member.guild, self.bot.get_notified_channel(guild))

    @Cog.listener('on_guild_channel_delete')
    async def on_guild_channel_delete(self, channel: GuildChannel):
        print(f"Channel {channel.name} deleted in guild {channel.guild.name}")
        await self.bot.send_to_notified(channel.guild, SimpleMessage(content=f"Channel {channel.name} deleted in guild {channel.guild.name}"))
        db.remove_pattern(channel.id)
