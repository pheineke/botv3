from discord.ext import commands, tasks
from datetime import datetime

import modules.main.mensa.database as database

class Mensa(commands.Cog):
    def __init__(self,bot) -> None:
        self.bot = bot
        self.user_time_db = database.Manage_database("users.db")
        self.cyclereset.start()

    time = datetime(year= datetime.now().year, hour=15, minute=00)

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
                        print("hier")
                        try:
                            self.user_time_db.remove_user(username)
                            await ctx.message.add_reaction('✅')
                        except:
                            await ctx.send("Kein User eingetragen.")
                    elif arg in ["const", "constant"]:
                        try:
                            self.user_time_db.set_user_time_constant(username)
                            await ctx.message.add_reaction('✅')
                        except:
                            await ctx.send("Kein User eingetragen")
                    elif arg in ["nconst", "nconstant", "notconstant"]:
                        try:
                            self.user_time_db.set_user_time_nconstant(username)
                            await ctx.message.add_reaction('✅')
                        except:
                            await ctx.send("Kein User eingetragen")
                    elif arg in ["jetzt", "now", "rn"]:
                        try:
                            now = datetime.now().strftime("%H:%M")
                            self.user_time_db.save_user_time(username, str(now))
                            await ctx.message.add_reaction('✅')
                        except:
                            await ctx.send("Kein gültiger Befehl")
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
    
    @tasks.loop(time=time)
    def cyclereset(self):
        self.user_time_db.remove_nconstants()

        
async def setup(bot):
    await bot.add_cog(Mensa(bot))
