import asyncio
import os

from transformers import AutoProcessor, MusicgenForConditionalGeneration
import scipy

from transformers import VitsModel, AutoTokenizer
import torch


import discord
from discord import app_commands
from discord.ext import commands, tasks
from discord.ui import Button, View


class AiAudio(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        #self.queue = asyncio.Queue()
        #self.worker_task = asyncio.create_task(self.worker())

    def music_transformer(self, model, prompt, length):
        processor = AutoProcessor.from_pretrained(str(model))
        model = MusicgenForConditionalGeneration.from_pretrained(str(model))

        inputs = processor(
            text=[prompt],
            padding=True,
            return_tensors="pt",
        )
        length = 256 * (length / 5)
        audio_values = model.generate(**inputs, max_new_tokens=int(length))


        sampling_rate = model.config.audio_encoder.sampling_rate
        scipy.io.wavfile.write("./audio_gen-out.wav", rate=sampling_rate, data=audio_values[0, 0].numpy())

    def tts_transformer(self,prompt):
        model = VitsModel.from_pretrained("facebook/mms-tts-eng")
        tokenizer = AutoTokenizer.from_pretrained("facebook/mms-tts-eng")

        text = str(prompt)
        inputs = tokenizer(text, return_tensors="pt")

        with torch.no_grad():
            output = model(**inputs).waveform

        scipy.io.wavfile.write("./tts_fb01-out.wav", rate=model.config.sampling_rate, data=output.float().numpy())

    async def worker(self):
        while True:
            interaction, type_, model, prompt, length = await self.queue.get()
            if type_ == "compose":
                self.music_transformer(model, prompt, length)
                await interaction.followup.send("Done", file=lambda: discord.File("./audio_gen-out.wav"))

            elif type_ == "tts":
                self.tts_transformer(prompt)
                await interaction.followup.send("Done", file=lambda: discord.File("./tts_fb01-out.wav"))

            self.queue.task_done()

    @app_commands.command(name="compose", description="Compose an audio sequence with a prompt")
    @app_commands.describe(length="Länge in Sekunden")
    @app_commands.choices(model=[
        app_commands.Choice(name='musicgen-small', value="facebook/musicgen-small"),
        app_commands.Choice(name='musicgen-medium', value="facebook/musicgen-medium"),
        app_commands.Choice(name='musicgen-large', value="facebook/musicgen-large"),
        app_commands.Choice(name='musicgen-melody', value="facebook/musicgen-melody"),
        app_commands.Choice(name='audiogen-medium', value="facebook/audiogen-medium")
    ])
    async def compose(self, interaction:discord.Interaction, prompt:str, length:int=29, model:app_commands.Choice[str]="facebook/musicgen-small"):
        if os.path.exists("./audio_gen-out.wav"):
            os.remove("./audio_gen-out.wav")
        
        await interaction.response.send_message("Processing...")
        #model = model or "facebook/musicgen-small"

        processor = AutoProcessor.from_pretrained(str(model))
        model = MusicgenForConditionalGeneration.from_pretrained(str(model))

        inputs = processor(
            text=[prompt],
            padding=True,
            return_tensors="pt",
        )
        length = 256 * (length / 5)
        audio_values = model.generate(**inputs, max_new_tokens=int(length))


        sampling_rate = model.config.audio_encoder.sampling_rate
        scipy.io.wavfile.write("./audio_gen-out.wav", rate=sampling_rate, data=audio_values[0, 0].numpy())

        await interaction.followup.send("Done", file=lambda: discord.File("./audio_gen-out.wav"))
        if os.path.exists("./audio_gen-out.wav"):
            os.remove("./audio_gen-out.wav")

    @app_commands.command(name="tts", description="Text to speech")
    async def tts_fb01(self, interaction:discord.Interaction, prompt:str):
        if os.path.exists("./tts_fb01-out.wav"):
            os.remove("./tts_fb01-out.wav")

        await interaction.response.send_message("Processing...")
        
        model = VitsModel.from_pretrained("facebook/mms-tts-eng")
        tokenizer = AutoTokenizer.from_pretrained("facebook/mms-tts-eng")

        text = str(prompt)
        inputs = tokenizer(text, return_tensors="pt")

        with torch.no_grad():
            output = model(**inputs).waveform

        scipy.io.wavfile.write("./tts_fb01-out.wav", rate=model.config.sampling_rate, data=output.float().numpy())

        await interaction.followup.send("Done", file=lambda: discord.File("./tts_fb01-out.wav"))        
        if os.path.exists("./tts_fb01-out.wav"):
            os.remove("./tts_fb01-out.wav")

    # @app_commands.command(name="tts", description="Text to speech")
    # @app_commands.describe(speaker_lang = "EN-US ")
    # @app_commands.choices(option=[
    #     app_commands.Choice(name='Default Accent', value='EN-Default'),
    #     app_commands.Choice(name='American Accent', value='EN-US'),
    #     app_commands.Choice(name='British Accent', value='EN-BR'),
    #     app_commands.Choice(name='Indian Accent', value='EN_INDIA'),
    #     app_commands.Choice(name='Australian Accent', value='EN-AU')
    # ])
    # async def tts_melo(self, interaction:discord.Interaction, prompt:str, speaker_lang:app_commands.Choice[str]=None):
    #     if os.path.exists("./tts_fb01-out.wav"):
    #         os.remove("./tts_fb01-out.wav.wav")

    #     await interaction.response.send_message("Processing...")
        
    #     speed = 1.0
    #     device = 'auto'
    #     text = prompt
    #     model = TTS(language='EN_V2', device=device)
    #     speaker_ids= model.hps.data.spk2id

    #     output_path= "tts_melo-out.wav"
    #     model.tts_to_file(text, speaker_ids[speaker_lang], output_path, speed=speed)

    #     await interaction.followup.send("Done", file=discord.File("tts_fb01_out.wav"))        
    #     if os.path.exists("./tts_fb01_out.wav"):
    #         os.remove("./tts_fb01-out.wav")


async def setup(client):
    await client.add_cog(AiAudio(client))
