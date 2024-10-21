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

class Timetable(commands.Cog):
    def __init__(self,bot) -> None:
        self.bot = bot
        self.timetable_path = "./lib/data/timetables/"

    @app_commands.command(name="timetables", description="See all Users who have uploaded their timetables")
    async def timetables(self, interaction: discord.Interaction):
        message = ""

        try:
            for filename in os.listdir(self.timetable_path):
                filepath = os.path.join(self.timetable_path, filename)
                if os.path.isfile(filepath):
                    print(f'File: {filepath}')
                    if "timetable_" in filepath:
                        a = filepath.removeprefix("timetable_")
                        b = a.removesuffix(".png")
                        user : discord.User = await self.bot.get_user(int(b))
                        message += f"{user.name} - {user.mention}\n"

                elif os.path.isdir(filepath):
                    pass
                    #print(f'Directory: {filepath}')

            # Send the message with the attachment
            await interaction.response.send_message(
                message,
                ephemeral = True  # This makes the message only visible to the user who triggered the command
            )

        except FileNotFoundError as e:
            await interaction.response.send_message(f"User timetable doesnt exist", ephemeral=True)
        except Exception as e:  
            await interaction.response.send_message(f"Error {e}", ephemeral=True)

    @app_commands.command(name="timetable", description="Shows timetable of user if uploaded")
    @app_commands.describe(user_selection="User from this server")
    async def timetable(self, interaction: discord.Interaction, user_selection : discord.Member):
        user_selection_id : int = user_selection.id

        try:
            # Specify the path to your file
            file_path = self.timetable_path + f"timetable_{user_selection_id}" + ".png"

            # Create a File object
            file = discord.File(file_path, filename="timetable.png")

            # Send the message with the attachment
            await interaction.response.send_message(
                file = file,
                ephemeral = True  # This makes the message only visible to the user who triggered the command
            )

        except FileNotFoundError as e:
            await interaction.response.send_message(f"User timetable doesnt exist", ephemeral=True)
        except Exception as e:  
            await interaction.response.send_message(f"Error {e}", ephemeral=True)


        
    @app_commands.command(name="my_timetable", description="Upload your personal time schedule for this semester here")
    async def my_timetable(self, interaction: discord.Interaction, file: discord.Attachment):
        user_id : int = interaction.user.id
        
        # Fetch the message
        #original_message = await interaction.original_response()

        try: 
            if file:

                if not file.content_type.startswith("image/png"):
                    await interaction.response.send_message("The attachment is not a PNG file.", ephemeral=True)
                else:
                    await file.save(f"./lib/data/timetables/timetable_{user_id}.png")
                    
                    await interaction.response.send_message("Timetable uploaded.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"Error. {e}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Timetable(bot))
