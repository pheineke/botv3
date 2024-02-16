from discord.ext import commands

import modules.main.mensa.database as database

class Mensa(commands.Cog):
    def __init__(self,bot) -> None:
        self.bot = bot
        self.user_time_db = database.Manage_database("users.db")

    @commands.command()
    async def mensatime(self, ctx, equal=None, arg=None):
        username = ctx.author.name
        if ctx.prefix == "my.":
            if arg is None and equal is None:
                try:
                    response = f"{ctx.author.mention} Deine Mensazeit ist: {self.user_time_db.get_user_times(username)[0]}".replace("'","")
                    await ctx.send(response)
                    
                except:
                    await ctx.send("Keine Usertime")
            else:
                if equal == "=":
                    if arg in ["none", "NONE", "false", "False"]:
                        try:
                            self.user_time_db.remove_user(username)
                            await ctx.message.add_reaction('✅')
                        except:
                            await ctx.send("Kein User eingetragen.")
                    else:
                        try:
                            arg = self.user_time_db.striptime(arg)
                            if self.user_time_db.validate_time_format(arg):
                                self.user_time_db.save_user_time(username, arg)
                                await ctx.message.add_reaction('✅')
                        except Exception as e:
                            print(e)
                            await ctx.send("Kein gültiger Befehl")

                        
        if ctx.prefix == "xs.":
            await ctx.send(f"{ctx.author.mention} Folgende Mensazeiten sind eingetragen:\n```\n{self.user_time_db.get_all_users_with_times()}\n```")
        

async def setup(bot):
    await bot.add_cog(Mensa(bot))
