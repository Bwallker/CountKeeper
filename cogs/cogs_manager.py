from discord.ext.commands import Cog, Bot, command, Context
from discord.ext.commands.core import is_owner, is_owner
import os

from discord.ext.commands.errors import CommandError, MissingRequiredArgument, NotOwner, TooManyArguments


class CogsManager(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @is_owner()
    @command(name="load")
    async def load(self, ctx: Context, cog_name: str, path_to_cogs: str = f'{os.getcwd()}/cogs'):
        self.load_helper(cog_name, path_to_cogs)

    def load_brief_text(self, _: str) -> str:
        return "Loads a cog"

    def load_help_text(self, _: str) -> str:
        self.load_brief_text(_)

    def load_helper(self, cog_name: str, path_to_cogs: str = f'{os.getcwd()}/cogs'):
        cog = self.bot.find_cog(cog_name, path_to_cogs)
        self.bot.add_cog(cog(self))

    @load.error
    async def load_error(self, ctx: Context, error: CommandError):
        if isinstance(error, NotOwner):
            await ctx.send("You must be the bot owner to use this command")
        elif isinstance(error, MissingRequiredArgument):
            await ctx.send("You must supply the name of the cog to load")
        elif isinstance(error, TooManyArguments):
            await ctx.send(
                "You gave more than 1 arguments to this command, even though it only takes oen")

    @is_owner()
    @command(name="unload")
    async def unload(self, ctx: Context, cog_name: str):
        self.unload_helper(cog_name)

    def unload_brief_text(self, _: str) -> str:
        return "Unloads a cog"

    def unload_help_text(self, _: str) -> str:
        return self.unload_brief_text(_)

    def unload_helper(self, cog_name):
        self.bot.remove_cog(cog_name)

    @unload.error
    async def unload_error(self, ctx: Context, error: CommandError):
        if isinstance(error, NotOwner):
            await ctx.send("You must be the bot owner to use this command")
        elif isinstance(error, MissingRequiredArgument):
            await ctx.send("You must supply the name of the cog to unload")
        elif isinstance(error, TooManyArguments):
            await ctx.send(
                "You gave more than 1 arguments to this command, even though it only takes oen")
