request = \
"""
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=GEMINI_API_KEY" \
-H 'Content-Type: application/json' \
-X POST \
-d '{
  "contents": [{
    "parts":[{"text": "Explain how AI works"}]
    }]
   }'
"""

import os
import tempfile
import discord
from discord import app_commands
from discord.ext import commands, tasks
from discord.ui import Button, View, ButtonStyle

from dotenv import load_dotenv

import requests, json
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta

from google import genai
from google.genai import types

class Gemini(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        load_dotenv()
        self.GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
        


    @app_commands.command(name="talk_gemini", description="Talk with gemini")
    @app_commands.choice(
        name="model",
        description="Model",
        choices=[
            app_commands.OptionChoice(name="gemini-2.0-flash", value="gemini-2.0-flash"),
            app_commands.OptionChoice(name="gemini-2.0-flash-exp", value="gemini-2.0-flash-exp"),
            app_commands.OptionChoice(name="gemini-2.0-flash-thinking-exp", value="gemini-2.0-flash-thinking-exp"),
        ],
    )
    async def talk(self, interaction:discord.Interaction, model:app_commands.Choice[str]=None, text:str=None, attachment:discord.Attachment=None):
        client = genai.Client(
            api_key=self.GEMINI_API_KEY,
            http_options={'api_version':'v1alpha'} if model == 'gemini-2.0-flash-thinking-exp' else {},
        )

        _attachments = []


        for attachment in interaction.attachments:
            if attachment.content_type and attachment.content_type.startswith('image/'):
                _attachments.append(types.Part.from_bytes(attachment, "image/jpeg"))
            
            elif attachment.content_type and attachment.content_type.startswith('audio/'):
                _attachments.append(types.Part.from_bytes(attachment, "audio/mpeg"))


        final_text = text
        if _attachments:
            final_text = text @ _attachments
        
        response = client.models.generate_content(
            model= model,
            contents=final_text,
        )

        await interaction.response.send_message(response.text)

    @app_commands.command(name="imagen_gemini", description="Generate image")
    async def imagen(self, interaction:discord.Interaction, text:str=None, image_num:int=1):
        client = genai.Client(
            api_key=self.GEMINI_API_KEY
        )

        response = client.models.generate_image(
            model= "imagen-3.0-generate-002",
            prompt=text,
            config=types.GenerateImageConfig(
                number_of_images= image_num,
                output_mime_type= 'image/jpeg'
            )
        )

        # Upload images
        for i, image in enumerate(response.images):
            await interaction.response.send_message(f"Image {i+1}", file=discord.File(image))

async def setup(bot):
    await bot.add_cog(Gemini(bot))