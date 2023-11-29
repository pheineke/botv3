from sympy import *

import os
import re
import discord
from discord.ext import commands


class Latex(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener("on_message")
    async def latex_converter(self,message):
        string = message.content.lower()
        if bool(re.search(r"\\[a-zA-Z]+", string)):
            
            try:
                preview(fr'$$\{string}$$', viewer='file', filename='latexequation.png', euler=False, dvioptions=['-D','300'])
                file = discord.File("./latexequation.png")
                await message.channel.send(file=file)
            except Exception as e:
                print("Konnte nicht konvertieren.")
                print(e)
                print(string)

async def setup(bot):
    await bot.add_cog(Latex(bot))