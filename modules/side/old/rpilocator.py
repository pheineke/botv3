import asyncio
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pytz

import discord
from discord.ext import commands


class Rpilocator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.background_task = self.bot.loop.create_task(self.rpistock_background_loop())

    @commands.Cog.listener()
    async def rpistock_background_loop(self):
        await self.bot.wait_until_ready()
        

        CHANNEL_ID = 1070443662695223297
        channel = self.bot.get_channel(CHANNEL_ID)
        await channel.send("RPILocator Module loaded.")
        
        while not self.bot.is_closed():
            req = requests.get("https://rpilocator.com/feed/")
            if req.status_code == 200:
                reqtext = req.text

                soup = BeautifulSoup(reqtext, 'xml')
                textlist = [item.text for item in soup.find_all(['title', 'pubDate'])]
                combined_list = [[textlist[i], textlist[i+1]] for i in range(0, len(textlist), 2) if "rpilocator.com" not in textlist[i+1] and "DE" in textlist[i]]

                gmt = pytz.timezone('GMT')
                current_time_gmt = datetime.now(gmt).strftime("%a, %d %b %Y %H:%M:%S GMT")
                time_now = datetime.strptime(current_time_gmt, "%a, %d %b %Y %H:%M:%S GMT")

                status = False
                for x in combined_list:
                    item = x
                    time_of_feed = datetime.strptime(x[1], "%a, %d %b %Y %H:%M:%S GMT")
                    time_difference = time_now - time_of_feed
                    if int(time_difference.total_seconds()) <= 7200:
                        status1 = True
                    else:
                        status1 = False
                    if status != status1 and status1 is True:
                        channel_id = CHANNEL_ID  # Ersetze durch die gewünschte Kanal-ID
                        
                        await channel.send(f"{item}")
                        print("UPDATE: ", item, end="\r")
                        status = status1
                    print(req.status_code, item, time_now, end="\r")
                await asyncio.sleep(60)

async def setup(bot):
    await bot.add_cog(Rpilocator(bot))