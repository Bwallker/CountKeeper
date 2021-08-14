from discord.ext import commands
from discord.ext.commands import Cog, Bot, command
import discord
from discord import Asset
from discord.ext.commands.context import Context
from discord.ext.commands.core import Command
from db import db
from utils import config


class Help(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @command("help")
    async def help(self, ctx: Context, command_name: str = None):
        if command_name is None:
            embed = self.help_generic_embed(
                ctx.guild.id, self.bot.user.avatar_url)
            await ctx.send(embed=embed)
            return
        command_name = command_name.lower().strip()
        exists = False
        for _, cog in self.bot.cogs.items():
            for command in cog.get_commands():
                if command.name == command_name:
                    exists = True
                    break
            if exists:
                break
        if not exists:
            await ctx.send(f"{command_name} is not a valid command")
            return

        embed = self.help_command_embed(
            command_name, ctx.guild.id, self.bot.user.avatar_url)
        await ctx.send(embed=embed)

    def help_brief_text(self, _: str):
        return "Provides descriptions for the commands avialable to the bot"

    def help_help_text(self, _: str):
        return "Briefly describes all the commands avialable to the bot if called without arguments, and provides a detailed description of a command if called with the name of that command as an argument"

    def help_generic_embed(self, guild_id: int, profile_pic: Asset):
        prefix = db.get_prefix(guild_id)
        author_name = config.BOT_NAME
        website = config.BOT_WEBSITE
        embed = discord.Embed(title="Help", url=website, color=0xFC8403)

        embed.set_author(name=author_name, url=website, icon_url=profile_pic)
        cog: Cog
        for name, cog in self.bot.cogs.items():
            not_dunder = [func for func in dir(cog) if not func.startswith(
                "__") and not func.endswith("__")]
            value = f"---COMMANDS---\n\n"
            cog.__class__
            command: Command
            for command in cog.get_commands():
                brief_help_text = cog.__getattribute__(
                    f"{command.name}_brief_text")(prefix)
                value += f"{command.name.upper()}\n{brief_help_text}\n\n"

            embed.add_field(name=name.upper(), value=value, inline=False)
        return embed

    def help_command_embed(self, command_name: str, guild_id: int, profile_pic: Asset):
        prefix = db.get_prefix(guild_id)
        author_name = config.BOT_NAME
        website = config.BOT_WEBSITE
        embed = discord.Embed(url=website, color=0xFC8403)

        embed.set_author(name=author_name, url=website, icon_url=profile_pic)
        value: str = ""

        for name, cog in self.bot.cogs.items():
            for command in cog.get_commands():
                if command.name == command_name:
                    help_text = cog.__getattribute__(
                        f"{command.name}_help_text")(prefix)
                    value = f"\n\n\n{help_text}"

        embed.add_field(
            name=f"{command_name.upper()}", value=value, inline=False)

        return embed
