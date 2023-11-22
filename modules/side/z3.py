from z3 import *


import os

import discord
from discord.ext import commands


class Z3(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def z3_import(self, ctx, program):
        try:
            ctx.send(program.replace("```python", "").replace("```", ""))
        except:
            await ctx.send("Ungültiges Programm")
        


    


async def setup(bot):
    await bot.add_cog(Z3(bot))