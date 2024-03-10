import discord
from discord import app_commands
from discord.ext import commands, tasks
from discord.ui import Button, View


class Help(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="help", description="Help-Message")
    async def help(self, interaction: discord.Interaction):
        command_info = ""  # Declare command_info outside the loop
        for cog in self.bot.cogs.values():
            if isinstance(cog, commands.Cog):
                commands_list = cog.get_commands()
                if commands_list:
                    cog_name = cog.qualified_name if cog.qualified_name else "No Category"
                    for command in commands_list:
                        short_description = command.brief or "Keine kurze Beschreibung verfügbar."
                        command_info += f"`{command.name}` - {short_description}\n"  # Accumulate command_info properly
        if command_info:  # Check if command_info is not empty before sending
            await interaction.response.send(command_info)
        else:
            await interaction.response.send("No commands found.")

        button0 = Button(label="fsin.fo",url="https://www.fachschaft.informatik.uni-kl.de")
        button1 = Button(label="olat",url="https://olat.vcrp.de/dmz/")
        button2 = Button(label="qis",url="https://qis.verw.uni-kl.de/")
        button3 = Button(label="semestertermine", url="https://rptu.de/studium/im-studium/fristen-und-termine")

        view = View()\
            .add_item(button0)\
            .add_item(button1)\
            .add_item(button2)\
            .add_item(button3)
        await interaction.response.send("**Nützliche Seiten:**", view=view, ephemeral=True)

async def setup(bot):
    await bot.add_cog(Help(bot))