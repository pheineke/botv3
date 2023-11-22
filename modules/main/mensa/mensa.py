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
    async def mensatime(self, ctx, equal, arg):
        author = ctx.author.name
        arg = arg.replace(".","").replace("-","").replace(":","")
        if equal == "=":
            try:
                datetime.strptime(arg, "%H%M")
            except:
                try:
                    datetime.strptime(arg, "%H")
                except:
                    
                    if arg == "jetzt":
                        ut.userwrite(author, str(datetime.now().strftime("%H%M")))
                    elif arg == 'false' or arg == 'none':
                        ut.userwrite(author, 'false')
                        await ctx.send(f"{author} Usertime wurde disabled.")
                    elif arg == 'true':
                        await ctx.send(f"{author} Um deine Usertime zu enablen setze deine Mensatime auf eine neue Uhrzeit.")
                    elif arg == 'constant' or arg == 'const':
                        ut.setuserconst(author)
                        await ctx.send(f"{author} Deine Usertime wurde als konstant vermerkt.")
                    elif arg == 'notconstant' or arg == 'nconst':
                        ut.deluserconst(author)
                        await ctx.send(f"{author} Deine Usertime wurde als nicht-konstant eingetragen.") 
                    elif arg == 'del' or arg == 'delete':
                        await ctx.send(f"{author} {ut.userdelete()}") 
                    elif '<@' in arg and '>' in arg:
                        try:
                            arg in ctx.guild.members()
                        except:
                            await ctx.send(f"{arg} ist kein gültiger User")
                        finally:
                            await ctx.send(f"{author} Die Zeit von {author} wurde {ut.userwriteuser(author, arg)}")
                    else:
                        raise ValueError("Incorrect data format, should be hh:mm or similar")
                finally:
                    arg += "00"
                    ut.userwrite(author, arg)

            finally:
                ut.userwrite(author, arg)
        else:
            await ctx.send("Das ist kein gültiges Argument.")


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