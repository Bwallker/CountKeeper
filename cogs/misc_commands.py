from typing import Union
from discord.ext.commands.errors import CommandError, MissingRequiredArgument
from db.DBError import DBError
from db import db
from discord.ext import commands, tasks
from discord.ext.commands import Cog, Bot, command, Context
import discord
from discord import message as msg
from patterns import counting_channels
from utils import discord_utils, utils
from logs.log import print
from utils import discord_utils

class MiscCommands(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @command
    async def prefix(self, ctx: Context, prefix: str = None):
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

    def prefix_help_text(self, prefix):
        return f"The prefix command changes the prefix of your server. To change prefix, you must supply a new prefix as an argument.\nThe command call should look like {prefix}prefix !\n\nAssuming you want to change your prefix to !"

    def prefix_brief_text(self, _):
        return "Command for changing the bot prefix for your server"
    @prefix.error
    async def prefix_error(self, ctx: Context, error: CommandError):
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

    @command
    async def notify(self, ctx: Context, channel_id_or_name: Union[int, str]):
        try:
            channel_id = int(channel_id_or_name)
            channel = discord_utils.get(
                lambda channel, channelId: channel.id == channelId, ctx.guild.text_channels, channel_id)
            if channel is None:
                raise ValueError()
        except ValueError as e:
            channel_name = str(channel_id_or_name)
            channel = discord_utils.get(
                lambda channel, channelName: channel.name == channelName, ctx.guild.text_channels, channel_name)
            if channel is None:
                raise discord.InvalidArgument(
                    "The channel name or id you have provided is invalid")
        db.add_notification_channel(channel.guild.id, channel.id)
        message = f'Notification channel has been been set to channel with ID of ({str(channel.id)}) and name of ({channel.name}) in guild {channel.guild.name}'
        await utils.print_and_send(ctx, message)


    def notify_help_text(self, _):
        return "Sets the notification channel for your guild. Takes either the name or the id of the channel as an argument"

    def notify_brief_text(self, _):
        return "Sets the notification channel for your guild"

    @notify.error
    async def notify_error(self, ctx, error):
        if isinstance(error, MissingRequiredArgument):
            message = "You did not include a channel name or ID"
            message += self.notify_help_text("")
            ctx.send(message)
        else:
            raise error
# -----------------------------------------------------------------------------------------


async def list_guilds(ctx, bot):
    print("Printing guild names...")
    for guild in bot.guilds:
        print("Guild name: " + guild.name)
        print("Guild ID: " + str(guild.id))
        print()
    print("Done printing guilds")


async def list_guilds_error(ctx, error):
    if isinstance(error, commands.NotOwner):
        await ctx.send("You must be the bot owner to use this command")
    elif isinstance(error, commands.TooManyArguments):
        await ctx.send("You gave this command arguments, even though it doesn't take any")
    else:
        raise error
# -----------------------------------------------------------------------------------------


async def list_channels_in_all_guilds(ctx, bot):
    print("Printing channels in guild...")
    for guild in bot.guilds:
        print("Printing channels in guild " + guild.name)
        i = 0
        for channel in guild.voice_channels:
            i += 1
            print("Channel number " + str(i) + ": \n")
            print("\tChannel name: " + channel.name)
            print("\tChannel id: " + str(channel.id))
            print("Done printing channel number " + str(i))
        print("Done printing channels in guild " + guild.name)


async def list_channels_in_all_guilds_error(ctx, error):
    if isinstance(error, commands.NotOwner):
        await ctx.send("You must be the bot owner to use this command")
    elif isinstance(error, commands.TooManyArguments):
        await ctx.send("You gave this command arguments, even though it doesn't take any")
    else:
        raise error
# -----------------------------------------------------------------------------------------


async def list_roles(ctx):
    await utils.print_and_send(ctx, f"Listing roles in guild {ctx.guild.name}...")
    i = 0
    message = ""
    for role in ctx.guild.roles:
        i += 1
        message += f"Role number {i} in guild {ctx.guild.name}:\n"
        message += f"\tRole name: {role.name}\n"
        message += f"\tRole ID: {role.id}\n"
    await utils.print_and_send(ctx, message)


async def listRolesError(ctx, error):
    if isinstance(error, commands.TooManyArguments):
        await ctx.send("You gave this command arguments, even though it doesn't take any")
