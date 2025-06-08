import discord
from discord.ext import commands
from discord.utils import get
import random
import asyncio
import json
from dotenv import load_dotenv
import os

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

JOIN_MESSAGE = "Hello, traveller!\nFeel free to join my server, I only deliver my new creations there...\nHere is an invitation for you :)\n%s"

RULES_MESSAGE = """### N0PStopia TCG

Ahem... So these are the official rules of _N0PStopia - Trading Card Game_!
For now, it is quite simple... but more releases are to come!
Each card has a specific class, represented by its original Topia (PwnTopia, WebTopia, CrypTopia and OsinTopia).
Those origins will give your card some special abilities.

Each card has between one and three abilities. The more superpowers your card has, the rarer it is!
For now, the first cards have not been released yet, but stay tuuuuuned!!!

Also, as a gift for our first players, you can redeem a free card now! All you have to do is to ask for your `!card`. Will you be lucky enough to get a _legendary_ one ??
"""

classes = ['pwntopia', 'webtopia', 'cryptopia', 'osintopia']

abilities = {
    'pwntopia': [
        "ASLR Bypass",
        "NOP Slide",
        "Return Oriented Programming",
        "Buffer Overflow",
        "Use After Free",
        "Format String",
        "Race Condition"
    ],
    'webtopia': [
        "Cross Site Scripting",
        "SQL Injection",
        "CSRF",
        "Command Injection",
        "Local File Inclusion",
        "Web Shell Upload",
        "Server Side Request Forgery"
    ],
    'cryptopia': [
        "Prime Number Factorization",
        "Hash Length Extension Attack",
        "Padding Oracle",
        "Poor PRNG Exploitation",
        "Side Channel Attack",
        "Quantum Cryptography",
        "Hash Collision"
    ],
    'osintopia': [
        "GeoGuesser Professional",
        "Sun Angle Analysis",
        "Polyglot",
        "Social Network Analysis",
        "OverPass Turbo",
        "Flight Schedule Mastermind",
        "Face Recognition Algorithm"
    ]
}

flag = os.getenv("FLAG")
guild_id = int(os.getenv("GUILD_ID"))
channel_id = int(os.getenv("CHANNEL_ID"))

roles = []

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="N0PStopia - TCG"))

@bot.event
async def on_member_join(member):
    if member.guild == bot.get_guild(guild_id):
        channel = bot.get_channel(channel_id)
        guild = member.guild
        role = member.name
        autorize_role = await guild.create_role(name=role)
        roles.append(autorize_role)
        await member.add_roles(autorize_role)
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=True, send_messages=False),
        }
        for role in roles:
            overwrites[role] = discord.PermissionOverwrite(read_messages=False)
        await channel.edit(overwrites=overwrites)
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            guild.me: discord.PermissionOverwrite(read_messages=True),
            autorize_role: discord.PermissionOverwrite(read_messages=True)
        }
        await guild.create_text_channel(member.name, overwrites=overwrites)
        await member.edit(nick=member.display_name)

@bot.event
async def on_message(message):
    
    guild = bot.get_guild(guild_id)
    
    if not(message.guild):
        if message.author != bot.user:
            if guild.get_member(message.author.id) is None:
                channel = bot.get_channel(channel_id)
                invite = await channel.create_invite(max_uses=1,unique=True)
                async with message.channel.typing():
                    await asyncio.sleep(5)
                await message.channel.send(JOIN_MESSAGE % invite)
            else:
                async with message.channel.typing():
                    await asyncio.sleep(2)
                await message.channel.send("I prefer if we discuss on my server...")
    elif message.guild == guild:
        if message.author != bot.user:
            if not message.content.startswith('!'):
                async with message.channel.typing():
                    await asyncio.sleep(1)
                await message.channel.send(f"Hello {message.author.nick}! I am Joe Dohn, **The Cardmaster**.")
                async with message.channel.typing():
                    await asyncio.sleep(1)
                await message.channel.send(f"Feel free to redeem your personal `!card`. It will be crafted especially for you!")
                async with message.channel.typing():
                    await asyncio.sleep(1)
                await message.channel.send(f"If you are curious about how my card game works, you can ask me about the `!rules`.")
            else:
                await bot.process_commands(message)

@bot.command()
async def rules(ctx):
    async with ctx.typing():
        await asyncio.sleep(1)
    await ctx.send(RULES_MESSAGE)

@bot.command()
async def devlog(ctx):
    await ctx.send(open('devlog.txt', 'r').read())

@bot.command()
async def card(ctx):
    display_name = ctx.author.nick.replace('/', '\\/')
    discord_tag = ctx.author.name.replace('/', '\\/')
    id = ctx.author.id
    profile_picture = ctx.author.display_avatar.url.replace('/', '\\/')
    default_picture = ctx.author.default_avatar.url.replace('/', '\\/')
    random.seed(id)
    card_class = random.choice(classes)
    if profile_picture == default_picture:
        profile_picture = f"https://www.nops.re/nopstgccards/default_profile_{card_class}.png".replace('/', '\\/')
    card_rarity = random.randint(0,100)
    if card_rarity <= 50:
        card_rarity_name = "common"
        card_abilities = random.sample(abilities[card_class], 1)
    elif card_rarity <= 80:
        card_rarity_name = "rare"
        card_abilities = random.sample(abilities[card_class], 2)
    elif card_rarity <= 99:
        card_rarity_name = "epic"
        card_abilities = random.sample(abilities[card_class], 3)
    else:
        card_rarity_name = "legendary"
        card_abilities = random.sample(abilities[card_class], 4)
    path = os.popen(f"/app/create_card.sh '{card_class}' '{display_name}' '{discord_tag}' '{'<br>'.join(card_abilities)}' '{profile_picture}' '{id}' '{card_rarity_name}'").read().strip()
    await ctx.send(file=discord.File(path, filename="card.jpg"))

bot.run(os.getenv("DISCORD_BOT_KEY"))

