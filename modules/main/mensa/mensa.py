import asyncio
import os

import discord
from discord.ext import commands

from datetime import datetime
from dotenv import load_dotenv


class Mensa(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.loop.create_task(self.cyclereset())
        self.create_db()

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
                arg = arg.replace(".","").replace("-","").replace(":","").lower()
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
                elif arg == 'false' or arg == 'none' or arg is None:
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


    #############################################################################################
            
    async def check_for_webhook(self, ctx, hookname):
        # Überprüfe, ob in diesem Channel bereits ein Webhook existiert
        existing_webhooks = await ctx.channel.webhooks()
        webhook = None

        for existing in existing_webhooks:
            if existing.name == hookname:
                webhook = existing
                print("Es exisitiert ein Webhook")
                break

        # Wenn kein Webhook gefunden wurde, erstelle einen neuen
        if webhook is None:
            webhook = await ctx.channel.create_webhook(name=hookname)
            print("Es exisitiert kein Webhook -> Wurde ein Neuer erstellt.")
        return webhook
    
    @commands.Cog.listener("on_reaction_add")
    async def on_reaction_add(self,reaction, user):
        if user.bot:
            return
        if str(reaction.emoji) == "<:plus1:1171776509195845652>":
            hookname = self.bot.user.name
            webhook = await self.check_for_webhook(reaction.message, hookname)
            await webhook.send(content=reaction.message.content, avatar_url=user.avatar, username=user.name)

    
    def create_db(self):
    # Liste der Dateinamen
        file_names = ["userdata.json", "usercache.json"]

        for file_name in file_names:
            if not os.path.exists(file_name):
                # Datei existiert nicht, erstelle sie und fülle sie mit einem leeren Dictionary
                with open(file_name, 'w') as file:
                    json.dump({}, file)
                    print(f'Datei {file_name} wurde erstellt und mit einem leeren Dictionary gefüllt.')

    
async def setup(bot):
    await bot.add_cog(Mensa(bot))



from string import printable
import time
from table2ascii import table2ascii as t2a, PresetStyle

class ut():
    def mapuser(user, string):
        usermap = jsh.openjsonfile('usermapping','userdata.json')
        usermap[user] = string
        return "Dir wurde erfolgreich ein Alias erstellt."

    def userread(user):
            localreaddata = jsh.openjsonfile('usercache','userdata.json')
            user = user.lower()

            try:
                    userdata = str(localreaddata[user])
            except:
                    return "nicht vorhanden."
            else:
                    if userdata == 'false':
                            return "nicht vorhanden."
                    
                    userdatalen = len(userdata)
                    hour, minute = userdata[:userdatalen//2], userdata[userdatalen//2:]

                    return (hour + ':' + minute)

    def userreadall():
            localreadall = jsh.openjsonfile('usercache','userdata.json')

            keys = [k for k, v in localreadall.items() if v == "false"]

            finallist = []
            i = 0

            for x in keys:
                    del localreadall[x]
            if not localreadall:
                    return "-> Keine.\n\n\n Bitch."
            else:
                    for attribute, value in localreadall.items():

                            string = str(value)
                            firstpart, secondpart = string[:len(string)//2], string[len(string)//2:]
                            finallist.append([attribute, firstpart + ":" + secondpart])
                    
                    finallist = t2a(
                            header=["User", "Zeit"],
                            body=finallist,
                            style=PresetStyle.thin_compact)
                    #print(finallist)
                    return finallist


    def userwrite(user, time):
            localuserwrite = jsh.openjsonfile('usercache', 'userdata.json')
            user = user.lower()
            localuserwrite[user] = time

            jsh.savefile(localuserwrite, 'usercache','userdata.json')

    def userwriteuser(user0, user1):
            try:
                    user1time = ut.userread(user1)
                    int(user1time)
            except:
                    return "nicht gefunden."
            else:
                    
                    user0 = user0.lower()
                    ut.userwrite(user0, user1time[:2] + user1time[3:])
                    return "als deine Zeit eingetragen." 

            


    def userdelete(user):
            localuserdelete = jsh.openjsonfile('usercache.json')
            user = user.lower()

            try:
                    del localuserdelete[user]
            except:
                    return "Diesen User gibt es nicht."

            else:
                    jsh.savefile(localuserdelete,'usercache.json')
                    return "Der User wurde gelöscht."

    def setuserconst(user):
            user = user.lower()
            userdata = jsh.openjsonfile('userconstants','userdata.json')
            userdata[user]= ""
            jsh.savefile(userdata,'userconstants', 'userdata.json')

    def deluserconst(user):
            userconstantsdelete = jsh.openjsonfile('userconstants','userdata.json')
            user = user.lower()

            try:
                    del userconstantsdelete[user]
            except:
                    return "Diesen User gibt es nicht."

            jsh.savefile(userconstantsdelete,'userconstants', 'userdata.json')

    def userreset():
        localuserconstants = jsh.openjsonfile('userconstants','userdata.json')
        data = jsh.openjsonfile('usercache','userdata.json')
        data2 = {}
        for key, value in data.items():
            if key in localuserconstants:
                data2[key] = value
        jsh.savefile(data2, 'usercache','userdata.json')



import json

class jsh():
    def openjsonfile(type, jsonfile):
            with open(jsonfile, 'r') as f:
                    data = json.load(f)
                    return data[type]
            
    def savefile(data, type, file):
            with open(file, 'r') as f:
                    jsondata = json.load(f)
                    jsondata[type] = data
                    with open(file, 'w') as f:
                            json.dump(jsondata,f)