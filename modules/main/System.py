import discord
from discord.ext import commands

class System(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def savechat(self, ctx):
        async for message in ctx.channel.history(limit=None):
            user_name = message.author.name
            message_content = message.content

            with open(f"{ctx.channel.name}_messages.txt", "a") as file:
                file.write(f'{{ "{user_name}" : "{message_content}" }}\n')
async def setup(bot):
    await bot.add_cog(System(bot))