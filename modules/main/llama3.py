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
        with open("./response.txt", 'w') as file:
            file.write(output)
    
        # Delete the content
        


        await interaction.followup.send(file=discord.File("response.txt")) 
        del output

async def setup(client):
    await client.add_cog(Llama3(client))

# https://llama.meta.com/llama-downloads/