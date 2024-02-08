import discord
from discord.ext import commands
#####
from datetime import datetime
from dotenv import load_dotenv
import json
import asyncio
import os

#####
import usertimehandler as ut

print(os.getcwd())

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
                            usertimehandler.userwrite(author, arg)
                            await ctx.send(f"{authormention} Deine Zeit ({arg[:2]}:{arg[2:]} Uhr) wurde eingetragen.")
                elif arg == "jetzt":
                    usertimehandler.userwrite(author, str(datetime.now().strftime("%H%M")))
                elif arg == 'false' or arg == 'none' or arg is None:
                    usertimehandler.userwrite(author, 'false')
                    await ctx.send(f"{authormention} Usertime wurde disabled.")
                elif arg == 'true':
                    await ctx.send(f"{authormention} Um deine Usertime zu enablen setze deine Mensatime auf eine neue Uhrzeit.")
                elif arg == 'constant' or arg == 'const':
                    usertimehandler.setuserconst(author)
                    await ctx.send(f"{authormention} Deine Usertime wurde als konstant vermerkt.")
                elif arg == 'notconstant' or arg == 'nconst':
                    usertimehandler.deluserconst(author)
                    await ctx.send(f"{authormention} Deine Usertime wurde als nicht-konstant eingetragen.") 
                elif arg == 'del' or arg == 'delete':
                    await ctx.send(f"{authormention} {usertimehandler.userdelete()}") 
                elif '<@' in arg and '>' in arg:
                    try:
                        arg in ctx.guild.members()
                    except:
                        await ctx.send(f"{arg} ist kein gültiger User")
                    finally:
                        await ctx.send(f"Die Zeit von {authormention} wurde {usertimehandler.userwriteuser(author, arg)}")
                else:
                    try:
                        datetime.strptime(arg, "%H%M")
                        usertimehandler.userwrite(author, arg)
                        await ctx.send(f"{authormention} Deine Zeit ({arg[:2]}:{arg[2:]} Uhr) wurde eingetragen.")
                    except:
                        await ctx.send("Das ist kein gültiges Argument.")
            elif equal is None and arg is None:
                await ctx.send(f"{authormention} Deine Mensazeit ist {usertimehandler.userread(author)}")

        elif ctx.prefix == "xs.":
            await ctx.send(f"{ctx.author.mention} Folgende Mensazeiten sind eingetragen:\n```\n{usertimehandler.userreadall()}\n```")


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
                usertimehandler.userreset()
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