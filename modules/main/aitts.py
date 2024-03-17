import asyncio
from transformers import AutoProcessor, MusicgenForConditionalGeneration
import scipy

import os

import discord
from discord import app_commands
from discord.ext import commands, tasks
from discord.ui import Button, View


class AiAudio(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        

    @app_commands.command(name="compose", description="Compose an audio sequence with a prompt")
    async def compose(self, interaction:discord.Interaction, prompt:str):
        
        await interaction.response.send_message("Processing...")
        
    
        processor = AutoProcessor.from_pretrained("facebook/musicgen-small")
        model = MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-small")

        inputs = processor(
            text=[prompt],
            padding=True,
            return_tensors="pt",
        )

        audio_values = model.generate(**inputs, max_new_tokens=256)


        sampling_rate = model.config.audio_encoder.sampling_rate
        scipy.io.wavfile.write("audio_gen-out.wav", rate=sampling_rate, data=audio_values[0, 0].numpy())

        await interaction.followup.send("Done", file=discord.File("audio_gen-out.wav"))
        if os.path.exists("./audio_gen-out.wav"):
            os.remove("./audio_gen-out.wav")


async def setup(client):
    await client.add_cog(AiAudio(client))
