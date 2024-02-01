import asyncio
import os
import json
import discord
from discord.ext import commands

from datetime import datetime
from dotenv import load_dotenv


class MensaTemp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.create_db()


    @commands.group(invoke_without_command=True)
    async def sensatime(self, ctx):
        authormention = ctx.author.mention
        author = ctx.author.name

        if ctx.prefix == "my.":
            await ctx.send(f"{authormention} Deine Mensazeit ist {ut.userread(author)}")
        elif ctx.prefix == "xs.":
            await ctx.send(f"{authormention} Folgende Mensazeiten sind eingetragen:\n```\n{ut.userreadall()}\n```")

    @sensatime.group(name='=',invoke_without_command=True)
    async def settime(self, ctx, arg=None):
        author = ctx.author.name
        authormention = ctx.author.mention

        if arg is None:
            await ctx.send("Deine Mutter")
        elif (''.join([char for char in arg if char.isdigit()]).isdigit()):
            try:
                
                arg = ''.join([char for char in arg if char.isdigit()])
                arg = (str(arg).zfill(2)).ljust(4,"0")

                try:
                    print(datetime.strptime(arg, "%H%M").time())
                    ut.userwrite(author, arg)
                    await ctx.send(f"{authormention} Deine Zeit ({arg[:2]}:{arg[2:]} Uhr) wurde eingetragen.")
                except:
                    await ctx.send("Das ist kein gültiges Argument.")
            except:
                await ctx.send("Keine gültige Uhrzeit.")
        elif (arg == 'jetzt'):
              nowtime = str(datetime.now().strftime("%H%M"))
              ut.userwrite(author, nowtime)
              await ctx.send(f"{author} deine Zeit ist jetzt ...")

        elif arg in ['false','none']:
                ut.userwrite(author, 'false')
                await ctx.send(f"{authormention} Usertime wurde disabled.")
        elif arg == 'true':
                await ctx.send(f"{authormention} Um deine Usertime zu enablen setze deine Mensatime auf eine neue Uhrzeit.")
        elif arg is ['constant', 'const']:
                ut.setuserconst(author)
                await ctx.send(f"{authormention} Deine Usertime wurde als konstant vermerkt.")
        elif arg is ['notconstant', 'nconst']:
                ut.deluserconst(author)
                await ctx.send(f"{authormention} Deine Usertime wurde als nicht-konstant eingetragen.") 
        elif arg in ctx.guild.members():
                await ctx.send(f"Die Zeit von {authormention} wurde {ut.userwriteuser(author, arg)}")
        elif arg in ctx.guild.members():
                await ctx.send(f"Die Zeit von {authormention} wurde {ut.userwriteuser(author, arg)}")
        else:
            await ctx.send("Das ist kein gültiges Argument.")
          
    
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
    await bot.add_cog(MensaTemp(bot))





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