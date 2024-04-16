import asyncio
import discord
from discord import app_commands
from discord.ext import commands, tasks
from discord.ui import Button, View

import os, sys

class Loader_prefix(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.is_owner()
    @commands.command(brief="[LOADER_PREF]", aliases=["l"])
    async def load(self, ctx, extension):
        try:
            await self.bot.load_extension(f"modules.{extension}")
            await ctx.message.add_reaction('✅')
        except Exception as e:
            print(e)
            await ctx.message.add_reaction('❌')

    @commands.is_owner()
    @commands.command(brief="[LOADER_PREF]", aliases=["u"])
    async def unload(self, ctx, extension):
    #####unload side
        try:
            await self.bot.unload_extension(f'modules.side.{extension}')
            await ctx.send(f'{extension} cog unloaded.')
            print(f'{extension} unloaded.')
        except:
    #####unload main
            try:
                await self.bot.unload_extension(f'modules.main.{extension}')
                await ctx.send(f'{extension} cog unloaded.')
                print(f'{extension} unloaded.')
            except Exception as e:
                await ctx.send(f'{e}')

        

    @commands.is_owner()
    @commands.command(brief="[LOADER_PREF]", aliases=["r"])
    async def reload(self, ctx, extension):
        await self.bot.unload_extension(f"modules.{extension}")
        await self.bot.load_extension(f"modules.{extension}")


    '''Bot kann heruntergefahren werden.'''
    @commands.command(brief="[LOADER_PREF]")
    @commands.is_owner()
    async def shutdown(self, ctx):
        await ctx.send('Shutting down...')
        print('Shutting down...')

        await self.bot.close()

    @app_commands.command(name="gitpull", description="[LOADER_PREF] Update bot")
    async def gitpull_(self, interaction:discord.Interaction):
        if interaction.user.id in self.bot.owner_ids:
            # Speichere den aktuellen Pfad
            current_path = os.getcwd() + "/"
            os.chdir(f"{os.path.dirname(os.path.abspath(__file__))}"+ "/../../")

            if os.popen('python3 --version').read() == "Python 3.6.8":
                os.system('export PATH=~/.localpython/bin:$PATH')

            await interaction.response.send_message(f"```{os.popen('git pull').read()}```")

            os.chdir(current_path)

            os.execv(sys.executable, ['python3', 'main.py'])

    @commands.command(brief="[LOADER_PREF] Update bot backup")
    @commands.is_owner()
    async def gitpull(self, ctx):
            # Speichere den aktuellen Pfad
            current_path = os.getcwd() + "/"
            if ".wwww" in current_path:
                os.chdir("/home/sih18pev/pythonproj/botv3")
            print(current_path)
            os.chdir(current_path)

            await ctx.send(f"```{os.popen('git pull').read()}```")

            os.chdir(current_path)

            os.execv(sys.executable, ['python3', 'main.py'])

    @commands.command(brief="[LOADER_PREF]")
    @commands.is_owner()
    async def modulespull(self,ctx):
        # Speichere den aktuellen Pfad
        current_path = os.getcwd() + "/"

        print(current_path)
        os.chdir(os.path.dirname(os.path.abspath(__file__)))

        await ctx.send(f"```{os.popen('git pull').read()}```")
        os.chdir(current_path)

        for module in os.listdir("./modules/main/"):
            print(module)


    @commands.command(brief="[LOADER_PREF]", aliases=["f"])
    async def freeze(self, ctx):
        loaded_cogs = [cog for cog in self.bot.cogs.keys()]
        if loaded_cogs:
            await ctx.send(f'Loaded cogs: {", ".join(loaded_cogs)}')
        else:
            await ctx.send('No cogs loaded.')

    @commands.command(brief="[LOADER_PREF]") 
    async def sync(self, ctx):
        synced = await self.bot.tree.sync()
        x = f"Synced {len(synced)} command(s)."
        print(x)
        await ctx.send(x)

async def setup(bot):
    await bot.add_cog(Loader_prefix(bot))