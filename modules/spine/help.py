import discord
from discord import app_commands
from discord.ext import commands, tasks
from discord.ui import Button, View


class Help(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx, arg=None):
        command_info = {}  # Use a dictionary to store commands categorized by brief category
        briefcategories = []
        for cog in self.bot.cogs.values():
            if isinstance(cog, commands.Cog):
                commands_list = cog.get_commands()
                if commands_list:
                    cog_name = cog.qualified_name if cog.qualified_name else "No Category"
                    for command in commands_list:
                        commandbrief = str(command.brief)
                        briefcategory, commandbrief = commandbrief.split("]") if "]" in commandbrief else ("_", None)
                        briefcategories.append(briefcategory)

                        short_description = commandbrief or "Keine kurze Beschreibung verfügbar."
                        if briefcategory not in command_info:
                            command_info[briefcategory] = []
                        command_info[briefcategory].append(f"`{command.name}` - {short_description}")


        # Sort the command descriptions by brief category
        sorted_command_info = sorted(command_info.items(), key=lambda x: x[0])
        returntext = ""
        if sorted_command_info:  # Check if sorted_command_info is not empty before sending
            for category, commands_ in sorted_command_info:
                formatted_category = str(category.strip("["))
                formatted_commands = str('\n'.join(commands_))
                if not arg:
                    returntext += f"***{formatted_category}***\n{formatted_commands}\n"
                else:
                    
                    if arg in formatted_category or arg in formatted_commands:
                        returntext += f"***{formatted_category}***\n{formatted_commands}\n"
                    else:
                        pass
            await ctx.send(returntext)
        else:
            await ctx.send("No commands found.")


    @app_commands.command(name="help", description="Help-Message")
    async def help_(self, interaction: discord.Interaction, arg: str=None):
        command_info = {}  # Use a dictionary to store commands categorized by brief category
        briefcategories = []
        for cog in self.bot.cogs.values():
            if isinstance(cog, commands.Cog) or isinstance(cog, app_commands):
                commands_list = cog.get_commands()
                commands_list += self.bot.tree.get_commands(type=discord.AppCommandType.chat_input)
                if commands_list:
                    cog_name = cog.qualified_name if cog.qualified_name else "No Category"
                    for command in commands_list:
                        try:
                            commandbrief = str(command.brief)
                        except:
                            commandbrief = str(command.description)
                        briefcategory, commandbrief = commandbrief.split("]") if "]" in commandbrief else ("_", None)
                        briefcategories.append(briefcategory)

                        short_description = commandbrief or "Keine kurze Beschreibung verfügbar."
                        if briefcategory not in command_info:
                            command_info[briefcategory] = []
                        command_info[briefcategory].append(f"`{command.name}` - {short_description}")


        # Sort the command descriptions by brief category
        sorted_command_info = sorted(command_info.items(), key=lambda x: x[0])
        returntext = ""
        if sorted_command_info:  # Check if sorted_command_info is not empty before sending
            for category, commands_ in sorted_command_info:
                formatted_category = str(category.strip("["))
                formatted_commands = str('\n'.join(commands_))
                if not arg:
                    returntext += f"***{formatted_category}***\n{formatted_commands}\n"
                else:
                    
                    if arg in formatted_category or arg in formatted_commands:
                        returntext += f"***{formatted_category}***\n{formatted_commands}\n"
                    else:
                        pass
            await interaction.response.send_message(returntext)
        else:
            await interaction.response.send_message("No commands found.")

        button0 = Button(label="fsin.fo",url="https://www.fachschaft.informatik.uni-kl.de")
        button1 = Button(label="olat",url="https://olat.vcrp.de/dmz/")
        button2 = Button(label="qis",url="https://qis.verw.uni-kl.de/")
        button3 = Button(label="semestertermine", url="https://rptu.de/studium/im-studium/fristen-und-termine")

        view = View()\
            .add_item(button0)\
            .add_item(button1)\
            .add_item(button2)\
            .add_item(button3)
        await interaction.response.send_message("**Nützliche Seiten:**", view=view, ephemeral=True)


async def setup(bot):
    await bot.add_cog(Help(bot))