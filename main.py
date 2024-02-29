# bot.py

import asyncio
import os
import random
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
intents.all()
intents.members = True
intents.message_content = True

owners = [417073119254282240, 386254372646158338]
grinchrole = 1188587621753036820

bot = commands.Bot(command_prefix = ["my.", "xs.","."], owner_ids = set(owners), intents=intents, help_command=None)

#BOTEVENTS
@bot.event
async def on_ready():
    print(f'{"-" * 50}\nConnected Bot: {bot.user.name}\n{"-" * 50}')

#####Alle main Module laden in ./modules/main/
    def getmainmodules():
        mainpath = "./modules/main/"
        modulliste = [x for x in os.listdir(mainpath) if "_" not in x]
        
        mainmodules0 = [("modules.main."+x[:-3]) for x in modulliste if ".py" in x and not("!" in x)]
        modulpaths = [x for x in modulliste if ".py" not in x]

        print(f"a{modulliste}\nb{mainmodules0}\nc{modulpaths}\n")
        
        for path in modulpaths:
            for data in os.listdir(mainpath+f"{path}"):
                data = data[:-3]
                print(f"{path} und {data}")
                if data == path:
                    mainmodules0.append(f"modules.main.{path}.{data}")

        print(f"d{mainmodules0}")
        return mainmodules0
    
    for module in getmainmodules():
        try:
            print(module)
            await bot.load_extension(module)
        except Exception as d:
            print(d)
    print("Main modules loaded.")
    


    
#####

@bot.command()
async def help(ctx):
    command_info = ""  # Declare command_info outside the loop
    for cog in bot.cogs.values():
        if isinstance(cog, commands.Cog):
            commands_list = cog.get_commands()
            if commands_list:
                cog_name = cog.qualified_name if cog.qualified_name else "No Category"
                for command in commands_list:
                    short_description = command.brief or "Keine kurze Beschreibung verfügbar."
                    command_info += f"`{command.name}` - {short_description}\n"  # Accumulate command_info properly
    if command_info:  # Check if command_info is not empty before sending
        await ctx.send(command_info)
    else:
        await ctx.send("No commands found.")

@commands.is_owner()
@bot.command(aliases=["l"])
async def load(ctx, extension):
    await bot.load_extension(f"modules.{extension}")


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
    await bot.unload_extension(f"modules.{extension}")
    await bot.load_extension(f"modules.{extension}")


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

    if os.popen('python3 --version').read() == "Python 3.6.8":
        os.system('export PATH=~/.localpython/bin:$PATH')

    await ctx.send(f"```{os.popen('git pull').read()}```")

    os.chdir(current_path)

    os.execv(sys.executable, ['python3', 'main.py'])

@bot.command()
@commands.is_owner()
async def modulespull(ctx):
    # Speichere den aktuellen Pfad
    current_path = os.getcwd() + "/"

    print(current_path)
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    await ctx.send(f"```{os.popen('git pull').read()}```")
    os.chdir(current_path)

    for module in os.listdir("./modules/main/"):
        print(module)


@bot.command(aliases=["f"])
async def freeze(ctx):
    loaded_cogs = [cog for cog in bot.cogs.keys()]
    if loaded_cogs:
        await ctx.send(f'Loaded cogs: {", ".join(loaded_cogs)}')
    else:
        await ctx.send('No cogs loaded.')


@bot.hybrid_command(name='test', with_app_command=True)
async def test(ctx):
    await ctx.send("This is a hybrid command!")





#BOT >>RUN
bot.run(TOKEN)
#
