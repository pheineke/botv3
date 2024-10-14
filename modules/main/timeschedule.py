import asyncio
import random
import discord
from discord import app_commands
from discord.ext import commands, tasks
from discord.ui import Button, View

from datetime import datetime, timedelta

import requests
import os
import modules.main.mensa.database as database

class Mensa(commands.Cog):
    def __init__(self,bot) -> None:
        self.bot = bot
        self.timetable_path = "./lib/data/timetables/"

    @app_commands.command(name="stundenplan", description="Zeigt den Stundenplan eines Users an, sofern er einen hochgeladen hat.")
    @app_commands.describe(user_selection="Ein User von diesem Server.")
    async def stundenplan(self, interaction: discord.Interaction, user_selection : discord.Member):
        user_selection_id : int = user_selection.id

        try:
            # Specify the path to your file
            file_path = self.timetable_path + f"{user_selection_id}" + ".png"

            # Create a File object
            file = discord.File(file_path, filename="timetable.png")

            # Send the message with the attachment
            await interaction.response.send_message(
                file = file,
                ephemeral = True  # This makes the message only visible to the user who triggered the command
            )

        except Exception as e:
            await interaction.response.send_message(f"An error occurred: {str(e)}", ephemeral=True)

        
    @app_commands.command(name="set_stundenplan", description="Hier kannst du deinen Stundenplan als Bild hochladen.")
    async def set_stundenplan(self, interaction: discord.Interaction):
        user_id : int = interaction.user.id
        attachments = interaction.message.attachments
        
        # Fetch the message
        channel_id = interaction.channel.id
        channel = self.get_channel(channel_id)

        message_id = interaction.message.id
        message = await channel.fetch_message(message_id)

        try: 
            if (attachments) and (len(attachments) == 1):
                attachment = attachments[0]

                if not attachment.content_type.startswith("image/png"):
                    await interaction.response.send_message("The attachment is not a PNG file.", ephemeral=True)
                else:
                    await attachment.save(f"timetable_{user_id}")

                    await message.add_reaction("✅")
        except:
            await message.add_reaction("❌")

async def setup(bot):
    await bot.add_cog(Mensa(bot))
