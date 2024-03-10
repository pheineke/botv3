import discord
from discord import app_commands
from discord.ext import commands, tasks
from discord.ui import Button, View
import asyncio
import os
import modules.main.schulden.schuldendb as schuldendb

class Schulden(commands.Cog):
    def __init__(self, bot):
         self.bot = bot
         self.schulden_db = schuldendb.Schuldenverwaltung()
         self.schulden_dir = os.getcwd()

    @commands.command(brief="[SCHULDEN] Zeige alle Schulden von allen Usern")
    @commands.is_owner()
    async def allschulden(self,ctx):
        self.schulden_db.aktualisieren()
        schulden = self.schulden_db.alle_schulden_anzeigen()
        if type(schulden) != list:
            await ctx.send(schulden)
        else:
            a,b="Schuldner","Gläubiger"
            returntext = f"{a:14}| > schuldet > | {b:14}| Betrag (EUR.CENT)\n"
            for schuldner,gläubiger, betrag in schulden:
                returntext += f"{schuldner:14}| > -------- > | {gläubiger:14}| {betrag}\n"
            await ctx.send(f"```{returntext}```")

    @commands.command(brief="[SCHULDEN] Zeige Schuldenverhältnisse von dir an")
    async def getschulden(self, ctx):
        self.schulden_db.aktualisieren()
        user0 = ctx.author.name
        eig = self.schulden_db.schulden_anzeigen(schuldner=user0)
        fremd = self.schulden_db.schulden_anzeigen(glaeubiger=user0)
        
        eigene_schulden = eig if eig != "Keine Schulden gefunden." else None
        fremd_schulden = fremd if fremd != "Keine Schulden gefunden." else None

        await ctx.send(f"```Eigene Schulden an:\n{eigene_schulden}\nFremd Schulden von:\n{fremd_schulden}```")

    @app_commands.command(name="", description="[SCHULDEN] .addschulden @Schuldner Betrag")
    async def addschulden(self, interaction:discord.Interaction, user1:discord.Member, betrag=None, comment=None):
        try:
            if user1 == interaction.author or user1.id == interaction.author.id or str(interaction.author.name) == str(user1.name) or interaction.author.bot or user1.bot:
                await interaction.response.send_message("haha sehr witzig", ephemeral=True)
            else:
                try:
                    if betrag is None:
                        await interaction.response.send_message("nö kein geld", ephemeral=True)
                    else:
                        betrag=round(float(str(betrag).replace(",",".")),2)
                        if betrag < 0.0:
                            await interaction.response.send_message("negative Schulden sind illegal hab ich beschlossen", ephemeral=True)
                        elif betrag > 500.0:
                            await interaction.response.send_message(f"Ja theoretisch kann man {betrag} Schulden plötzlich machen aber hier erstmal net.")
                        elif len(comment) > 100:
                            await interaction.response.send_message("Kommentar darf nicht mehr als 100 Zeichen enthalten.")
                        else:
                            user0_str = str(interaction.author.name)
                            user1_str = str(user1.name)
                            
                            accept_button = Button(label="Accept", style=discord.ButtonStyle.blurple)
                            revoke_button = Button(label="Revoke", style=discord.ButtonStyle.red)
                            
                            closed_acc_button = Button(label="✅",style=discord.ButtonStyle.gray, disabled=True)
                            closed_rev_button = Button(label="🔄",style=discord.ButtonStyle.gray, disabled=True)
                            closed_none_button = Button(label="···",style=discord.ButtonStyle.gray, disabled=True)
                            error_button = Button(label="⚠",style=discord.ButtonStyle.gray, disabled=True)

                            async def button_callback(interaction:discord.Interaction):
                                if interaction.user == user1:
                                    try:
                                        self.schulden_db.schulden_hinzufuegen(schuldner=user1_str, glaeubiger=user0_str, betrag=betrag, comment=comment)
                                        await interaction.response.edit_message(content=f"{user1.name} hat akzeptiert.", view=view1)
                                    except Exception as e:
                                        print(f"{e}")
                                        await interaction.response.edit_message(content=f"{user1.name} ERROR", view=view3)
                            accept_button.callback=button_callback

                            async def revoke_callback(interaction:discord.Interaction):
                                if interaction.user == interaction.author:
                                    await interaction.response.edit_message(content=f"{interaction.author.name} hat widerrufen.", view=view2)                    
                            revoke_button.callback=revoke_callback

                            view0 = View(timeout=30)\
                                .add_item(accept_button)\
                                .add_item(revoke_button)
                            view1 = View()\
                                .add_item(closed_acc_button)\
                                .add_item(closed_none_button)
                            view2 = View()\
                                .add_item(closed_none_button)\
                                .add_item(closed_rev_button)
                            view3 = View()\
                                .add_item(error_button)
                            
                            comment = comment or "-"
                            returntext = f"{user1.mention} muss akzeptieren:\nSchulden in Höhe von \n`{betrag}` an {interaction.author.name}\nKommentar:\n{comment}"
                            await interaction.response.send(returntext, view=view0)

                            '''try:
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
                                self.schulden_db.aktualisieren()'''
                except:
                    await interaction.response.send("da passt was nicht", ephemeral=True)
        except:
            await interaction.response.send("User not found", ephemeral=True)
        self.schulden_db.aktualisieren()
        #return f"Alter Betrag: {betrag0} Neuer Betrag: {betrag1}"

    @app_commands.command(name="getschuldenlog", description="[SCHULDEN] .getschulden um Einsicht in die Datenbank zu erhalten. Der Bot wird die gesamte Datenbank inklusive Transaction-History ausgeben.")
    async def getschuldenlog(self, interaction:discord.Interaction):
        bt:commands.Bot = self.bot

        if interaction.user.id in bt.owner_ids:
            interaction.response.send_message(file=discord.File(self.schulden_db.backup_database()))


###Funktion: Log schreiben um streitigkeiten zu vermeiden
             
async def setup(bot):
    await bot.add_cog(Schulden(bot))