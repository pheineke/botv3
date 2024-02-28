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

    @tasks.loop(minutes=1.0)
    async def main(self):
        fslocksite = requests.get("https://www.fachschaft.informatik.uni-kl.de/opendoor.json")
        fslocksite = fslocksite.content.decode('utf8').replace("'", '"')
        fslockjson = json.loads(fslocksite)
        current_date = datetime.now().strftime('%Y-%m-%d')
        current_time = datetime.now().strftime('%H:%M')
        value = fslockjson["opendoor"]
        with open('lock-log.txt', 'a') as file:
            file.write(f"{current_date},{current_time},{value}\n")

    @tasks.loop(minutes=5.0)
    async def cleandata(self):
        def clean_data(file_path):
            with open(file_path, 'r') as file:
                lines = file.readlines()

            cleaned_lines = []
            clean0 = []
            for line in lines:
                lineval = line.strip().split(',')[2]
                cleaned_lines.append(lineval)
                
            def find_equal_intervals(lst):
                equal_intervals = []
                start_index = 0
                current_element = None
                
                for i, element in enumerate(lst):
                    if element != current_element:
                        if i > start_index:
                            equal_intervals.append((start_index, i - 1, current_element))
                        start_index = i
                        current_element = element

                # Füge das letzte Intervall hinzu, falls es gleich ist
                if lst and lst[-1] == current_element:
                    equal_intervals.append((start_index, len(lst) - 1, current_element))

                return equal_intervals
            intervals = find_equal_intervals(cleaned_lines)

            for index0, index1, val in intervals:
                if index0 != index1:
                    clean0.append(lines[index0])
                    clean0.append(lines[index1])
                else:
                    clean0.append(lines[index0])

            with open(file_path, 'w') as file:
                for elem in clean0:
                    file.write(f'{elem}')

        clean_data('lock-log.txt')

    @commands.command()
    async def get_diagram(self, ctx, datum0=None, datum1=None):
        #datum0 = "2024-02-26"
        #datum1 = "2024-02-26"
        # Laden der Daten aus der Datei
        try:
            data = np.loadtxt('lock-log.txt', delimiter=',',dtype=str)

            values = [row[2] == 'True' for row in data]
            dates = [datetime.strptime(row[0] + ' ' + row[1], '%Y-%m-%d %H:%M') for row in data]
            date_values = [[dates[i], values[i]] for i in range(len(dates))]

            print(f"{datum0}{datum1}")
            if datum0 and (not datum1):
                filtered_entries = [entry for entry in date_values if datum0 in str(entry[0])]
                title = f'FS-Info Öffnungsverlauf von {datum0}'
            elif datum0 and datum1:
                filtered_entries = [entry for entry in date_values if datum0 in str(entry[0]) or datum1 in str(entry[0])]
                title = f'FS-Info Öffnungsverlauf von {datum0} bis {datum1}'
            else:
                filtered_entries = date_values
                title = f'FS-Info Öffnungsverlauf gesamt'


            plot_dates = [str(x[0]) for x in filtered_entries]
            plot_values = [str(x[1]) for x in filtered_entries]
            # Erstellen des Diagramms
            plt.figure(figsize=(20, 3))
            plt.plot(plot_dates, plot_values, marker='o', linestyle='-', color='b')
            plt.xlabel('Date and Time')
            plt.ylabel('Value')
            plt.title(title)
            plt.yticks([0, 1], ['OPEN', 'CLOSED'])
            plt.grid(True)
            plt.xticks(rotation=45)
            plt.gca().invert_yaxis()  # Umkehren der y-Achse
            plt.tight_layout()
            plt.savefig("plot-door.png")


            await ctx.send(file=discord.File('plot-door.png'))

        except Exception as e:
            await ctx.send(f"No Data\n```{e}```")



async def setup(bot):
    await bot.add_cog(Fslock(bot))