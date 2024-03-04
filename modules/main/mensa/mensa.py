import discord
from discord.ext import commands, tasks
from datetime import datetime

import requests

import modules.main.mensa.database as database

class Mensa(commands.Cog):
    def __init__(self,bot) -> None:
        self.bot = bot
        self.user_time_db = database.Manage_database("users.db")
        self.cyclereset.start()

    async def db_controller(self, ctxprefix, authormention, authorname, equal=None, arg=None):
        if ctxprefix == "my.":
            if arg is None and equal is None:
                try:
                    response = f"{authormention} Deine Mensazeit ist: {self.user_time_db.get_user_times(authorname)[0]}".replace("'","")
                    return ("1", response) #1, response
                    
                except:
                    return ("3", "Keine Usertime") #3
            else:
                if equal == "=":
                    if arg in ["none", "NONE", "false", "False"]:
                        try:
                            self.user_time_db.remove_user(authorname)
                            return ("2", None) #2
                        except:
                            return ("3", "Kein User eingetragen.") #3
                    elif arg in ["const", "constant", "1"]:
                        try:
                            self.user_time_db.set_user_time_constant(authorname)
                            return ("2", None) #2
                        except:
                            return ("3", "Kein User eingetragen.") #3
                    elif arg in ["nconst", "nconstant", "notconstant", "0"]:
                        try:
                            self.user_time_db.set_user_time_nconstant(authorname)
                            return ("2", None) #2
                        except:
                            return ("3", "Kein User eingetragen.") #3
                    elif arg in ["jetzt", "now", "rn"]:
                        try:
                            now = datetime.now().strftime("%H:%M")
                            self.user_time_db.save_user_time(authorname, str(now))
                            return ("2", None) #2
                        except:
                            return ("0", "Kein gültiger Befehl") #0
                    else:
                        try:
                            arg = self.user_time_db.striptime(arg)
                            if self.user_time_db.validate_time_format(arg):
                                self.user_time_db.save_user_time(authorname, arg)
                                return ("2", None) #2
                        except Exception as e:
                            print(e)
                            return ("0", "Kein gültiger Befehl") #0

                        
        if ctxprefix == "xs.":
            x = self.user_time_db.get_all_users_with_times()
            a = {key: x[key] for key in sorted(x)}
            y = ""
            for key,value in a.items():
                y += f"{key:15} |  {value}\n".replace("'","").replace("[","").replace("]","")
            return ("4", y) #4

    @commands.command()
    async def mensatime(self, ctx, equal=None, arg=None):
        authorname = ctx.author.name
        authormention = ctx.author.mention
        ctxprefix = ctx.prefix

        db_control, response = await self.db_controller(ctxprefix=ctxprefix, authormention=authormention, authorname=authorname, equal=equal, arg=arg)
        if ctxprefix == "my.":
            await ctx.message.add_reaction(':plus1:1171776509195845652')

        match db_control:
            case "0":
                await ctx.message.add_reaction('❌')
            case "1":
                await ctx.send(response)
            case "2":
                await ctx.message.add_reaction('✅')
            case "3":
                await ctx.send("Keine Usertime")
            case "4":
                await ctx.send(f"{authormention} Folgende Mensazeiten sind eingetragen:\n```\n{response}\n```")
            case _:
                await ctx.message.add_reaction('⚠')
        
    @commands.command()
    async def mensamutter(self,ctx):
        await ctx.send("Deine Mom")

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
        username = user.name
        usermention = user.mention
        if user.bot:
            return
        if str(reaction.emoji) == "<:plus1:1171776509195845652>":
            hookname = self.bot.user.name
            webhook = await self.check_for_webhook(reaction.message, hookname)
            msgcontent = reaction.message.content

            webhookmsg = await webhook.send(content=reaction.message.content, avatar_url=user.avatar, username=username)
            
            
            if "my.mensatime" in msgcontent and "=" in msgcontent:
                msgcontentarray = msgcontent.split('=')
                await self.db_controller("my.", usermention, username, '=', msgcontentarray[1])
                await reaction.message.add_reaction('🔄')
                await webhookmsg.add_reaction('✅')
            elif msgcontent == "my.mensatime":
                await self.db_controller("my.", authormention=usermention, authorname=username, equal=None, arg=None)
                await reaction.message.add_reaction('🔄')
            else:
                pass



    @commands.cooldown(1, 20, commands.BucketType.user)
    @commands.command(alias = "Mensa",brief="Zeigt zukünftige Mahlzeiten in der Mensa an")
    async def mensa(self, ctx, pics = 0, date: str ="0"):
        base_url = "https://www.mensa-kl.de/api.php"
        params = {"format": "json", "date": date}

        try:
            response = requests.get(f"{base_url}", params=params)
            response.raise_for_status()
            data = response.json()

            if data:
                if pics == 0:
                    if date == "all":
                        titel = f"Alle nächsten Ausgaben"
                    else:
                        heute = data[0].get("date","Alle Tage")

                        titel = f"Ausgabe am {heute}"
                    
                    embed = discord.Embed(title=titel, color=0x0080FF)  # Du kannst die Farbe anpassen
                    for meal in data:
                        title = meal.get("title", "N/A")
                        price = meal.get("price", "N/A")
                        image_url = meal.get("image", "")
                        ausgabe = meal.get("loc", "")
                        formatted_meal = f"**{title}** - {price}€"
                        embed.add_field(name=f"Ausgabe {ausgabe}", value=formatted_meal, inline=False)
                    embed.set_footer(text="Daten von Mensa-kl.de")
                    await ctx.send(embed=embed)
                elif date == "all":
                    await ctx.send(f"Ich werde dir nicht alle Gerichte mit Bildern geben, das wären {len(data)} Nachrichten!\n Mach lieber +mensa 0 all")
                else:
                    for meal in data:
                        title = meal.get("title_with_additives", "N/A")
                        price = meal.get("price", "N/A")
                        image_url = meal.get("image", "")
                        icon = meal.get("icon", "")
                        ausgabe = meal.get("loc", "Weiß nicht, welche Ausgabe")
                        formatted_meal = f"**{title}** - {price}€"

                        embed = discord.Embed(title=f"Ausgabe {ausgabe}", description = formatted_meal, color=0x0080FF)
                        if image_url:
                            embed.set_image(url=f"https://www.mensa-kl.de/mimg/{image_url}")
                        if icon:
                            embed.set_thumbnail(url=f"https://www.mensa-kl.de/img/{icon}.png")
                        embed.set_footer(text="Daten von Mensa-kl.de")
                        await ctx.send(embed=embed)

            else:
                await ctx.send("Es wurden keine Mahlzeiten gefunden.")

        except Exception as e:
            await ctx.send(f"Fehler beim Abrufen der Mahlzeiten: {str(e)}")


    @tasks.loop(minutes=15.0)
    async def cyclereset(self):
        if datetime.now().strftime("%H") == "15":
            self.user_time_db.remove_nconstants()

    @commands.is_owner()
    @commands.command(brief="reset-db")
    async def reset(self,ctx):
        self.user_time_db.remove_nconstants()
        
async def setup(bot):
    await bot.add_cog(Mensa(bot))
