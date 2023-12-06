import asyncio

from sympy import pretty_print
import chess
import os
import discord
from discord.ext import commands

import time
import json

moves = {}
board = chess.Board()

class Chess(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def playchess(self, ctx, user):
        acceptm = await ctx.send(str(user) + " akzeptierst du das Match?")
        await acceptm.add_reaction("✅")
        await asyncio.sleep(30)

        print()


        if user in acceptm.reactions.user:
            await ctx.send("Es geht los")

        moves[ctx.author] = {}
        moves[user] = {}

        pretty_print(moves)
            
    @commands.command()
    async def move(self, ctx, move):
        counter = 0
        if chess.Move.from_uci(move) in board.legal_moves:
            board.push(move)
            moves[ctx.author] = counter

    @commands.command()
    async def board(self, ctx):
        await ctx.send("```\n" + str(board)  + "\n```")


        

async def setup(bot):
    await bot.add_cog(Chess(bot))