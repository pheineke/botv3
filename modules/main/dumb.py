import asyncio
import random
import discord
from discord import app_commands
from discord.ext import commands, tasks
from discord.ui import Button, View

import datetime
import time

class Dumb(commands.Cog):
    @commands.command()
    async def hrs(self, ctx, user:discord.Member):
        a = random.randint(1, 101)
        x = a //30
        giff0 = ('''⬛️⬛️⬛⬛️⬛️
⬛️⬛️⬛️⬛️⬛️
⬛️⬛️⬛️⬛️⬛️
⬛️⬛️⬛️⬛️⬛️
⬛️⬛️⬛️⬛️⬛️''')
        giff1 = ('''⬛️⬛️​🟥⬛️⬛️
⬛️⬛️​🟥⬛️⬛️
⬛️⬛️⬛️⬛️⬛️
⬛️⬛️⬛️⬛️⬛️
⬛️⬛️⬛️⬛️⬛️''')
        giff2 = ('''⬛️⬛️​🟥🟥🟥
⬛️⬛️​🟥🟥⬛️
⬛️⬛️⬛️⬛️⬛️
⬛️⬛️⬛️⬛️⬛️
⬛️⬛️⬛️⬛️⬛️''')
        giff3 = ('''⬛️⬛️​🟥🟥🟥
⬛️⬛️​🟥🟥🟥
⬛️⬛️🟥🟥🟥
⬛️⬛️⬛️⬛️⬛️
⬛️⬛️⬛️⬛️⬛️''')
        giff4 = ('''⬛️⬛️​🟥🟥🟥
⬛️⬛️​🟥🟥🟥
⬛️⬛️🟥🟥🟥
⬛️⬛️⬛️🟥🟥
⬛️⬛️⬛️⬛️🟥''')
        giff5 = ('''⬛️⬛️​🟥🟥🟥
⬛️⬛️​🟥🟥🟥
⬛️⬛️🟥🟥🟥
⬛️⬛️🟥🟥🟥
⬛️⬛️🟥🟥🟥''')
        giff6 = ('''⬛️⬛️​🟥🟥🟥
⬛️⬛️​🟥🟥🟥
⬛️⬛️🟥🟥🟥
⬛️⬛️🟥🟥🟥
⬛️⬛️🟥🟥🟥''')
        giff7 = ('''⬛️⬛️​🟥🟥🟥
⬛️⬛️​🟥🟥🟥
⬛️⬛️🟥🟥🟥
⬛️🟥🟥🟥🟥
🟥🟥🟥🟥🟥''')
        giff8 = ('''⬛️⬛️​🟥🟥🟥
⬛️⬛️​🟥🟥🟥
🟥🟥🟥🟥🟥
🟥🟥🟥🟥🟥
🟥🟥🟥🟥🟥''')
        giff9 = ('''🟥⬛️​🟥🟥🟥
🟥🟥​🟥🟥🟥
🟥🟥🟥🟥🟥
🟥🟥🟥🟥🟥
🟥🟥🟥🟥🟥''')
        giff10 = ('''🟥🟥🟥🟥🟥
🟥🟥​🟥🟥🟥
🟥🟥🟥🟥🟥
🟥🟥🟥🟥🟥
🟥🟥🟥🟥🟥''')
        
        
        liste = [giff0, giff1, giff2, giff3, giff4, giff5, giff6, giff7, giff8, giff9, giff10]
        msg:discord.Message = await ctx.send(f"{user.mention} dein Hurensohnstatus:\n{liste[0]}")
        for i in range(1, len(liste)):
            await msg.edit(content=f"{user.mention} dein Hurensohnstatus:\n{liste[i]}")
            await asyncio.sleep(2)


    def print_progress_bar(self, progress):
        gif_frames = [
            ['⬛️', '⬛️', '⬛️', '⬛️', '⬛️'],
            ['⬛️', '⬛️', '⬛️', '⬛️', '⬛️'],
            ['⬛️', '⬛️', '⬛️', '⬛️', '⬛️'],
            ['⬛️', '⬛️', '⬛️', '⬛️', '⬛️'],
            ['⬛️', '⬛️', '⬛️', '⬛️', '⬛️'],
            ['⬛️', '⬛️', '⬛️', '⬛️', '⬛️'],
            ['⬛️', '⬛️', '⬛️', '⬛️', '⬛️'],
            ['⬛️', '⬛️', '⬛️', '⬛️', '⬛️'],
            ['⬛️', '⬛️', '⬛️', '⬛️', '⬛️'],
            ['⬛️', '⬛️', '⬛️', '⬛️', '⬛️'],
            ['⬛️', '⬛️', '⬛️', '⬛️', '⬛️']
        ]


    @commands.command()
    @commands.is_owner()
    async def ladebalken2(self, ctx):
        msg:discord.Message = await ctx.send(self.print_progress_bar(0))
        await asyncio.sleep(1)
        for i in range(1,6):
            await msg.edit(self.print_progress_bar(i))
            await asyncio.sleep(1)

async def setup(bot):
    await bot.add_cog(Dumb(bot))