import discord
from discord import app_commands
from discord.ext import commands, tasks
from discord.ui import Button, View

import os, sys, json

class Website(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="websitepull", description="[WEBSITE] Update .wwww")
    async def websitepull(self, interaction:discord.Interaction):
        if interaction.user.id in self.bot.owner_ids:
            # Speichere den aktuellen Pfad
            os.chdir("/home/sih18pev/.wwww/")
            await interaction.response.send_message(f"```{os.popen('git pull').read()}```")

    @app_commands.command(name="websitereset", description="[WEBSITE] git reset .wwww")
    async def websitereset(self, interaction:discord.Interaction):
        if interaction.user.id in self.bot.owner_ids:
            # Speichere den aktuellen Pfad
            os.chdir("/home/sih18pev/.wwww/")
            response = f"```{os.popen('git reset --hard').read()}```"
            response += f"```{os.popen('git pull').read()}```"
            await interaction.response.send_message(response)

    @app_commands.command(name="websiteset", description="[WEBSITE] Set own website info")
    async def websiteset(self, interaction:discord.Interaction, website:str):
        key = interaction.user.id
        value = website

        try:
            with open("websitedb.json", 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            data = {}

        data[key] = value

        with open("websitedb.json", 'w') as file:
            json.dump(data, file, indent=4)

        await interaction.response.send_message("Done")

    @app_commands.command(name="website", description="[WEBSITE] Info")
    async def website(self, interaction:discord.Interaction, user:discord.Member):
        try:
            with open("websitedb.json", 'r') as file:
                data = json.load(file)
                website = data.get(user.id)
        except (FileNotFoundError, json.JSONDecodeError):
            website = "No website saved"

        await interaction.response.send_message(website)
                

async def setup(bot):
    await bot.add_cog(Website(bot))