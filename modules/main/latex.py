from sympy import *
import matplotlib.pyplot as plt

import os
import re
import discord
from discord.ext import commands


class Latex(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener("on_message")
    async def latex_converter(self,message):
        string = message.content
        if bool(re.search(r"\\[a-zA-Z]+", string)):
            
            try:
                fig = plt.figure(figsize=(3, 0.5))  # Dimensions of figsize are in inches
                text = fig.text(
                    x=0.5,  # x-coordinate to place the text
                    y=0.5,  # y-coordinate to place the text
                    s=string,
                    horizontalalignment="center",
                    verticalalignment="center",
                    fontsize=16,
                )

                fig.savefig("latexequation.png")

                file = discord.File("./latexequation.png")
                await message.channel.send(file=file)
            except Exception as e:
                print("Konnte nicht konvertieren.")
                print(e)
                print(string)

async def setup(bot):
    await bot.add_cog(Latex(bot))