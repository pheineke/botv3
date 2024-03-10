import discord
from discord.ext import commands
from discord.ui import Button, View
import asyncio


class PersistentView(discord.ui.View):
    def __init__(self, bot: commands.Bot, user_id: int):
        super().__init__(timeout=None)
        self.bot = bot
        self.user_id = user_id

    @discord.ui.button(label='Red', style=discord.ButtonStyle.red, custom_id='persistent_view:red')
    async def red(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('This is red.', ephemeral=True)

    @discord.ui.button(label='Grey', style=discord.ButtonStyle.grey, custom_id='persistent_view:grey')
    async def grey(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('This is grey.', ephemeral=True)


class Viewtest(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def viewtest(self,ctx):
         button = Button(label="Test", style=discord.ButtonStyle.green)
         view = View().add_item(button)
         await ctx.send("What's your favourite colour?", view=view)


async def setup(bot):
    await bot.add_cog(Viewtest(bot))