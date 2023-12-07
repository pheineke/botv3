import os

import discord
from discord.ext import commands


class Minecraftserver(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def startmcserver(self, ctx):
        await ctx.send(f"```{os.popen('sh ~/Minecraft/serverDez2023/start.sh').read()}```")

async def setup(bot):
    await bot.add_cog(Minecraftserver(bot))