from typing import Union
from discord.channel import TextChannel
from discord.ext.commands.errors import CommandError, MissingRequiredArgument
from discord.guild import Guild
from db.DBError import DBError
from db import db
from discord.ext import commands
from discord.ext.commands import Cog, Bot, command, Context
import discord

from utils import utils
from logs.log import print

class MiscCommands(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @command(name="prefix")
    async def prefix(self, ctx: Context, prefix: str = None) -> None:
        if prefix is None:
            guild_prefix = db.get_prefix(ctx.guild.id)
            ctx.send(f"The prefix for your server is {guild_prefix}")
            return
        prefix = str(prefix)
        successful = db.change_prefix(ctx.guild.id, prefix)
        if not successful:
            raise DBError()
        print(f"prefix updated to {prefix} in guild: {ctx.guild.name}")
        message = f"Prefix changed to ( {prefix} )"
        await ctx.send(message)

    def prefix_help_text(self, prefix: str) -> str:
        return f"The prefix command changes the prefix of your server. To change prefix, you must supply a new prefix as an argument.\nThe command call should look like {prefix}prefix !\n\nAssuming you want to change your prefix to !"

    def prefix_brief_text(self, _: str) -> str:
        return "Command for changing the bot prefix for your server"

    @prefix.error
    async def prefix_error(self, ctx: Context, error: CommandError) -> None:
        if isinstance(error, commands.MissingRequiredArgument):
            prefix = db.get_prefix(ctx.guild.id)
            answer = self.prefix_help_text(prefix)
            await ctx.send(answer)
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(
                "To change prefix for the bot you must have the manage server permission"
            )
        elif isinstance(error, DBError):
            await ctx.send("A database error occured while changing the prefix for your server! Try setting it to a different one")
        else:
            raise error
# -----------------------------------------------------------------------------------------

    @command(name="notify")
    async def notify(self, ctx: Context, channel_id_or_name: Union[int, str]) -> None:
        channel: TextChannel
        try:
            channel_id = int(channel_id_or_name)
            channel = [
                channel for channel in ctx.guild.text_channels if channel.id == channel_id][0]
            if channel is None:
                raise ValueError
        except ValueError:
            channel_name = str(channel_id_or_name)
            channel = [
                channel for channel in ctx.guild.text_channels if channel.name == channel_name][0]
            if channel is None:
                raise discord.InvalidArgument(
                    "The channel name or id you have provided is invalid")

        if db.get_notification_channel(channel.guild.id) is None:
            successful = db.add_notification_channel(
                channel.guild.id, channel.id)
        else:
            successful = db.change_notification_channel(
                channel.guild.id, channel.id)
        if successful:
            message = f'Notification channel has been been set to channel with ID of ({str(channel.id)}) and name of ({channel.name}) in guild {channel.guild.name}'
        else:
            message = "A DB error occured while changing the notification channel in your server"
        await utils.print_and_send(ctx, message)

    def notify_help_text(self, _: str) -> str:
        return "Sets the notification channel for your guild. Takes either the name or the id of the channel as an argument"

    def notify_brief_text(self, _: str) -> str:
        return "Sets the notification channel for your guild"

    @notify.error
    async def notify_error(self, ctx: Context, error: CommandError) -> None:
        if isinstance(error, MissingRequiredArgument):
            message = "You did not include a channel name or ID"
            message += self.notify_help_text("")
            await ctx.send(message)
        else:
            raise error
# -----------------------------------------------------------------------------------------

    @command(name="list_guilds")
    async def list_guilds(self, _: Context) -> None:
        print("Printing guild names...")
        guild: Guild
        for guild in self.bot.guilds:
            print("Guild name: " + guild.name)
            print("Guild ID: " + str(guild.id))
        print("Done printing guilds")

    def list_guilds_brief_text(self, _: str) -> str:
        return "Lists all the guilds the bot is in. Only usable by the bot owner"

    def list_guilds_help_text(self, _: str) -> str:
        return self.list_guilds_brief_text(_)

    @list_guilds.error
    async def list_guilds_error(self, ctx: Context, error: CommandError) -> None:
        if isinstance(error, commands.NotOwner):
            await ctx.send("You must be the bot owner to use this command")
        elif isinstance(error, commands.TooManyArguments):
            await ctx.send("You gave this command arguments, even though it doesn't take any")
        else:
            raise error
# -----------------------------------------------------------------------------------------

    @command(name="list_channels_in_all_guilds")
    async def list_channels_in_all_guilds(self, _: Context) -> None:
        print("Printing channels in guild...")
        for guild in self.bot.guilds:
            print("Printing channels in guild " + guild.name)
            i = 0
            for channel in guild.voice_channels:
                i += 1
                print("Channel number " + str(i) + ": \n")
                print("\tChannel name: " + channel.name)
                print("\tChannel id: " + str(channel.id))
                print("Done printing channel number " + str(i))
            print("Done printing channels in guild " + guild.name)

    def list_channels_in_all_guilds_brief_text(self, _: str) -> str:
        return "Lists all the channels in all guilds the bot is in. Only usable by the bot owner"

    def list_channels_in_all_guilds_help_text(self, _: str) -> str:
        return self.list_channels_in_all_guilds_brief_text(_)

    @list_channels_in_all_guilds.error
    async def list_channels_in_all_guilds_error(self, ctx: Context, error: CommandError) -> None:
        if isinstance(error, commands.NotOwner):
            await ctx.send("You must be the bot owner to use this command")
        elif isinstance(error, commands.TooManyArguments):
            await ctx.send("You gave this command arguments, even though it doesn't take any")
        else:
            raise error
# -----------------------------------------------------------------------------------------

    @command(name="list_roles")
    async def list_roles(self, ctx: Context) -> None:
        await utils.print_and_send(ctx, f"Listing roles in guild {ctx.guild.name}...")
        i = 0
        message = ""
        for role in ctx.guild.roles:
            i += 1
            message += f"Role number {i} in guild {ctx.guild.name}:\n"
            message += f"\tRole name: {role.name}\n"
            message += f"\tRole ID: {role.id}\n"
        await utils.print_and_send(ctx, message)

    def list_roles_brief_text(self, _: str) -> str:
        return "Lists all the roles in your server. Doesn't take any arguments"

    def list_roles_help_text(self, _: str) -> str:
        return self.list_roles_brief_text(_)

    @list_roles.error
    async def list_roles_error(self, ctx: Context, error: CommandError) -> None:
        if isinstance(error, commands.TooManyArguments):
            await ctx.send("You gave this command arguments, even though it doesn't take any")
        else:
            raise error

# -----------------------------------------------------------------------------------------

    @command(name="ape")
    async def ape(self, ctx: Context, string: str) -> None:
        await ctx.send(string)
        print(string)

    def ape_brief_text(self, _: str) -> str:
        return "Sends back your argument as a response"

    def ape_help_text(self, _: str) -> str:
        return self.ape_brief_text(_)

    @ape.error
    async def ape_error(self, ctx: Context, error: CommandError) -> None:
        if isinstance(error, commands.TooManyArguments):
            await ctx.send("You gave this command more than one arguments")
        elif isinstance(error, MissingRequiredArgument):
            await ctx.send("You didn't give this command anything to ape")
        else:
            raise error
