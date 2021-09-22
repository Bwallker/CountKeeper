from pattern_parser.simple_discord import create_simple_guild, SimpleGuild
from pattern_parser.pattern import PatternParams
from pattern_parser.pattern_error import PatternError
import pattern_optimizer.optimizer as optimizer
import discord
from discord.ext import commands
from discord.ext.commands import Cog, Bot, command, Context

from discord.ext.commands.errors import CommandError
from discord.guild import Guild
from discord.member import Member

from db import db

from logs.log import print
import pattern_parser.counting_channels as counting_channels
import pattern_parser.channels_manager as channels_manager
import os
import shutil


class CountingChannelsCommands(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @command(name="force_update")
    async def force_update(self, ctx: Context) -> None:
        await channels_manager.update_channels(ctx.guild, ctx)

    def force_update_brief_text(self, _: str) -> str:
        return "Forcably updates all the Counting Channels in your discord server. Should only be used if automatic updates aren't working for some reason"

    def force_update_help_text(self, _: str) -> str:
        return self.force_update_brief_text(_)

    @force_update.error
    async def force_update_error(self, ctx: Context, error: CommandError) -> None:
        if isinstance(error, commands.TooManyArguments):
            await ctx.send("You gave this command arguments even though it doesn't take any")
# -----------------------------------------------------------------------------------------

    @command(name="create")
    async def create(self, ctx: Context, name: str, pattern: str):
        guild: Guild = ctx.guild
        simple_guild = create_simple_guild(guild)

        params = PatternParams(pattern, 0, simple_guild, "")
        try:
            unoptimized_component = counting_channels.pattern_constructor(
                params)
        except PatternError as e:
            await ctx.send(e.__str__())
            return
        optimized_component = optimizer.optimize(unoptimized_component)

        channel = await guild.create_voice_channel(name)
        db.add_pattern(ctx.guild.id, channel.id, optimized_component)

        unoptimized_component_repr = unoptimized_component.__repr__()
        optimized_component_repr = optimized_component.__repr__()

        await ctx.send(channels_manager.successful_message(pattern, unoptimized_component_repr, optimized_component_repr))
        await channels_manager.update_channels(guild, self.bot.get_notified_channel(guild))

    def create_brief_text(self, _: str):
        return "This command creates a new counting channel using the pattern you provided as an argument"

    def create_help_text(self, _: str):
        return self.create_brief_text(_)

    @create.error
    async def create_error(self, ctx: Context, error: CommandError):
        if isinstance(error, commands.TooManyArguments):
            await ctx.send("You gave this command too many arguments")
        else:
            raise error

# -----------------------------------------------------------------------------------------
    @command(name="edit")
    async def edit(self, ctx: Context):
        pass

    def edit_brief_text(self, _: str):
        return "This command edits a new counting channel using the pattern you provided as an argument"

    def edit_help_text(self, _: str):
        return self.create_brief_text(_)

    @edit.error
    async def edit_error(self, ctx: Context, error: CommandError):
        if isinstance(error, commands.TooManyArguments):
            await ctx.send("You gave this command too many arguments")
        else:
            raise error
