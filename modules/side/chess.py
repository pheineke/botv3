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
        players = []
        def check(reaction, user):
                players.append(user)


        acceptm = await ctx.send(str(user) + " akzeptierst du das Match?")
        
        await acceptm.add_reaction("✅")

        moves[ctx.author] = {}
        moves[user] = {}

        time.sleep(5)
        check(acceptm.reactions, user)

        if (user in players):
            await ctx.send("Es geht los")
            
            
    @commands.command()
    async def move(self, ctx, move):
        if chess.Move.from_uci(move) in board.legal_moves:
            board.push(move)

    @commands.command()
    async def board(self, ctx):
        await ctx.send("```\n" + str(board)  + "\n```")


        

async def setup(bot):
    await bot.add_cog(Chess(bot))