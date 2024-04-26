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
        message = await interaction.original_response()

        response = ollama.chat(model='llama3', messages=[
        {
            'role': 'user',
            'content': f'{prompt}',
        },
        ])
        print(response)
        output = response['message']['content']

        def split_message_with_code(content):
            MAX_LENGTH = 2000
            chunks = []
            code_block_started = False

            while len(content) > MAX_LENGTH:
                # Finde das nächste Vorkommen von '```'
                next_code_index = content.find('```')

                if next_code_index != -1 and next_code_index < MAX_LENGTH:
                    # Wenn '```' innerhalb des Limits gefunden wurde, füge einen neuen Chunk hinzu,
                    # der bis zum nächsten '```' geht
                    code_block_end_index = content.find('```', next_code_index + 3)
                    if code_block_end_index != -1:
                        chunks.append(content[:code_block_end_index + 3])
                        content = content[code_block_end_index + 3:]
                        code_block_started = False
                        continue  # Springe zum nächsten Schleifendurchlauf

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

                # Wenn ein Codeblock begonnen hat, füge den aktuellen Chunk dem vorherigen hinzu
                if code_block_started:
                    chunks[-1] += chunk
                else:
                    chunks.append(chunk)
                code_block_started = True

            # Füge den verbleibenden Teil hinzu (wenn er existiert)
            if content:
                chunks.append(content)

            return chunks
            
        parts = split_message_with_code(output)
        parts01 = [':white_larawait create_thread(*, name, auto_archive_duration=in-minutes)ge_square: :white_large_square: :white_large_square: '] + parts + [':white_large_square: :white_large_square: :white_large_square: ']

        for x in parts01:
            if x != '':
                await message.channel.send(x)

async def setup(client):
    await client.add_cog(Llama3(client))

# https://llama.meta.com/llama-downloads/