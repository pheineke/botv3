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
        if ctx.prefix == "my.":
            authormention = ctx.author.mention
            author = ctx.author.name

            print(arg)
            print(type(arg))
            print(equal)
            print(type(equal))
            if equal is not None and arg is not None:
                arg = arg.replace(".","").replace("-","").replace(":","")
                if len(arg) == 2 and len(equal) == 1 and equal == "=":
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
                    try:
                        datetime.strptime(arg, "%H%M")
                        ut.userwrite(author, arg)
                        await ctx.send(f"{authormention} Deine Zeit ({arg[:2]}:{arg[2:]} Uhr) wurde eingetragen.")
                    except:
                        await ctx.send("Das ist kein gültiges Argument.")
            elif equal is None and arg is None:
                await ctx.send(f"{authormention} Deine Mensazeit ist {ut.userread(author)}")

        elif ctx.prefix == "xs.":
            await ctx.send(f"{ctx.author.mention} Folgende Mensazeiten sind eingetragen:\n```\n{ut.userreadall()}\n```")


    @commands.command()
    async def myhelp(self, ctx):
        load_dotenv("./.envlocal")
        embed = discord.Embed(title="MensaBot Help",color=0x9998ff)
        embed.add_field(name="Auflistung Bot-Befehle (alle können in lowercase angegeben werden)", value="", inline=False)
        embed.add_field(name="my.myhelp", value="Well du bist schon hier...",inline=False)
        embed.add_field(name="my.mensatime", value=">> ohne weiteren Command gibt er euch eure Zeit zurück.\n>> **= HH:MM** oder **= HH Uhr** oder *= HH:MM Uhr* - geht alles.\n>> **= False** oder **= None**  - wird später bei xs.mensatime wichtig.\n>> **= anderen User pingen**, oder seinen Usertag eintragen.\n- Setzt den User auf den anderen User.\n>> **= const** oder **= constant** - Setzt den User auf konstant\n- (Dies ist noch ein Experimentelles Feature, es sollten alle nicht-constant User um 15:00 resettet werden.)\n>> **= nconst** oder **= notconstant** - das Gegenteil von **const**\n",inline=False)
        embed.add_field(name="xs.mensatime", value=">> Gibt euch eine Liste zurück von Mensazeiten der User, die sich eingetragen haben.\n>> Insofern ihr bei my.mensatime = False eingegeben habt, werdet ihr in der xs Liste nicht aufgelistet.\n>> Ihr müsst aber um euch wieder einzutragen, einfach euch eine neue Uhrzeit setzen.",inline=False)
        await ctx.send(embed = embed)
    
    
    async def cyclereset(self):
        while True:
            
            currenttime = str(datetime.now().strftime("%H:%M"))
            if currenttime == "15:00":
                ut.userreset()
            await asyncio.sleep(30)
    
    
async def setup(bot):
    await bot.add_cog(Mensa(bot))