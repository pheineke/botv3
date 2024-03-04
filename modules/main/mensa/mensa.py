import json
from discord.ext import commands, tasks
from datetime import datetime

import modules.main.mensa.database as database

class Mensa(commands.Cog):
    def __init__(self,bot) -> None:
        self.bot = bot
        self.user_time_db = database.Manage_database("users.db")
        self.cyclereset.start()

    def db_controller(self, ctxprefix, authormention, authorname, arg=None, equal=None):
        if ctxprefix == "my.":
            if arg is None and equal is None:
                try:
                    response = f"{authormention} Deine Mensazeit ist: {self.user_time_db.get_user_times(authorname)[0]}".replace("'","")
                    return ("1", response) #1, response
                    
                except:
                    return ("3", "Keine Usertime") #3
            else:
                if equal == "=":
                    if arg in ["none", "NONE", "false", "False"]:
                        try:
                            self.user_time_db.remove_user(authorname)
                            return ("2", None) #2
                        except:
                            return ("3", "Kein User eingetragen.") #3
                    elif arg in ["const", "constant"]:
                        try:
                            self.user_time_db.set_user_time_constant(authorname)
                            return ("2", None) #2
                        except:
                            return ("3", "Kein User eingetragen.") #3
                    elif arg in ["nconst", "nconstant", "notconstant"]:
                        try:
                            self.user_time_db.set_user_time_nconstant(authorname)
                            return ("2", None) #2
                        except:
                            return ("3", "Kein User eingetragen.") #3
                    elif arg in ["jetzt", "now", "rn"]:
                        try:
                            now = datetime.now().strftime("%H:%M")
                            self.user_time_db.save_user_time(authorname, str(now))
                            return ("2", None) #2
                        except:
                            return ("0", "Kein gültiger Befehl") #0
                    else:
                        try:
                            arg = self.user_time_db.striptime(arg)
                            if self.user_time_db.validate_time_format(arg):
                                self.user_time_db.save_user_time(authorname, arg)
                                return ("2", None) #2
                        except Exception as e:
                            print(e)
                            return ("0", "Kein gültiger Befehl") #0

                        
        if ctxprefix == "xs.":
            x = self.user_time_db.get_all_users_with_times()
            a = {key: x[key] for key in sorted(x)}
            y = ""
            for key,value in a.items():
                y += f"{key:15} |  {value}\n".replace("'","").replace("[","").replace("]","")
            return ("4", y) #4

    @commands.command()
    async def mensatime(self, ctx, equal=None, arg=None):
        authorname = ctx.author.name
        authormention = ctx.author.mention
        ctxprefix = ctx.prefix

        db_control, response = self.db_controller()

        match db_control, response:
            case "0", response:
                await ctx.send(response)
            case "1", response:
                await ctx.send(response)
            case "2", None:
                await ctx.message.add_reaction('✅')
            case "3", None:
                await ctx.send("Keine Usertime")
            case "4", response:
                await ctx.send(f"{authormention} Folgende Mensazeiten sind eingetragen:\n```\n{response}\n```")
        

        
    
    @commands.Cog.listener("on_reaction_add")
    async def on_reaction_add(self,reaction, user):
        if user.bot:
            return
        if str(reaction.emoji) == "<:plus1:1171776509195845652>":
            hookname = self.client.user.name
            webhook = await self.check_for_webhook(reaction.message, hookname)
            await webhook.send(content=reaction.message.content, avatar_url=user.avatar, username=user.name)

    @tasks.loop(minutes=15.0)
    async def cyclereset(self):
        if datetime.now().strftime("%H") == "15":
            self.user_time_db.remove_nconstants()

    @commands.is_owner()
    @commands.command(brief="reset-db")
    async def reset(self,ctx):
        self.user_time_db.remove_nconstants()
        
async def setup(bot):
    await bot.add_cog(Mensa(bot))
