import discord
from discord import app_commands
from discord.ext import commands, tasks
from discord.ui import Button, View

import os, sys
class Website(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="websitepull", description="[WEBSITE] Update .wwww")
    async def websitepull(self, interaction:discord.Interaction):
        if interaction.user.id in self.bot.owner_ids:
            # Speichere den aktuellen Pfad
            os.chdir("$HOME/.wwww/")
            await interaction.response.send_message(f"```{os.popen('git pull').read()}```")

    @app_commands.command(name="websitereset", description="[WEBSITE] git reset .wwww")
    async def websitereset(self, interaction:discord.Interaction):
        if interaction.user.id in self.bot.owner_ids:
            # Speichere den aktuellen Pfad
            os.chdir("$HOME/.wwww/")
            response = f"```{os.popen('git reset --hard').read()}```"
            response += f"```{os.popen('git pull').read()}```"
            await interaction.response.send_message(response)
            

async def setup(bot):
    await bot.add_cog(Website(bot))