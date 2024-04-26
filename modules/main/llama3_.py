import discord
from discord import app_commands
from discord.ext import commands, tasks
from discord.ui import Button, View

import transformers
import torch

class Llama3(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

        

    @app_commands.command(name="llama3", description="Llama3 GPT")
    async def llama3(self, interaction:discord.Interaction, prompt:str):
        await interaction.response.send_message("Processing...")

        pipeline = transformers.pipeline(
        "text-generation",
        model="meta-llama/Meta-Llama-3-8B-Instruct",
        model_kwargs={"torch_dtype": torch.bfloat16},
        device="cuda",
        )

        output = pipeline(prompt)

        await interaction.followup.send(output) 

async def setup(client):
    await client.add_cog(Llama3(client))