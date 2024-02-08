import discord
from discord.ext import commands

class Schulden(commands.Cog):
    def __init__(self, bot):
         self.bot = bot
         self.schulden = {"user0": {"user1": 0.01}}

    @commands.command()
    async def getschulden(self, user0, user1):
        return self.schulden[user0][user1]

    @commands.command()
    async def addschulden(self, ctx, user1, betrag):
        user0 = ctx.author.name

        if user1 in ctx.guild.members:
            try:
                betrag = float(betrag)
                "{:.2f}".format(betrag)


                try:
                    betrag0 = self.schulden[user0][user1] 
                    self.schulden[user0][user1] += betrag
                    betrag1 = self.schulden[user0][user1]
                except:
                    self.schulden[user0] = {f"{user1}":betrag}
                    betrag0 = 0
                    betrag1 = betrag
            except ValueError:
                "fail"
        

        return f"Alter Betrag: {betrag0} Neuer Betrag: {betrag1}"

    print(addschulden("user1","user0", "1.10"))


    @commands.Cog.listener("on_reaction_add")
    async def on_reaction_add(self,reaction, user):
        if user.bot:
            return
        if str(reaction.emoji) == "✅":
            


###Funktion: Log schreiben um streitigkeiten zu vermeiden




import json

class jsh():
    def openjsonfile(type, jsonfile):
            with open(jsonfile, 'r') as f:
                    data = json.load(f)
                    return data[type]
            
    def savefile(data, type, file):
            with open(file, 'r') as f:
                    jsondata = json.load(f)
                    jsondata[type] = data
                    with open(file, 'w') as f:
                            json.dump(jsondata,f)