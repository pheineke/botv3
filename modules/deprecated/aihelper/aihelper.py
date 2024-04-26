import discord
from discord import app_commands
from discord.ext import commands, tasks
from discord.ui import Button, View

import torch, asyncio, os, subprocess
from concurrent.futures import ThreadPoolExecutor
from transformers import LlamaTokenizer, LlamaForCausalLM


class Aihelper(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.download_file_if_empty()
        self.message_history_limit = 5
        self.tokenizer = LlamaTokenizer.from_pretrained("./modules/main/aihelper/models/alpaca")
        self.model = LlamaForCausalLM.from_pretrained(
            "alpaca",
            load_in_8bit=True,
            torch_dtype=torch.float16,
            device_map="auto"
        )
        self.queue = asyncio.Queue()
        asyncio.get_running_loop().create_task(self.background_task())


    def download_file_if_empty(self, repo_url="https://huggingface.co/NousResearch/Nous-Hermes-13b", save_path="./modules/main/aihelper/models/alpaca"):
        if os.path.exists(save_path) and os.listdir(save_path):
            print("Der angegebene Pfad ist nicht leer.")
        else:
            try:
                # Git-Repository klonen
                subprocess.run(["git", "clone", repo_url, save_path])
                print(f"Das Git-Repository wurde erfolgreich von {repo_url} in {save_path} geklont.")
            except Exception as e:
                print(f"Fehler beim Klonen des Git-Repository: {e}")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user:
            return
        
        if isinstance(message.channel, discord.channel.DMChannel) or (self.bot.user and self.bot.user.mentioned_in(message)) or message.channel.id == 1216430405104959578:
            if message.reference:
                pastMessage = await message.channel.fetch_message(message.reference.message_id)
            else:
                pastMessage = None
            await self.queue.put((message, pastMessage))

    def sync_task(self, message):
        input_ids = self.tokenizer(message, return_tensors="pt").input_ids.to("cuda")
        generated_ids = self.model.generate(input_ids, max_new_tokens=250, do_sample=True, repetition_penalty=1.3, temperature=0.8, top_p=0.75, top_k=40)
        response = self.tokenizer.decode(generated_ids[0][input_ids.shape[-1]:])
        return response

    async def background_task(self):
        executor = ThreadPoolExecutor(max_workers=1)
        loop = asyncio.get_running_loop()
        print("Task Started. Waiting for inputs.")
        while True:
            msg_pair: tuple[discord.Message, discord.Message] = await self.queue.get()
            msg, past = msg_pair

            username = self.bot.user.name
            user_id = self.bot.user.id
            message_content = msg.content.replace(f"@{username} ", "").replace(f"<@{user_id}> ", "")
            past_content = None
            if past:
                past_content = past.content.replace(f"@{username} ", "").replace(f"<@{user_id}> ", "")
            text = self.generate_prompt(message_content, past_content)
            response = await loop.run_in_executor(executor, self.sync_task, text)
            print(f"Response: {text}\n{response}")
            await msg.reply(response, mention_author=False)

    def generate_prompt(self, text, pastMessage):
        if pastMessage:
            return f"""### Instruction:
Your previous response to the prior instruction: {pastMessage}
       
Current instruction to respond to: {text}
### Response:"""
        else:
            return f"""### Instruction:
{text}
### Response:"""

async def setup(bot):
    await bot.add_cog(Aihelper(bot))