import discord
from discord import app_commands
from discord.ext import commands

class Slashtest(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @app_commands.command(name="slash", description="Anzeigen")
    async def slashtest(self, interaction: discord.Interaction):
        await interaction.response.send_message("Jo noice")
    
async def setup(client):
    await client.add_cog(Slashtest(client))
