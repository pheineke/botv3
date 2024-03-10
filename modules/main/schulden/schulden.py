import asyncio
import os
import discord
from discord.ext import commands

import modules.main.schulden.schuldendb as schuldendb

class Schulden(commands.Cog):
    def __init__(self, bot):
         self.bot = bot
         self.schulden_db = schuldendb.Schuldenverwaltung()
         self.schulden_dir = os.getcwd()

    @commands.command(brief="[SCHULDEN] Zeige alle Schulden von allen Usern")
    @commands.is_owner()
    async def allschulden(self,ctx):
        schulden = self.schulden_db.alle_schulden_anzeigen()
        a,b="Schuldner","Gläubiger"
        returntext = f"{a:14}| {b:14}| Betrag\n"
        for schuldner,gläubiger, betrag in schulden:
            returntext += f"{schuldner:14}| {gläubiger:14}| {betrag}\n"
        await ctx.send(f"```{returntext}```")

    @commands.command(brief="[SCHULDEN] Zeige Schuldenverhältnisse von dir an")
    async def getschulden(self, ctx):
        user0 = ctx.author.name
        eig = self.schulden_db.schulden_anzeigen(schuldner=user0)
        fremd = self.schulden_db.schulden_anzeigen(glaeubiger=user0)
        
        eigene_schulden = eig if eig != "Keine Schulden gefunden." else None
        fremd_schulden = fremd if fremd != "Keine Schulden gefunden." else None

        await ctx.send(f"```Eigene Schulden an:\n{eigene_schulden}\nFremd Schulden von:\n{fremd_schulden}```")

    @commands.command(brief="[SCHULDEN] .addschulden @Schuldner Betrag")
    async def addschulden(self, ctx, user1=None, betrag=None):
        self.schulden_db.aktualisieren()
        if user1 == ctx.author:
            await ctx.send("haha sehr witzig")
        else:
            try:
                user1 = await commands.MemberConverter().convert(ctx, user1)
                if betrag is None:
                    await ctx.send("nö kein geld")
                else:
                    try:
                        betrag=float(betrag)
                    except:
                        await ctx.message.add_reaction('❌')

                    user0_str = str(ctx.author.name)
                    user1_str = str(user1.name)
                    print(f"{user0_str} {user1_str}")

                    def check(r: discord.Reaction, u: discord.Member):  # r = discord.Reaction, u = discord.Member or discord.User.
                        return u.id == user1.id and r.message.channel.id == ctx.channel.id and \
                            str(r.emoji) == '✅'
                    
                    try:
                        sent_message = await ctx.send(f"{user1.mention} muss die Schulden bestätigen:")
                        await sent_message.add_reaction('✅')

                        reaction, _ = await self.bot.wait_for('reaction_add', check=check, timeout=60.0)
                        if reaction:
                            try:
                                self.schulden_db.schulden_hinzufuegen(user1_str, user0_str, betrag=betrag)
                            except Exception as e:
                                print(f"{e}")
                                await sent_message.add_reaction('⚠')
                        
                    except asyncio.TimeoutError:
                        await ctx.message.add_reaction('🕒')
                        await ctx.message.add_reaction('❌')
                    except Exception as e:
                        print(f"Ein Fehler ist aufgetreten: {e}")
                    
                    finally:
                        self.schulden_db.aktualisieren()
            except:
                await ctx.send("ne den typen gibts net")
        #return f"Alter Betrag: {betrag0} Neuer Betrag: {betrag1}"


###Funktion: Log schreiben um streitigkeiten zu vermeiden
             
async def setup(bot):
    await bot.add_cog(Schulden(bot))