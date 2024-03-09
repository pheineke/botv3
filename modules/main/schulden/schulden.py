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

    @commands.command()
    @commands.is_owner()
    async def allschulden(self,ctx):
        schulden = self.schulden_db.alle_schulden_anzeigen()
        await ctx.send(f"```{schulden}```")

    @commands.command()
    async def getschulden(self, ctx):
        user0 = ctx.author.name
        eigene_schulden = self.schulden_db.schulden_anzeigen(schuldner=user0)
        fremd_schulden = self.schulden_db.schulden_anzeigen(glaeubiger=user0)

        await ctx.send(f"```Eigene Schulden an:\n{eigene_schulden}\nFremd Schulden von:\n{fremd_schulden}```")

    @commands.command(brief=".addschulden @Schuldner Betrag")
    async def addschulden(self, ctx, user1: discord.Member, betrag):
        self.schulden_db.aktualisieren()
        if user1 == ctx.author:
            await ctx.send("haha sehr witzig")
        elif user1 not in ctx.guild.members:
            await ctx.send("ne den typen gibts net")
        elif betrag is None:
            await ctx.send("nö kein geld")
        else:
            try:
                betrag=float(betrag)
            except:
                await ctx.message.add_reaction('❌')

            user0_str = str(ctx.author.name)
            user1_str = str(user1.name)

            def check(r: discord.Reaction, u: discord.Member):  # r = discord.Reaction, u = discord.Member or discord.User.
                return u.id == ctx.author.id and r.message.channel.id == ctx.channel.id and \
                    str(r.emoji) == '✅'
            
            try:
                sent_message = await ctx.send(f"{user1.mention} muss die Schulden bestätigen:")
                await sent_message.add_reaction('✅')

                reaction, _ = await self.bot.wait_for('reaction_add', check=check, timeout=30)
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
        #return f"Alter Betrag: {betrag0} Neuer Betrag: {betrag1}"


###Funktion: Log schreiben um streitigkeiten zu vermeiden
             
async def setup(bot):
    await bot.add_cog(Schulden(bot))