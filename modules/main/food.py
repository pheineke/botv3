import discord
from discord.ext import commands
import requests
from datetime import date as datum

class MensaAPI(commands.Cog):
    def __init__(self, client):
        self.client = client

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

    @commands.Cog.listener("on_message")
    async def fowd(self, message):
        if message.author.bot:
            return
        if message.content.lower() == "my.food":
            await MensaAPI.mensa(self, message.channel)
        elif "my.mensatime = " in message.content.lower():
            await message.add_reaction(':plus1:1171776509195845652')

    @commands.Cog.listener("on_reaction_add")
    async def on_reaction_add(self,reaction, user):
        if user.bot:
            return
        if str(reaction.emoji) == "<:plus1:1171776509195845652>":
            hookname = self.client.user.name
            webhook = await self.check_for_webhook(reaction.message, hookname)
            await webhook.send(content=reaction.message.content, avatar_url=user.avatar, username=user.name)
        
        

    @commands.cooldown(1, 20, commands.BucketType.user)
    @commands.command(alias = "Mensa",brief="Zeigt zukünftige Mahlzeiten in der Mensa an")
    async def mensa(self, ctx, pics = 0, date: str ="0"):
        base_url = "https://www.mensa-kl.de/api.php"
        params = {"format": "json", "date": date}

        try:
            response = requests.get(f"{base_url}", params=params)
            response.raise_for_status()
            data = response.json()

            if data:
                if pics == 0:
                    if date == "all":
                        titel = f"Alle nächsten Ausgaben"
                    else:
                        heute = data[0].get("date","Alle Tage")

                        titel = f"Ausgabe am {heute}"
                    
                    embed = discord.Embed(title=titel, color=0x0080FF)  # Du kannst die Farbe anpassen
                    for meal in data:
                        title = meal.get("title", "N/A")
                        price = meal.get("price", "N/A")
                        image_url = meal.get("image", "")
                        ausgabe = meal.get("loc", "")
                        formatted_meal = f"**{title}** - {price}€"
                        embed.add_field(name=f"Ausgabe {ausgabe}", value=formatted_meal, inline=False)
                    embed.set_footer(text="Daten von Mensa-kl.de")
                    await ctx.send(embed=embed)
                elif date == "all":
                    await ctx.send(f"Ich werde dir nicht alle Gerichte mit Bildern geben, das wären {len(data)} Nachrichten!\n Mach lieber +mensa 0 all")
                else:
                    for meal in data:
                        title = meal.get("title_with_additives", "N/A")
                        price = meal.get("price", "N/A")
                        image_url = meal.get("image", "")
                        icon = meal.get("icon", "")
                        ausgabe = meal.get("loc", "Weiß nicht, welche Ausgabe")
                        formatted_meal = f"**{title}** - {price}€"

                        embed = discord.Embed(title=f"Ausgabe {ausgabe}", description = formatted_meal, color=0x0080FF)
                        if image_url:
                            embed.set_image(url=f"https://www.mensa-kl.de/mimg/{image_url}")
                        if icon:
                            embed.set_thumbnail(url=f"https://www.mensa-kl.de/img/{icon}.png")
                        embed.set_footer(text="Daten von Mensa-kl.de")
                        await ctx.send(embed=embed)

            else:
                await ctx.send("Es wurden keine Mahlzeiten gefunden.")

        except Exception as e:
            await ctx.send(f"Fehler beim Abrufen der Mahlzeiten: {str(e)}")

async def setup(client):
    await client.add_cog(MensaAPI(client))