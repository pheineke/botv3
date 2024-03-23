import discord
from discord import app_commands
from discord.ext import commands, tasks
from discord.ui import Button, View

from bs4 import BeautifulSoup
import requests, os, json
from dotenv import load_dotenv

class Monster(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.cookies = self.get_cookies()

    def get_cookies(self):
        cookie_file = open('cookies.json')
        cookies = json.load(cookie_file)
        return cookies

    def get_monsters(self):
        urls = ["https://www.globus.de/produkte/getraenke/soft-drinks/energy-sportgetraenke/5060896625829/energy-drink-lewis-hamilton-zero",
                "https://www.globus.de/produkte/getraenke/soft-drinks/energy-sportgetraenke/5060751219095/energy-drink-watermelon",
                "https://www.globus.de/produkte/getraenke/soft-drinks/energy-sportgetraenke/5060947541153/energy-ultra-rosa-dose",
                "https://www.globus.de/produkte/getraenke/soft-drinks/energy-sportgetraenke/5060751212249/energy-drink-ultra-fiesta",
                "https://www.globus.de/produkte/getraenke/soft-drinks/energy-sportgetraenke/5060335635266/energy-drink-the-doctor",
                "https://www.globus.de/produkte/getraenke/soft-drinks/energy-sportgetraenke/5060337500401/energy-drink-ultra-white",
                "https://www.globus.de/produkte/getraenke/soft-drinks/energy-sportgetraenke/5060947541986/energy-aussie-style-lemonade-dose",
                "https://www.globus.de/produkte/getraenke/soft-drinks/energy-sportgetraenke/5060639126897/energy-drink-ultra-paradise",
                "https://www.globus.de/produkte/getraenke/soft-drinks/energy-sportgetraenke/5060947549555/energy-drink-zero-original",
                "https://www.globus.de/produkte/getraenke/soft-drinks/energy-sportgetraenke/5060751212393/energydrink-monarch",
                "https://www.globus.de/produkte/getraenke/soft-drinks/energy-sportgetraenke/5060337507608/energy-eistee-rehab-peach",
                "https://www.globus.de/produkte/getraenke/soft-drinks/energy-sportgetraenke/5060751216520/energy-drink-nitro",
                "https://www.globus.de/produkte/getraenke/soft-drinks/energy-sportgetraenke/5060896622859/khaotic-juiced",
                "https://www.globus.de/produkte/getraenke/soft-drinks/energy-sportgetraenke/5060335635235/energy-drink-assault",
                "https://www.globus.de/produkte/getraenke/soft-drinks/energy-sportgetraenke/5060517883607/energy-drink-pipeline-punch",
                "https://www.globus.de/produkte/getraenke/soft-drinks/energy-sportgetraenke/5060517888510/energy-drink-juiced-mango-loco",
                "https://www.globus.de/produkte/getraenke/soft-drinks/energy-sportgetraenke/5060335635228/energy-drink-original",
                "https://www.globus.de/produkte/getraenke/soft-drinks/energy-sportgetraenke/5060335635242/energy-drink-absolutely-zero-zuckerfrei",
                ""]
        cookies = self.cookies

            # Führe eine GET-Anfrage auf die Webseite mit den gespeicherten Cookies durch
            
        products = {}
        responses = []

        session = requests.session()

        counter = -1
        for url in urls:
            response_text = session.get(url, cookies=cookies).text
            counter +=1

            responses.append(response_text)
            # with open(f"seitehtml{counter}.html", "w") as file:
            #     file.write(response_text)

        for url in responses:
            #response = requests.get(url, cookies=cookies)
            #requests.delete(url)
            #print(response.status_code)
            html_content = url

            
            # Parse the HTML
            soup = BeautifulSoup(html_content, 'html.parser')

            product_info = {}

            # Produktname
            product_name = soup.find("h1", class_="product--title").get_text(strip=True)
            product_info["Produktname"] = product_name

            # Im Sortiment Information
            im_sortiment = soup.find("span", class_="delivery--text").get_text(strip=True)
            product_info["Im Sortiment"] = im_sortiment

            # Regal Information
            regal_info = soup.find("span", class_="product--shelfinfos-text").get_text(strip=True)
            product_info["Regal"] = regal_info

            # Preis Information
            price_info = soup.find("span", class_="price--content").get_text(strip=True)
            product_info["Preis"] = price_info

            webp_original_url = soup.find("span", class_="image--element")["data-img-webp-original"]
            product_info["Image-WEBP"] = webp_original_url

            products[product_name] = product_info

        return products


    @commands.command()
    async def monster(self, ctx, view=None):
        monster_data = self.get_monsters()

        if view:
            embed = discord.Embed(title=drink_name, color=0x00ff00)
            for key, value in drink_data.items():
                if "Image" not in key:
                    embed.add_field(name=key, value=value, inline=False)

            await ctx.send(embed=embed)
        else:
            embeds = []
            for drink_name, drink_data in monster_data.items():
                embed = discord.Embed(title=drink_name, color=0x00ff00)
                for key, value in drink_data.items():
                    if "Image" in key:
                        embed.set_image(url=value)
                    else:
                        embed.add_field(name=key, value=value, inline=False)
                embeds.append(embed)
            
            await ctx.send(embeds=embeds)


async def setup(client):
    await client.add_cog(Monster(client))