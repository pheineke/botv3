import discord
from discord import app_commands
from discord.ext import commands, tasks
from discord.ui import Button, View

import os, sys, json

class Website(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="websitepull", description="Update .wwww")
    async def websitepull(self, interaction:discord.Interaction):
        if interaction.user.id in self.bot.owner_ids:
            # Speichere den aktuellen Pfad
            os.chdir("/home/sih18pev/.wwww/")
            await interaction.response.send_message(f"```{os.popen('git pull').read()}```")

    @app_commands.command(name="websitereset", description="git reset .wwww")
    async def websitereset(self, interaction:discord.Interaction):
        if interaction.user.id in self.bot.owner_ids:
            # Speichere den aktuellen Pfad
            os.chdir("/home/sih18pev/.wwww/")
            response = f"```{os.popen('git reset --hard').read()}```"
            response += f"```{os.popen('git pull').read()}```"
            await interaction.response.send_message(response)

    @app_commands.command(name="websiteset", description="Set own website info")
    async def websiteset(self, interaction:discord.Interaction, rhrkusername:str):
        key = interaction.user.id
        value = rhrkusername
        try:
            with open("websitedb.json", 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            data = {}

        data[key] = value

        with open("websitedb.json", 'w') as file:
            json.dump(data, file, indent=4)

        await interaction.response.send_message("Done")

    @app_commands.command(name="website", description="Info")
    async def website(self, interaction:discord.Interaction, user:discord.Member):
        try:
            with open("websitedb.json", 'r') as file:
                data = json.load(file)
                username = data.get(str(user.id))
        except (FileNotFoundError, json.JSONDecodeError):
            username = None
        
        if username:
            await interaction.response.send_message(f"https://www-user.rhrk.uni-kl.de/~{username}/index.html")
        else:
            await interaction.response.send_message("No website saved")
                

async def setup(bot):
    await bot.add_cog(Website(bot))