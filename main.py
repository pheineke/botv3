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

bot = commands.Bot(command_prefix = ["my.", "xs."], owner_ids = set(owners), intents=intents)

#BOTEVENTS
@bot.event
async def on_ready():
    print(f'{"-" * 50}\nConnected Bot: {bot.user.name}\n{"-" * 50}')

#####Alle main Module laden in ./modules/main/
    modulliste = os.listdir("./modules/main/")
    try:
        await bot.load_extension('modules.main.mensa.mensa')
        await bot.load_extension('modules.main.latex')

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
######reload mensa
    if extension == "mensa":
        try:
            await bot.unload_extension('modules.main.mensa.mensa')
            await bot.load_extension('modules.main.mensa.mensa')
            await ctx.send('mensa cog reloaded.')
            print('mensa reloaded.')
        except Exception as e:
            await ctx.send(f'{e}')
    else:
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


'''Bot kann heruntergefahren werden.'''
@bot.command()
@commands.is_owner()
async def shutdown(ctx):
    await ctx.send('Shutting down...')
    print('Shutting down...')
    await bot.close()

@bot.command()
@commands.is_owner()
async def gitpull(ctx):
    # Speichere den aktuellen Pfad
    current_path = os.getcwd() + "/"

    print(current_path)
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    await ctx.send(os.system('git pull'))

    os.chdir(current_path)

    os.execv(sys.executable, ['python3', 'main.py'])      


@bot.hybrid_command(name='test', with_app_command=True)
async def test(ctx):
    await ctx.send("This is a hybrid command!")

#BOT >>RUN
bot.run(TOKEN)
#
