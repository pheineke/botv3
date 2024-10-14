import discord
from discord import app_commands
from discord.ext import commands, tasks
from discord.ui import Button, View

import json

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
                        cog_class, commandbrief = commandbrief.split("]") if "]" in commandbrief else ("_", None)
                        briefcategories.append(cog_class)

                        short_description = commandbrief or "Keine kurze Beschreibung verfügbar."
                        if cog_class not in command_info:
                            command_info[cog_class] = []
                        command_info[cog_class].append(f"`{command.name}` - {short_description}")


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
    @app_commands.describe(arg = "Nach commands filtern bzw. iwas was im command steht")
    async def help_(self, interaction: discord.Interaction, arg: str=None):
        def add_command(command_name, cog_class, description) -> dict:
            return {
                "command" : f"{command_name}",      # "command" : "test"
                "class" : f"{cog_class}",           # "class" : "test_cog"
                "description" : f"{description}"    # "description" : "test description"
            }
        
        info = {
            #"class_name" :
            #    [
            #        
            #    ]
        }

        for cog in self.bot.cogs.values():
            cog_class = str(cog.__cog_name__)
            info[cog_class] = {}
            if isinstance(cog, commands.Cog):
                commands_list = cog.get_commands() + cog.get_app_commands()

                info[cog_class] = {"is_cog" : True, "commands" : []}

                if commands_list:
                    for command in commands_list:

                        cog_class = str(cog.__cog_name__)

                        if isinstance(command, discord.app_commands.Command):
                            commandbrief = str(command.description) or "Keine Kurzbeschreibung verfügbar"
                        else:
                            commandbrief = (str(command.brief)) or "Keine Kurzbeschreibung verfügbar"
                            
                        
                        command_dict = add_command(
                            command_name=str(command.name),
                            cog_class=str(cog_class),
                            description=str(commandbrief)
                        )

                        info[cog_class]['commands'].append(command_dict)

                        

        

        sorted_command_info = dict(sorted(info.items()))

        f = open("command_data", 'w')
        f.write(json.dumps(info, indent=3))
        f.close()

        button0 = Button(label="fsin.fo",url="https://www.fachschaft.informatik.uni-kl.de")
        button1 = Button(label="olat",url="https://olat.vcrp.de/dmz/")
        button2 = Button(label="qis",url="https://qis.verw.uni-kl.de/")
        button3 = Button(label="semestertermine", url="https://rptu.de/studium/im-studium/fristen-und-termine")

        view = View()\
            .add_item(button0)\
            .add_item(button1)\
            .add_item(button2)\
            .add_item(button3)

        message = ""
        if sorted_command_info:  # Check if sorted_command_info is not empty before sending
            for class_ in sorted_command_info.keys():
                message += f"**{class_}**\n"
                for command in sorted_command_info.get(class_).get('commands'):
                    message += f"`{command.get('command')}` {command.get('description')}\n"
            
            message += "\n\n **Nützliche Seiten:**"

            await interaction.response.send_message(message, view=view, ephemeral=True)
        else:
            await interaction.response.send_message("No commands found. \n\n **Nützliche Seiten:**", view=view, ephemeral=True)


async def setup(bot):
    await bot.add_cog(Help(bot))