import asyncio
import os
import discord
from discord.ext import commands

import sqlite3

class Inventar(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    inventories = sqlite3.connect("inventories.db")

    @commands.command()
    async def myinv(self, ctx):
        

        pass


                

async def setup(bot):
    await bot.add_cog(Inventar(bot))