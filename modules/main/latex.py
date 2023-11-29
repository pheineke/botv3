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
        def imagebgtransparent(image):
            img = Image.open(image)
            img = img.convert("RGBA")
            datas = img.getdata()

            newData = []
            for item in datas:
                if item[0] == 255 and item[1] == 255 and item[2] == 255:
                    newData.append((255, 255, 255, 0))
                else:
                    newData.append(item)

            img.putdata(newData)
            img.save(image, "PNG")


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

                fig.savefig("lateximg.png")
                imagebgtransparent("lateximg.png")

                file = discord.File("./lateximg.png")
                await message.channel.send(file=file)
            except Exception as e:
                print("Konnte nicht konvertieren.")
                print(e)
                print(string)

async def setup(bot):
    await bot.add_cog(Latex(bot))