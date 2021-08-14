import discord
from logs.log import print
import discord
from discord.member import Member
from discord.guild import Guild
from discord import Asset
import utils.config as config


def guild_join_message(profile_pic: Asset):
    author_name = config.BOT_NAME
    website = config.BOT_WEBSITE
    embeds: list[discord.Embed] = []
    embed = discord.Embed(
        title="Thank you for inviting CountKeeper to your server!", url=website, color=0xFC8403)

    embed.set_author(name=author_name, url=website, icon_url=profile_pic)
    value = \
        "Thank you for choosing CountKeeper!\n\n\
        \
        CountKeeper is a discord bot that counts how many members in your server follow certain patterns, allowing you to create extremely detailed statistics about your discord server\n\n\
        \
        It is up to you to create these so called patterns, so the bot knows what it's supposed to be counting.\n\n\
        Every pattern you create is unique to the channel you created using that pattern, however you can clone patterns using the \"clone\" command\n\n\
        \
        NOTE: I realize all these embeds is a lot of text to read, but I recommend you at least skim through them, so you at least have a basic idea about how the bot works"
    embed.add_field(name="Usage Guide", value=value, inline=False)
    embeds.append(embed)
    embed = discord.Embed(
        title="Terminology", url=website, color=0xFC8403)
    embed.set_author(name=author_name, url=website, icon_url=profile_pic)
    terminology = "\
        NOTE: I know this all a lot to take in. If you feel overwhelmed at any point, feel free to take a break, and if you don't care about how Components work and just wanna know how many bots there are in your server or how many people have the @everyone role, skip ahead to when I talk about how to build Simple Patterns. I promise you, it's really easy\n\n\
        Before I explain patterns to you, here's a short list of what some of the things I say actually mean:\n"
    terminology_2 = "Counting Channel:\tThe name of the channels that the bot uses to do its count keeping"
    terminology_3 = "Component:\tA Component is a self contained part of a Pattern. Simple Patterns contain only one Component, while Advanced Components can contain any number of Components. There are many different types of Components, and they all have their own rules, but a good way to think about how Components work, is that they are machines that take in a member of your server as an input, and as an output they tell you \"Yes, this member follows my rules\" or \"No, this member does not follow my rules\""
    terminology_4 = "Pattern:\tA pattern is really just a wrapper around a Component. When the bot goes to update all the Counting Channels in your server, it will ask each every Counting Channel in your server \"What is your pattern\", at which point the Counting Channel will tell the bot what its pattern is. The bot then goes over each and every member in your server, and asks the pattern\"Does this member follow your rules?\". The number that gets updated in the name of your Counting Channel is how many times the pattern of that channel said \"Yes, this member follows my rules\""
    terminology_5 = "Boolean: A value that is either true or false. Can be thought of as a number that is either 0 or 1"
    embed.add_field(name="Terminology prelude",
                    value=terminology, inline=False)
    embed.add_field(name="Counting Channel meaning",
                    value=terminology_2, inline=False)
    embed.add_field(name="Component meaning",
                    value=terminology_3, inline=False)
    embed.add_field(name="Pattern meaning",
                    value=terminology_4, inline=False)
    embed.add_field(name="Boolean meaning",
                    value=terminology_5, inline=False)
    embeds.append(embed)
    embed = discord.Embed(
        title="Simple Patterns", url=website, color=0xFC8403)
    embed.set_author(name=author_name, url=website, icon_url=profile_pic)
    simple_patterns_text = "\
        Here's a short crash couse on how patterns work!\n\
        There are two kinds of patterns: Simple Patterns and Advanced Patterns\nSimplePatterns are, as the name inplies, simple.\n\
        The definition for a Simple Pattern is that they contain no Statements (I'll tell you what a Statement is later ^_^)"
    simple_patterns_text_2 = "\
        Alrigt, so let's say you wanted to create a pattern that tracks how many in your server have the @CoolKid role. How would you do this?.\n\
        Well hold your breath, for here comes THE GLORIOUS SIMPLE PATTERN!!!\n\
        @CoolKid\n\
        \"Really, its that simple? All I have to do is ping the role I want to track?\"\n\
        Yes it is my friend. In fact, building any SimplePattern is just as simple. For example:"
    simple_patterns_text_3 = "\
        if you want to create a pattern that tracks how many people in your server are bots, you write \"bot\" as your pattern.\n\
        if you want to track how many people have less than 3 roles, you write \"< 3\".\n\
        If you instead want to know how many members in your guild are not bots, you write \"not bot\".\n\
        A full list of Components can be found by the using \"components\" command."
    embed.add_field(name="Simple Patterns Overview",
                    value=simple_patterns_text, inline=False)
    embed.add_field(name="Example",
                    value=simple_patterns_text_2, inline=False)
    embed.add_field(name="More Examples",
                    value=simple_patterns_text_3, inline=False)
    embeds.append(embed)
    embed = discord.Embed(
        title="Advanded Patterns", url=website, color=0xFC8403)
    embed.set_author(name=author_name, url=website, icon_url=profile_pic)
    advanced_patterns_text = "\
        Building Advanced Components is only slightly harder. The Statement is the heart of any Advanced Component. Statements are considered to be Components in their own right. A Statement consists of three parts. Two Components and An Operator. Operators here are logical operators, so if you have ever taken a logics class, you will feel right at home. If you haven't fear not, for you can use the \"operators\" command to get a full list of all the operators and what they do. But in short, the OR, AND and XOR operators and their oposites are available.\n\
        In short, an operator takes in two numbers, that are either 0 or 1, or in other words, True or False, or in even more other words, a Boolean. It then uses its own interal rules to produce a new number, that is also a Boolean. Now you may be rightfully wondering what heck any of this has to do with Patterns or Components, and you'd be right to wonder."

    advanced_patterns_text_2 = "\
        In short, When the bot asks a Statement whether a member of your server follows its rules, the Statement will first ask the two components it contains if the member follows their rules. These components will then respond with True if the member follows its rules, and False otherwise\n\
        So the Statement then takes the result it gets from its components, and hands these two Booleans over to the operator, which then uses its internal to send back a Booleans response. This final result is then finally what the Statement returns as its final result\n\
        If you have no idea what I just said then don't worry. You'll probably understand better once you see some examples."

    advanced_patterns_text_3 = "\
        EXAMPLES:\n\n\
        \
        So lets you wanted to create a pattern that tracks how many members have more than 3 roles, and are bots. How would you do this?\n\
        Like this:\n\
        (> 3, and, bot)\n\
        As you can see, the defining characteristic of statements is that they surrounded by parentheses.\n\
        Here the first component of the Statement is a RolesLimitComponent, that checks if the user has more than 3 roles. Next is an AndOperator, and finally we have a BotComponent, that checks if the user is a bot."
    advanced_patterns_text_4 = "\
        We can also put Statements inside of Statements, or nest them, as its sometimes called. That looks like this:\n\
        (> 3, and, (bot, not exclusive or, @Moderator))\n\
        As you see, Statements can get pretty complicated pretty fast, but in the end they always consist of three parts. Two Components and an Operator.\n\
        NOTE: You can use the \"statement\" command for info on statements"

    embed.add_field(name="Advanced Patterns Intro",
                    value=advanced_patterns_text, inline=False)
    embed.add_field(name="Advanced Patterns Theory",
                    value=advanced_patterns_text_2, inline=False)
    embed.add_field(name="Advanced Patterns Example",
                    value=advanced_patterns_text_3, inline=False)
    embed.add_field(name="Advanced Patterns Nested Statements",
                    value=advanced_patterns_text_4, inline=False)
    embeds.append(embed)
    embed = discord.Embed(
        title="Summary", url=website, color=0xFC8403)
    embed.set_author(name=author_name, url=website, icon_url=profile_pic)
    summary = "\
        To summarise:\n\
        1. You can use the \"components\", \"operators\" and \"statement\" commands to get more info.\n\
        2. You can also use the \"intro\" command to get this message again\n\
        3. Patterns are the rules that you write, that tells the bot what a certain Counting Channel should keep track of.\n\
        4. Simple Components are stupid simple.\n\
        5. Advanced Components can get hard fast if you start nesting Statements, but if you avoid doing that they are pretty easy.\n\n\
        \
        If you have any questions you can join the support discord server and ask away to your hearts content.\n\
        Link: discord.gg/fq3kYsK4Ms"
    embed.add_field(name="Summary", value=summary, inline=False)
    embeds.append(embed)
    return embeds
