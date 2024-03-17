from transformers import pipeline
import scipy

import os

import discord
from discord import app_commands
from discord.ext import commands, tasks
from discord.ui import Button, View


class AiAudio(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        

    @app_commands.command(name="AI Audio Composer", description="Compose an audio sequence with a prompt")
    async def compose(self, interaction:discord.Interaction, prompt:str):

        synthesiser = pipeline("text-to-audio", "facebook/musicgen-small")

        music = synthesiser(prompt, forward_params={"do_sample": True})

        scipy.io.wavfile.write("musicgen_out.wav", rate=music["sampling_rate"], data=music["audio"])

        await interaction.response.send_message(file=discord.File("musicgen_out.wav"))
        if os.path.exists("./musicgen_out.wav"):
            os.remove("./musicgen_out.wav")