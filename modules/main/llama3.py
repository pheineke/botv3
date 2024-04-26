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
        print(response)
        output = response['message']['content']

        split_index = None
        
        if len(output) > 2000:
        # Find the last paragraph boundary within the first 2000 characters
            split_index = output.rfind('\n', 0, 2000)
        
            if split_index == -1:
                # If no paragraph boundary is found, split at 2000 characters
                split_index = 2000
    
        

        embed:discord.Embed = discord.Embed(description=output)
        await interaction.followup.send(embed=embed)

async def setup(client):
    await client.add_cog(Llama3(client))

# https://llama.meta.com/llama-downloads/