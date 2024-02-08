import discord
from discord.ext import commands

from datetime import datetime


class Hallo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def check_for_webhook(self, ctx, hookname):
        # Überprüfe, ob in diesem Channel bereits ein Webhook existiert
        existing_webhooks = await ctx.channel.webhooks()
        webhook = None

        for existing in existing_webhooks:
            if existing.name == hookname:
                webhook = existing
                print("Es exisitiert ein Webhook")
                break

        # Wenn kein Webhook gefunden wurde, erstelle einen neuen
        if webhook is None:
            webhook = await ctx.channel.create_webhook(name=hookname)
            print("Es exisitiert kein Webhook -> Wurde ein Neuer erstellt.")
        return webhook
    

    @commands.Cog.listener()
    async def on_message(self, message):
        
        def get_time_period(current_time):
            hour = current_time.hour
            if 6 <= hour < 12:
                return "n Morgen"
            elif 12 <= hour < 18:
                return "n Mittag"
            elif 18 <= hour < 24:
                return "Abend"
            else:
                return "n Nacht"
            
        if message.content == "Guten _" and not message.author.bot:
            user = message.author
            current_time = datetime.now()

            hookname = self.bot.user.name
            webhook = await self.check_for_webhook(message, hookname)

            returncontent = f"Gute{get_time_period(current_time)}"
            await webhook.send(content=returncontent, avatar_url=user.avatar, username=user.name)
            



async def setup(bot):
    await bot.add_cog(Hallo(bot))
