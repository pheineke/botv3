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

#IMPORTS Else.................END

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
owners = [386254372646158338, 417073119254282240]

bot = commands.Bot(command_prefix = "my.", owner_ids = set(owners), intents=intents)

#BOTEVENTS
@bot.event
async def on_ready():
    print(f'{"-" * 50}\nConnected Bot: {bot.user.name}\n{"-" * 50}')

#####Alle main Module laden in ./modules/main/
    modulliste = os.listdir("./modules/main/")
    print(modulliste)
    try:
        for modul in modulliste:
            if os.path.isfile(modul):
                modul = modul.replace(".py","")
                await bot.load_extension(f'modules.main.{modul}')
                print(modul)
#####Mensa in ./modules/main/mensa/ laden
        await bot.load_extension('modules.main.mensa.mensa')

        print("Main modules loaded.")
    except Exception as d:
        print(d)
#####


@commands.is_owner()
@bot.command(aliases=["l"])
async def load(ctx, extension):
#####load side
    try:
        await bot.load_extension(f'modules.side.{extension}')
        await ctx.send(f"{extension} loaded")
    except:
#####load main
        try:
            await bot.load_extension(f'modules.main.{extension}')
            await ctx.send(f"{extension} loaded")
        except Exception as d:
            await ctx.send(f'{d}')



@commands.is_owner()
@bot.command(aliases=["u"])
async def unload(ctx, extension):
#####unload side
    try:
        await bot.unload_extension(f'modules.side.{extension}')
        await ctx.send(f'{extension} cog unloaded.')
        print(f'{extension} unloaded.')
    except:
#####unload main
        try:
            await bot.unload_extension(f'modules.main.{extension}')
            await ctx.send(f'{extension} cog unloaded.')
            print(f'{extension} unloaded.')
        except Exception as e:
            await ctx.send(f'{e}')

    

@commands.is_owner()
@bot.command(aliases=["r"])
async def reload(ctx, extension):
#####reload side

    try:
        await bot.unload_extension(f'modules.side.{extension}')
        await bot.load_extension(f'modules.side.{extension}')
        await ctx.send(f'{extension} cog reloaded.')
        print(f'{extension} reloaded.')
    except:
#####reload main
        try:
            await bot.unload_extension(f'modules.main.{extension}')
            await bot.load_extension(f'modules.main.{extension}')
            await ctx.send(f'{extension} cog reloaded.')
            print(f'{extension} reloaded.')
        except Exception as e:
            await ctx.send(f'{e}')


@bot.hybrid_command(name='test', with_app_command=True)
async def test(ctx):
    await ctx.send("This is a hybrid command!")

#BOT >>RUN
bot.run(TOKEN)

