import discord
from logs.log import print
def guildJoinMessage(inviter, guild):
    title = "Thank you for inviting CountKeeper to your discord server!"
    description = "test"
    color = 0xF5A623
    embed = discord.Embed(title=title, description=description, color=color)
    embed.add_field(name="myTestField", value="value of test field --- not inlined", inline=False)
    embed.add_field(name="myInlineTestField", value="value of inlined test field --- inlined", inline=True)
    return embed
    