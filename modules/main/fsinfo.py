import os
import tempfile
import discord
from discord import app_commands
from discord.ext import commands, tasks
from discord.ui import Button, View

import requests, json
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta


class Fsinfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.filepath = './lib/data/lock/lock-log.json'
        self.check_if_file()

        self.savestarttime()

        self.main.start()
        self.cleandata.start()

    def check_if_file(self):
        print("checkiffile")
        if not os.path.exists(self.filepath):
            with open(self.filepath, 'w') as file:
                test = {}
                file.write(json.dumps(test, indent=4))

    def savestarttime(self):
        day  = str((datetime.now().strftime('%Y-%m-%d')))
        hour = str((datetime.now().strftime('%H:%M'))) + ":00" 
        data : dict = {}
        with open(self.filepath, 'r') as file:
            data : dict = json.load(file)
            if day in data:
                print("start0")
                data[day][hour] = "start"
                print(data)
            else:
                print("start1")
                data[day] = {}
                data[day][hour] = "start"

        with open(self.filepath, 'w') as file:
            file.write(json.dumps(data, indent=4))


    def filter_last_n_days(self, data: dict, n_days: int):
        current_date = datetime.now().date()
        start_date = current_date - timedelta(days=n_days)

        filtered_data = {}
        for date_str, value_dict in data.items():
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
            if start_date <= date_obj <= current_date:
                filtered_data[date_str] = value_dict

        return filtered_data
        
    @tasks.loop(minutes=1.0)
    async def main(self):
        fslocksite = requests.get("https://www.fachschaft.informatik.uni-kl.de/opendoor.json")
        print(fslocksite)
        fslocksite = fslocksite.content.decode('utf8').replace("'", '"')
        fslockjson = json.loads(fslocksite)

        print(fslockjson, type(fslockjson))

        current_date = str(datetime.now().strftime('%Y-%m-%d'))
        current_time = str(datetime.now().strftime('%H:%M:%S'))
        value = bool(fslockjson['opendoor'])
        print(value, type(value))
        with open(self.filepath, 'r') as file:
            data = json.load(file)
            if current_date in data:
                data[current_date][current_time] = value
            else:
                data[current_date] = {}
                data[current_date][current_time] = value

        with open(self.filepath, 'w') as file:
            file.write(json.dumps(data, indent=4))


    @tasks.loop(minutes=5.0)
    async def cleandata(self):
        with open(self.filepath, 'r') as file:
            data : dict = json.load(file)

        data_ = {}

        for key in data.keys():
            data_[key] = {}

            hour_data : dict = data.get(key)
            hour_data_items : list = list(hour_data.items())
            hour_data_items_len = len(hour_data_items)
            keys : list = list(hour_data.keys())
            #keys_len = len(keys)

            i = 0
            while i < hour_data_items_len:
                key0, value0 = hour_data_items[i]
                if i == 0:
                    #print("First")
                    #Save first data value
                    data_[key][key0] = value0
                
                elif i == hour_data_items_len-1:
                    #print("Last")
                    #Save first data value
                    data_[key][key0] = value0

                else:
                    #Else save the two values if they change
                    key1, value1 = hour_data_items[i+1]

                    if value0 != value1:
                        data_[key][key0] = value0
                        data_[key][key1] = value1
                        
                #input(">") Debug
                i += 1

        with open(self.filepath, 'w') as file:
            file.write(json.dumps(data_, indent=4))
            file.close()

    @app_commands.command(name="opendoor_log", description="Zeigt pure opendoor log")
    @app_commands.describe(filter="Optional filter timestamps")
    @app_commands.choices(filter=[
        app_commands.Choice(name='Last Five Days', value="0"),
        app_commands.Choice(name='Last Week', value="1")
    ])
    async def get_opendoor_log(self,interaction:discord.Interaction, filter:app_commands.Choice[str]=None):
        if not filter:
            await interaction.response.send_message(file=discord.File("./lib/data/lock/lock-log.json"))
        else:
            with open(self.filepath, 'r') as file:
                data = json.load(file)

                fd, path = tempfile.mkstemp()
                try:
                    with os.fdopen(fd, 'w') as tmp:
                        # do stuff with temp file
                        if filter == 0:
                            filtered = self.filter_last_n_days(data=data, days=5)
                            tmp.write(filtered)
                        elif filter == 1:
                            filtered = self.filter_last_n_days(data=data, days=14)
                            tmp.write(filtered)
                        await interaction.followup.send(content="Hier ist der Verlauf:", file=discord.File(path))
                finally:
                    os.remove(path)




    @app_commands.command(name="opendoor_graph", description="Shows opendoor Graph")
    @app_commands.describe(datum0 = "Optional from-date - YYYY-MM-dd", datum1 = "Optional end-date - YYYY-MM-dd")
    async def get_diagram(self, interaction:discord.Interaction, datum0: str=None, datum1:str=None):
        #datum0 = "2024-02-26"
        #datum1 = "2024-02-26"
        # Laden der Daten aus der Datei
        try:
            data = np.loadtxt('lock-log.txt', delimiter=',',dtype=str)

            values = []
            for row in data:
                if row[2] == 'True':
                    values.append(2)
                elif row[2] == 'False':
                    values.append(1)
                else:
                    values.append(0)
            
            dates = [datetime.strptime(row[0] + ' ' + row[1], '%Y-%m-%d %H:%M') for row in data]
            date_values = [[dates[i], values[i]] for i in range(len(dates))]

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
            plot_values = [x[1] for x in filtered_entries]
            print(f"{plot_dates} {plot_values}")
            # Erstellen des Diagramms
            plt.figure(figsize=(20, 3))
            #plt.plot(plot_dates, plot_values, marker='o', linestyle='-', color='b')
            plt.plot([plot_dates[i] for i, v in enumerate(values) if v > 0], 
                [v for v in values if v > 0], 
                marker='o', color='blue', label='Linien')

        # Punkte für Wert 0
            plt.plot([plot_dates[i] for i, v in enumerate(values) if v == 0], 
                [v for v in values if v == 0], 
                marker='o', markersize=8, linestyle='', color='red', label='Punkte')
            plt.xlabel('Date and Time')
            plt.ylabel('Value')
            plt.title(title)
            plt.yticks([0, 1, 2], ['BOTSTART','CLOSED', 'OPEN'])
            plt.grid(True)
            plt.xticks(rotation=45)
            #plt.gca().invert_yaxis()  # Umkehren der y-Achse
            plt.tight_layout()
            plt.savefig("plot-door.png")


            await interaction.response.send_message(file=discord.File('plot-door.png'))

        except Exception as e:
            await interaction.response.send_message(f"No Data\n```{e}```")



async def setup(bot):
    await bot.add_cog(Fsinfo(bot))