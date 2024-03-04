import discord
from discord.ext import commands
import json
import os
import pprint

class Data(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel_id = None
        self.key = None

    @commands.is_owner()
    @commands.command()
    async def channel(self, ctx, id=None):
        if id is None:
            self.channel = self.bot.get_channel(ctx.message.channel)
        else:
            self.channel = self.client.get_channel(id)
        await self.channel.send("ChannelID set")
    
    @commands.is_owner()
    @commands.command()
    async def key(self, ctx, key):
        self.key = key

    @commands.Cog.listener("on_message")
    async def on_message(self, message):
        decodemsg = str(message.content).decode()

        

async def setup(bot):
    await bot.add_cog(Data(bot))