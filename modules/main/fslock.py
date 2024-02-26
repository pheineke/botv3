from datetime import datetime
import os
import time
import requests
import json
import discord
from discord.ext import commands, tasks
import matplotlib.pyplot as plt
import numpy as np


class Fslock(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.main.start()

    @tasks.loop(minutes=5.0)
    async def main(self):
        fslocksite = requests.get("https://www.fachschaft.informatik.uni-kl.de/opendoor.json")
        fslocksite = fslocksite.content.decode('utf8').replace("'", '"')
        fslockjson = json.loads(fslocksite)
        current_date = datetime.now().strftime('%Y-%m-%d')
        current_time = datetime.now().strftime('%H:%M')
        value = fslockjson["opendoor"]
        with open('data.txt', 'a') as file:
            file.write(f"{current_date},{current_time},{value}\n")

    @commands.command()
    async def get_diagram(self, ctx, datum0=None, datum1=None):
        #datum0 = "2024-02-26"
        #datum1 = "2024-02-26"
        # Laden der Daten aus der Datei
        data = np.loadtxt('data.txt', delimiter=',',dtype=str)

        values = [row[2] != 'True' for row in data]
        dates = [datetime.strptime(row[0] + ' ' + row[1], '%Y-%m-%d %H:%M') for row in data]
        date_values = [[dates[i], values[i]] for i in range(len(dates))]

        if not(datum0 and datum1):
            filtered_entries = date_values
        elif datum0 and not datum1:
            filtered_entries = [entry for entry in date_values if datum0 in str(entry[0])]
        elif datum0 and datum1:
            filtered_entries = [entry for entry in date_values if datum0 in str(entry[0]) or datum1 in str(entry[0])]
        else:
            filtered_entries = date_values


        plot_dates = [str(x[0]) for x in filtered_entries]
        plot_values = [str(x[1]) for x in filtered_entries]
        # Erstellen des Diagramms
        plt.figure(figsize=(20, 3))
        plt.plot(plot_dates, plot_values, marker='o', linestyle='-', color='b')
        plt.xlabel('Date and Time')
        plt.ylabel('Value')
        plt.title('FS-Info Öffnungsverlauf')
        plt.yticks([0, 1], ['CLOSED', 'OPEN'])
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig("plot-door.png")

        await ctx.send(file=discord.File('plot-door.png'))




async def setup(bot):
    await bot.add_cog(Fslock(bot))
