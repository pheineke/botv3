import asyncio
import os

import discord
from discord.ext import commands

from datetime import datetime

import modules.main.mensa.usertime as ut
from dotenv import load_dotenv


class Mensa(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.loop.create_task(self.cyclereset())


    @commands.command()
    async def mensatime(self, ctx, equal=None, arg=None):
        authormention = ctx.author.mention
        author = ctx.author.name
        arg = arg.replace(".","").replace("-","").replace(":","")
        if equal == "=":
            if len(arg) == 2:
                try:
                    arg += "00"
                except:
                    await ctx.send("Das ist kein gültiges Argument.")
                finally:
                    try:
                        datetime.strptime(arg, "%H%M")
                    except:
                        await ctx.send("Das ist kein gültiges Argument.")
                    finally:
                        ut.userwrite(author, arg)
                        await ctx.send(f"{authormention} Deine Zeit ({arg[:2]}:{arg[2:]} Uhr) wurde eingetragen.")
            elif len(arg) == 4 and datetime.strptime(arg, "%H%M"):
                ut.userwrite(author, arg)
                await ctx.send(f"{authormention} Deine Zeit ({arg[:2]}:{arg[2:]} Uhr) wurde eingetragen.")
            elif arg == "jetzt":
                ut.userwrite(author, str(datetime.now().strftime("%H%M")))
            elif arg == 'false' or arg == 'none':
                ut.userwrite(author, 'false')
                await ctx.send(f"{authormention} Usertime wurde disabled.")
            elif arg == 'true':
                await ctx.send(f"{authormention} Um deine Usertime zu enablen setze deine Mensatime auf eine neue Uhrzeit.")
            elif arg == 'constant' or arg == 'const':
                ut.setuserconst(author)
                await ctx.send(f"{authormention} Deine Usertime wurde als konstant vermerkt.")
            elif arg == 'notconstant' or arg == 'nconst':
                ut.deluserconst(author)
                await ctx.send(f"{authormention} Deine Usertime wurde als nicht-konstant eingetragen.") 
            elif arg == 'del' or arg == 'delete':
                await ctx.send(f"{authormention} {ut.userdelete()}") 
            elif '<@' in arg and '>' in arg:
                try:
                    arg in ctx.guild.members()
                except:
                    await ctx.send(f"{arg} ist kein gültiger User")
                finally:
                    await ctx.send(f"Die Zeit von {authormention} wurde {ut.userwriteuser(author, arg)}")
            else:
                await ctx.send("Das ist kein gültiges Argument.")
        elif equal is None and arg is None:
            await ctx.send(f"{authormention} Deine Mensazeit ist {ut.userread(author)}")


    @commands.Cog.listener()
    async def xsmensatime(self, message):
        if not message.author.bot and message.content.lower() == "xs.mensatime":
            await message.channel.send(f"{message.author} Folgende Mensazeiten sind eingetragen:\n```\n{ut.userreadall()}\n```")


    @commands.command()
    async def myhelp(self, ctx):
        load_dotenv("./.envlocal")
        embed = discord.Embed(title="MensaBot Help", description=os.getenv('helpmessage'),color=0x9998ff)
        await ctx.send(embed = embed)
    
    
    async def cyclereset(self):
        while True:
            
            currenttime = str(datetime.now().strftime("%H:%M"))
            if currenttime == "15:00":
                ut.userreset()
            await asyncio.sleep(30)
    
    
async def setup(bot):
    await bot.add_cog(Mensa(bot))