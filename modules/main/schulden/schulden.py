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

    @app_commands.command(name="allschulden", description="[SCHULDEN] Zeige alle Schulden von allen Usern")
    async def allschulden(self,interaction:discord.Interaction):
        if interaction.message.author.id in self.bot.owner_ids:
            self.schulden_db.aktualisieren()
            schulden = self.schulden_db.alle_schulden_anzeigen()
            if type(schulden) != list:
                await interaction.response.send_message(schulden)
            else:
                a,b="Schuldner","Gläubiger"
                returntext = f"{a:14}| > schuldet > | {b:14}| Betrag (EUR.CENT)\n"
                for schuldner,gläubiger, betrag in schulden:
                    returntext += f"{schuldner:14}| > -------- > | {gläubiger:14}| {betrag}\n"
                await interaction.response.send_message(f"```{returntext}```")

    @app_commands.command(name="getschulden", description="[SCHULDEN] Zeige Schuldenverhältnisse von dir an")
    async def getschulden(self, interaction:discord.Interaction):
        self.schulden_db.aktualisieren()
        user0 = interaction.user.name
        eig = self.schulden_db.schulden_anzeigen(schuldner=user0)
        fremd = self.schulden_db.schulden_anzeigen(glaeubiger=user0)
        
        eigene_schulden = eig if eig != "Keine Schulden gefunden." else None
        fremd_schulden = fremd if fremd != "Keine Schulden gefunden." else None

        await interaction.response.send_message(f"```Eigene Schulden an:\n{eigene_schulden}\nFremd Schulden von:\n{fremd_schulden}```", ephemeral=True)

    @app_commands.command(name="addschulden", description="[SCHULDEN] .addschulden @Schuldner Betrag")
    @app_commands.describe(user1 = "An wen gehen die Schulden?", betrag="Wie viel Schulden? XX.XX", comment="Kommentar max 100 Zeichen")
    async def addschulden(self, interaction:discord.Interaction, user1:discord.Member, betrag:str, comment:str=None):
        message_author = interaction.user
        message_author_name = message_author.name
        message_author_id = message_author.id
        user1_name = user1.name
        try: # 
            if (user1 == message_author or user1.id == message_author_id or str(message_author_name) == str(user1_name)) and (interaction.user.bot or user1.bot):
                await interaction.response.send_message("haha sehr witzig", ephemeral=True)
            else:
                try:
                    if "," in betrag:
                        betrag = betrag.replace(",", ".")
                    betragteile = betrag.split(".")
                    if len(betragteile) == 1:
                        betrag += ".00"
                    else:
                        if len(betragteile[1]) > 2:
                            await interaction.response.send_message("Betrag muss zwei Nachkommastellen haben",ephemeral=True)
                            return
                    try:
                        betrag=round(float(betrag),2)
                        
                        if betrag < 0.0:

                            await interaction.response.send_message("negative Schulden sind illegal hab ich beschlossen", ephemeral=True)
                        elif betrag > 500.0:
                            await interaction.response.send_message(f"Ja theoretisch kann man {betrag} Schulden plötzlich machen aber hier erstmal net.")
                        elif comment:

                            if len(comment) > 100:
                                await interaction.response.send_message("Kommentar darf nicht mehr als 100 Zeichen enthalten.")
                                return

                            user0_str = str(message_author_name)
                            user1_str = str(user1_name)
                            
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
                                        await interaction.response.edit_message(content=f"{user1_name} hat akzeptiert.", view=view1)
                                    except Exception as e:
                                        print(f"{e}")
                                        await interaction.response.edit_message(content=f"{user1_name} ERROR", view=view3)
                            accept_button.callback=button_callback
                            print("hier1")

                            async def revoke_callback(interaction:discord.Interaction):
                                if interaction.user == message_author:
                                    await interaction.response.edit_message(content=f"{message_author_name} hat widerrufen.", view=view2)                    
                            revoke_button.callback=revoke_callback

                            print("hier2")
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
                            
                            print("hier3")
                            comment = comment or "-"
                            returntext = f"{user1.mention} muss akzeptieren:\nSchulden in Höhe von \n`{betrag}` an {message_author_name}\nKommentar:\n{comment}"
                            print("hier")
                            await interaction.response.send_message(returntext, view=view0)
                            return
                    except:
                        await interaction.response.send_message("Betrag kann nicht zu einer Zahl konvertiert werden.",ephemeral=True)
                except:
                    await interaction.response.send_message("da passt was nicht", ephemeral=True)
        except:
            await interaction.response.send_message("User not found", ephemeral=True)
        self.schulden_db.aktualisieren()
        #return f"Alter Betrag: {betrag0} Neuer Betrag: {betrag1}"

    @app_commands.command(name="getschuldenlog", description="[SCHULDEN] Einsicht in Datenbank. Ausgabe der kompletten Transaction-History")
    async def getschuldenlog(self, interaction:discord.Interaction):
        bt:commands.Bot = self.bot

        if interaction.user.id in bt.owner_ids:
            interaction.response.send_message(file=discord.File(self.schulden_db.backup_database()))


###Funktion: Log schreiben um streitigkeiten zu vermeiden
             
async def setup(bot):
    await bot.add_cog(Schulden(bot))