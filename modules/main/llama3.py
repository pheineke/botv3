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

        def split_message(content):
            MAX_LENGTH = 2000
            chunks = []

            while len(content) > MAX_LENGTH:
                # Finde das nächste Leerzeichen vor dem MAX_LENGTH
                last_space_index = content.rfind(' ', 0, MAX_LENGTH)

                # Wenn kein Leerzeichen gefunden wurde, schneide einfach bei MAX_LENGTH ab
                if last_space_index == -1:
                    chunk = content[:MAX_LENGTH]
                    content = content[MAX_LENGTH:]
                else:
                    # Andernfalls schneide bis zum letzten Leerzeichen ab
                    chunk = content[:last_space_index]
                    content = content[last_space_index + 1:]  # Überspringe das Leerzeichen

                # Überprüfe, ob der nächste Block einen Code-Block enthält
                next_code_index = content.find('```')
                if next_code_index != -1 and next_code_index < MAX_LENGTH:
                    # Wenn der nächste Block einen Code-Block enthält und innerhalb der Grenze liegt,
                    # füge den Code-Block dem aktuellen Chunk hinzu
                    code_block_end_index = content.find('```', next_code_index + 3)
                    if code_block_end_index != -1:
                        chunk += content[next_code_index:code_block_end_index + 3]
                        content = content[code_block_end_index + 3:]

                chunks.append(chunk)

            # Füge den verbleibenden Teil hinzu (wenn er existiert)
            if content:
                chunks.append(content)

            return chunks
            
        parts = split_message(output)
        for x in parts:
            if x != '': 
                await interaction.followup.send(x)

async def setup(client):
    await client.add_cog(Llama3(client))

# https://llama.meta.com/llama-downloads/