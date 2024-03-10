# bot.py


import asyncio
import discord
from discord import app_commands
from discord.ext import commands, tasks
from discord.ui import Button, View

import os, sys, subprocess
from dotenv import load_dotenv
from datetime import datetime

from main_helper import Helper


async def create_logdir():
    if not os.path.exists(os.getcwd() + "/logs"):
    # Erstelle den Ordner, wenn er nicht vorhanden ist
        os.makedirs(os.getcwd() + "/logs")
        print("Der 'logs' Ordner wurde erstellt.")
    else:
        print("Der 'logs' Ordner existiert bereits.")




async def load_spine():
    mainpath = "./modules/spine/"
    modulliste = [x for x in os.listdir(mainpath) if "pycache" not in x]
    mainmodules0 = [("modules.spine."+x[:-3]) for x in modulliste if ".py" in x and not("!" in x)]
    succeded = []
    for module in mainmodules0:
            try:
                #print(module)
                await bot.load_extension(module)
                succeded.append(module)
            except Exception as d:
                print(d)
    print(f"Spine modules loaded. {succeded}")


async def getmainmodules():
        mainpath = "./modules/main/"
        modulliste = [x for x in os.listdir(mainpath) if "_" not in x]
        
        mainmodules0 = [("modules.main."+x[:-3]) for x in modulliste if ".py" in x and not("!" in x)]
        modulpaths = [x for x in modulliste if ".py" not in x]

        #print(f"a{modulliste}\nb{mainmodules0}\nc{modulpaths}\n")
        
        for path in modulpaths:
            for data in os.listdir(mainpath+f"{path}"):
                data = data[:-3]
                #print(f"{path} und {data}")
                if data == path:
                    mainmodules0.append(f"modules.main.{path}.{data}")

        #print(f"d{mainmodules0}")
        for module in mainmodules0:
            try:
                #print(module)
                await bot.load_extension(module)
            except Exception as d:
                print(d)
        print("Main modules loaded.")


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

owners = [417073119254282240, 386254372646158338]

bot = commands.Bot(command_prefix = ["my.", "xs.","."], owner_ids = set(owners), intents=discord.Intents.all(), help_command=None, sync_commands=True)
#BOTEVENTS
@bot.event
async def on_ready():
    #activity = discord.Game(name="Starting...", type=3,
    #                        large_image=)
    slower = True
    while(slower):
        try:
            await bot.change_presence(status=discord.Status.idle)
            await bot.user.edit(avatar=open("./lib/pic/loading.gif",'rb').read())
            slower = False
            break
        except:
            await asyncio.sleep(10.0)
            slower = True

    await create_logdir()
    await Helper().do()
    await load_spine()
    await getmainmodules()


    slower = True
    while(slower):
        try:
            await bot.change_presence(status=discord.Status.online)
            await bot.user.edit(avatar=open("./lib/pic/normal_pfp.png",'rb').read())
            slower = False
            break
        except:
            await asyncio.sleep(10.0)
            slower = True


    print(f'{"-" * 50}\nConnected Bot: {bot.user.name}\n{"-" * 50}')



#BOT >>RUN
bot.run(TOKEN)











###################################################################



