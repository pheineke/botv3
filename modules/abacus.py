import os

import discord
from discord.ext import commands


class Abacus(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



    reg = []

    pc = 0


    @commands.command
    async def setreg(self, ctx, zahl):
        try:
            n = int(zahl)
            reg = [k for k in range(n)]
        except:
            await ctx.send("Ungültige Registeranzahl")
        


    def mov(rd,c):
        reg[rd] = c

    def addi(rd, rl, c):
        reg[rd] = rl + c

    def subi(rd, rl, c):
        reg[rd] = rl - c


    


async def setup(bot):
    await bot.add_cog(Abacus(bot))