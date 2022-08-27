import os
import discord
import time
import asyncio
import datetime
import random
import aiohttp
import pretty_help

from discord import Guild, activity, Member, TextChannel, User

from discord.ext import commands, tasks
from discord.ext.commands import Bot, has_permissions, has_role, has_any_role, MissingPermissions, BadArgument
from discord.utils import get

from datetime import datetime
from itertools import cycle
from pretty_help import DefaultMenu, PrettyHelp

from webserver import keep_alive


intents = discord.Intents.all()
intents.members = True

players = {}

menu = DefaultMenu(page_left="◀", page_right="▶", remove="❌")
ending_note = "The Bambenian Bot Help Menu" 
no_category="All Commands"

bot = commands.Bot(command_prefix='-', help_command=PrettyHelp(menu=menu, ending_note=ending_note, no_category=no_category, show_index=False, sort_commands=True, dm_help=True), intents=intents)

amount = 0

#BOT ONLINE PRINT

@bot.event
async def on_ready():
    timestamp = datetime.now()

    print("-------------------")
    print('The Bambenian Bot is online!')
    print('Ping: {0}ms'.format(round(bot.latency, 3)))
    print("-------------------")

    bot.loop.create_task(status_task())

# BOT COMMAND NOT FOUND ERROR

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("The command you entered doesn't exist!", delete_after=5)


#BOT CHANGE PRESENCE

@bot.event
async def status_task():
    while True:
        await bot.change_presence(activity=discord.Game(name="MPAMPHS IS MY HERO"))


#BOT.LISTEN - 1

@bot.listen('on_message')
async def f(message):
    if message.author == bot.user:
        return

    elif 'f in chat' in message.content.lower():
        await message.channel.send('F')


#BOT.LISTEN - 2

@bot.listen('on_message')
async def love(message):
    if message.author == bot.user:
        return

    elif 'i love this bot' in message.content.lower():
        await message.channel.send("Love you too homie.")


#CLEAR COMMAND 

@bot.command(help="Clears given number of messages", hidden=True)
@has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount + 1)
    if amount==1:
        await ctx.channel.send('Deleted 1 message', delete_after=3)
    else:
        await ctx.channel.send(f'Deleted {amount} messages', delete_after=3)

@clear.error
async def clear_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.channel.send(f"{ctx.message.author.mention}, you don't have the permission to do that!", delete_after=5)


#LATENCY COMMAND

@bot.command(help="Shows latency")
async def ping(ctx):
    await ctx.channel.send("Ping/Latency: {0} ms".format(round(bot.latency, 3)))


#FUN COMMAND 1

@bot.command(help="THE WARHAMMER SHALL DROP")
async def warhammer(ctx):
    await ctx.channel.send("ONCE THE WARHAMMER DROPS...")
    await asyncio.sleep(1)
    await ctx.channel.send("...YOU SHALL BE FLATTENED")
    await asyncio.sleep(1)
    await ctx.channel.send("-random flat earther")


#KICK COMMAND

@bot.command(help="Kicks a user.", hidden=True)
@has_permissions(kick_members=True)
async def kick(ctx, member : discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.channel.send(f'Kicked {member.mention}\n-Reason: {reason}', delete_after=10)


@kick.error
async def kick_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.channel.send(f"{ctx.message.author.mention}, you don't have the permission to do that!", delete_after=5)


#BAN COMMAND

@bot.command(help="Bans a user.", hidden=True)
@has_permissions(ban_members=True)
async def ban(ctx, member : discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.channel.send(f'Banned {member.mention}\n-Reason: {reason}')
    await ctx.channel.send("https://imgur.com/a/e3g5W37")

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.channel.send(f"{ctx.message.author.mention}, you don't have the permission to do that!", delete_after=5)

#BAM COMMAND

@bot.command(help="Bams a user.")
async def bam(ctx):
    await ctx.channel.send("https://imgur.com/a/e3g5W37")

#UNBAN COMMAND

@bot.command(help='Unbans a banned user.', hidden=True)
@has_permissions(ban_members=True)
async def unban(ctx, id: int):
    user = await bot.fetch_user(id)
    await ctx.guild.unban(user)

@unban.error
async def unban_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.channel.send(f"{ctx.message.author.mention}, you don't have the permission to do that!", delete_after=5)


#INFO COMMAND

@bot.command(help='Gives info about the server.')
async def serverinfo(ctx):
    embed = discord.Embed(title="Sphere of Bambenia Server", description="")
    embed.add_field(name="Server Created At:", value=ctx.guild.created_at.strftime("%d/%m/%Y %H:%M:%S"), inline=False)
    embed.add_field(name="Server Owner:", value=ctx.guild.owner, inline=False)
    embed.add_field(name="Role Count:", value=len(ctx.guild.roles), inline=False)
    embed.add_field(name="Category Count:", value=len(ctx.guild.categories), inline=False)
    embed.add_field(name="Channel Count:", value=len(ctx.guild.channels), inline=False)
    embed.add_field(name="Booster Status:", value=ctx.guild.premium_subscription_count, inline=False)
    await ctx.channel.send(embed=embed)


#STUPID METER COMMAND

@bot.command(help="Measures how stupid you (or a specified user) are!")
async def stupid(ctx, member : discord.Member = None):
    percentage = (random.randint(0, 100))

    if member == None:
        message = await ctx.channel.send("Calculating...")
        await asyncio.sleep(3)
        await message.edit(content=f"You are {percentage}% stupid!")

    if member == bot.user:
        message = await ctx.channel.send("Calculating...")
        await asyncio.sleep(3)
        await message.edit(content=f"HOW DARE YOU CALL ME STUPID")

    elif member == member:
        message = await ctx.channel.send("Calculating...")
        await asyncio.sleep(3)
        await message.edit(content=f"{member.mention} is {percentage}% stupid!")


#SAY COMMAND
@bot.command(help="Says what you say")
async def say(ctx, *, message=None):
    if message == None:
        await ctx.channel.send('You need to say something so I can say it back...')
    else:
        await ctx.channel.send(message)


#FLAG COMMAND
@bot.command(help="Says what you say")
async def flag(ctx, *, message=None):
        await ctx.channel.send("https://cdn.discordapp.com/attachments/1010331746920824944/1013131110781304952/RWDT_Flag.png")
        await ctx.channel.send("So goddamn beautiful")


#MAP COMMAND
@bot.command(help="Says what you say")
async def map(ctx, *, message=None):
        await ctx.channel.send("https://cdn.discordapp.com/attachments/1010331746920824944/1013131462503051344/1661619314901.jpg")


keep_alive()

TOKEN = os.environ.get("DISCORD_TOKEN")

bot.run(TOKEN)