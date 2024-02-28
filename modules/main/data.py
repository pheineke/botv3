import discord
from discord.ext import commands

class Data(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def getuserinfo(self, ctx):

        userdata = {

        }
        member = ctx.author
        await ctx.send(f"Benutzername: {member.name}")
        await ctx.send(f"Benutzer-ID: {member.id}")
        await ctx.send(f"Status: {member.desktop_status}")
        await ctx.send("Rollen:")
        for role in member.roles:
            await ctx.send(role.name)

async def setup(bot):
    await bot.add_cog(Data(bot))