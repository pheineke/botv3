import discord
from discord import app_commands
from discord.ext import commands, tasks
from discord.ui import Button, View

import ollama

class Llama3(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

        

    @app_commands.command(name="llama3", description="Llama3 GPT")
    async def llama3(self, interaction:discord.Interaction, prompt:str):
        await interaction.response.send_message("Processing...")

        response = ollama.chat(model='llama3', messages=[
        {
            'role': 'user',
            'content': f'{prompt}',
        },
        ])
        output = response['message']['content']

        await interaction.followup.send(output) 

async def setup(client):
    await client.add_cog(Llama3(client))

# https://llama.meta.com/llama-downloads/