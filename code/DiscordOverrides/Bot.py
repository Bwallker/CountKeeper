import discord
from discord.ext import commands
from utils.config import TESTER_ID
from logs.log import print
class Bot(commands.Bot):
    async def process_commands(self, message):
        
        if message.author.bot and message.author.id != TESTER_ID:
            return

        ctx = await self.get_context(message)
        await self.invoke(ctx)