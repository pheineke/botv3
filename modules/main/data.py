import discord
from discord.ext import commands
import json
import os

class Data(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def getuserinfo(self, ctx, member: discord.Member = None):
        await ctx.send("Hallo")

        
        

async def setup(bot):
    await bot.add_cog(Data(bot))