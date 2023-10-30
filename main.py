# bot.py

import asyncio
import os
import sys
import subprocess
import discord
from discord.ext import commands
from discord.ext import tasks

from dotenv import load_dotenv

from datetime import datetime

#IMPORTS Discord..............END
import modules.abacus as abacus

#IMPORTS......................END

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix = "$",intents=intents)

#BOTEVENTS
@bot.event
async def on_ready():
    print("Im Ready")

@commands.is_owner()
@bot.command(aliases=["l"])
async def load(ctx, extension):
    try:
    
        await bot.load_extension(f'modules.{extension}')
        await ctx.send(f"{extension} loaded")
    except Exception as d:
        await ctx.send(f"{d}")

@bot.hybrid_command()
async def test(ctx):
    await ctx.send("This is a hybrid command!")

#BOT >>RUN
bot.run(TOKEN)