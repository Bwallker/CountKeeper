 # Thank you for choosing CountKeeper!
 
## Intro
CountKeeper is a discord bot that counts how many members in your server follow certain patterns, allowing you to create extremely detailed statistics about your discord server.

It is up to you to create these so called patterns, so the bot knows what it's supposed to be counting.

Every pattern you create is unique to the channel you created using that pattern, however you can clone patterns using the "clone" command.

NOTE: I realize all this is a lot of text to read, but I recommend you at least skim through it, so you at least have a basic idea about how the bot works.

## Terminology

NOTE: I know this all a lot to take in. If you feel overwhelmed at any point, feel free to take a break, and if you don't care about how Components work and just wanna know how many bots there are in your server or how many people have the @everyone role, skip ahead to when I talk about how to build Simple Patterns. I promise you, it's really easy.
        
Before I explain patterns to you, here's a short list of what some of the things I say actually mean:
    
    Counting Channel: The name of the channels that the bot uses to do its count keeping.
    
    Component:  A Component is a self contained part of a Pattern. Simple Patterns contain only one Component, while Advanced Components can contain any number of Components. There are many different types of Components, and they all have their own rules, but a good way to think about how Components work, is that they are machines that take in a member of your server as an input, and as an output they tell you "Yes, this member follows my rules" or "No, this member does not follow my rules".
    
    Pattern:  A pattern is really just a wrapper around a Component. When the bot goes to update all the Counting Channels in your server, it will ask each every Counting Channel in your server "What is your pattern", at which point the Counting Channel will tell the bot what its pattern is. The bot then goes over each and every member in your server, and asks the pattern "Does this member follow your rules?". The number that gets updated in the name of your Counting Channel is how many times the pattern of that channel said "Yes, this member follows my rules"
    
    Boolean: A value that is either true or false. Can be thought of as a number that is either 0 or 1.
    
## Patterns and Simple Components

Here's a short crash couse on how patterns work!

There are two kinds of patterns: Simple Patterns and Advanced Patterns.
SimplePatterns are, as the name inplies, simple.
The definition for a Simple Pattern is that they contain no Statements (I'll tell you what a Statement is later).
Alrigt, so let's say you wanted to create a pattern that tracks how many in your server have the @CoolKid role. How would you do this?.
Well hold your breath, for here comes THE GLORIOUS SIMPLE PATTERN!!!

        @CoolKid


Really, its that simple? All I have to do is ping the role I want to track?
Yes it is my friend. In fact, building any SimplePattern is just as simple. For example:

If you want to create a pattern that tracks how many people in your server are bots, you write "bot" as your pattern.
If you want to track how many people have less than 3 roles, you write "< 3".
If you instead want to know how many members in your guild are not bots, you write "not bot".

A full list of Components can be found by the using "components" command.

## Advanced components

Building Advanced Components is only slightly harder. The Statement is the heart of any Advanced Component. Statements are considered to be Components in their own right.

A Statement consists of three parts. Two Components and An Operator. Operators here are logical operators, so if you have ever taken a logics class, you will feel right at home. If you haven't fear not, for you can use the "operators" command to get a full list of all the operators and what they do. But in short, the OR, AND and XOR operators and their oposites are available.

In short, an operator takes in two numbers, that are either 0 or 1, or in other words, True or False, or in even more other words, a Boolean. It then uses its own interal rules to produce a new number, that is also a Boolean. Now you may be rightfully wondering what heck any of this has to do with Patterns or Components, and you'd be right to wonder.

In short, When the bot asks a Statement whether a member of your server follows its rules, the Statement will first ask the two components it contains if the member follows their rules. These components will then respond with True if the member follows its rules, and False otherwise.

So the Statement then takes the result it gets from its components, and hands these two Booleans over to the operator, which then uses its internal logic to send back a Boolean response. This final result is then finally what the Statement returns as its final result.

If you have no idea what I just said then don't worry. You'll probably understand better once you see some examples.


EXAMPLES:

So lets you wanted to create a pattern that tracks how many members have more than 3 roles, and are bots. How would you do this?

Like this:
        
    (> 3, and, bot)
        
As you can see, the defining characteristic of statements is that they surrounded by parentheses.

Here the first component of the Statement is a RolesLimitComponent, that checks if the user has more than 3 roles. Next is an AndOperator, and finally we have a BotComponent, that checks if the user is a bot.


We can also put Statements inside of Statements, or nest them, as its sometimes called. That looks like this:

    (> 3, and, (bot, not exclusive or, @Moderator))
 
As you see, Statements can get pretty complicated pretty fast, but in the end they always consist of three parts. Two Components and an Operator.\n\

NOTE: You can use the "statement" command for more info on statements


## Summary

To summarise:
  1. You can use the \"components\", \"operators\" and \"statement\" commands to get more info.
  2. You can also use the \"intro\" command to get this message again.
  3. Patterns are the rules that you write, that tells the bot what a certain Counting Channel should keep track of.
  4. Simple Components are stupid simple.
  5. Advanced Components can get hard fast if you start nesting Statements, but if you avoid doing that they are pretty easy.
  
If you have any questions you can join the support discord server and ask away to your hearts content.

Link: discord.gg/fq3kYsK4Ms

    
-----------------------------------------------------------------------

TODO:
- Website
- More advanced tracking commands
- Control panel for configuring the bot


CONTRIBUTING:
- Create a new branch that is named after the feature you are adding and your own name
- So if you were to add a new command you might name your branch "Name of command"/"Your username"


Self hosting instructions:

Requirements:
1. Stable internet
2. 24/7 online pc (or at least while you are using the bot)
3. Latest version of Python installed (3.9 currently)


Setup instructions:

1. clone the main branch of the repo (git clone https://github.com/CountKeeper/CountKeeper.git) or (git clone git@github.com:CountKeeper/CountKeeper.git)
2. cd CountKeeper
3. Add the submodule that contains all the data files (git submodule add -f https://github.com/CountKeeper/CountKeeperData.git) or 
4. (git submodule add -f git@github.com:CountKeeper/CountKeeperData.git)
5. Create a venv using python3 -m venv count_keeper_venv
6. activate the venv using "source count_keeper_venv/bin/activate" on Linux/macOS or using "count_keeper_venvv\Scripts\activate.bat" on Windows
7. pip install -r requirements.txt
9. Open config.json inside of the submodule and change BOT_TOKEN to you bot token. You must create a discord app and then a bot for this. Instructions can be found in your search engine of choice. I won't list them here since the steps might change in the future. Search terms are "How to create discord bot" or "Bot token discord"

Running Instructions:
run start.bat on Windows or start.sh on Linux/macOS or alternatively activate the venv manually and run count_keeper.py
Please note that the start scripts won't work if you name your venv something else than count_keeper_venv
----------------------------------------------------------------------

Invite link for the bot:
https://discord.com/oauth2/authorize?client_id=813180967028129842&scope=bot&permissions=613520

Support server:
https://discord.gg/fq3kYsK4Ms
