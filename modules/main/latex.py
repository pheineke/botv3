from sympy import *
import matplotlib.pyplot as plt
from PIL import Image

import os
import re
import discord
from discord.ext import commands


class Latex(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    

    @commands.Cog.listener("on_message")
    async def latex_converter(self,message):
        def latex_converter(string):
            if bool(re.search(r"\\[a-zA-Z]+", string)):
                
                try:
                    fig = plt.figure(figsize=(3, 0.5))  # Dimensions of figsize are in inches
                    text = fig.text(
                        x=0.5,  # x-coordinate to place the text
                        y=0.5,  # y-coordinate to place the text
                        s=string,
                        horizontalalignment="center",
                        verticalalignment="center",
                        fontsize=24,
                    )
                    fig.savefig("lateximg.png")
                    imagebgtransparent()

                except Exception as e:
                    print("Konnte nicht konvertieren.")

        def imagebgtransparent():
            img = Image.open("lateximg.png")
            img = img.convert("RGBA")
            datas = img.getdata()

            newData = []
            for item in datas:
                if item[0] >= 200 and item[1] >= 200 and item[2] >= 200:
                    newData.append((255, 255, 255, 0))
                else:
                    newData.append((255, 255, 255, 255))

            img.putdata(newData)
            img.save("lateximg.png", "PNG")


        latex_converter(message.content)
        await message.channel.send(file=discord.File("./lateximg.png"))
        os.remove("./lateximg.png")

async def setup(bot):
    await bot.add_cog(Latex(bot))