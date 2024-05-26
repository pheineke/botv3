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
        self.main.start()
        self.cleandata.start()
        self.savestarttime()


    def savestarttime(self):
        day = str((datetime.now().strftime('%Y-%m-%d')))  
        hour =str((datetime.now().strftime('%H:%M')))  
        #'a' Wichtig sonst überschreibt er die Datei
        with open('lock-log.txt', 'a') as file:
            file.write(f"{day},{hour},BOTSTART\n")
        with open('./lib/data/lock/lock-log.json', 'a') as file:  
            json.dump({day:{hour:"BOTSTART"}}, file, indent=4)

    def filter_last_n_days(self, data, n_days):
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
        fslocksite = fslocksite.content.decode('utf8').replace("'", '"')
        fslockjson = json.loads(fslocksite)
        current_date = datetime.now().strftime('%Y-%m-%d')
        current_time = datetime.now().strftime('%H:%M')
        value = fslockjson["opendoor"]
        with open('./lib/data/lock/lock-log.txt', 'a') as file:
            file.write(f"{current_date},{current_time},{value}\n")
        with open('./lib/data/lock/lock-log.json', 'a') as file:    
            json.dump({current_date:{current_time:value}}, file, indent=4)

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

    @app_commands.command(name="opendoor_log", description="[FSINFO] Zeigt pure opendoor log")
    @app_commands.describe(filter="Nach Zeit filtern (kann weggelassen werden)")
    @app_commands.choices(filter=[
        app_commands.Choice(name='Last Five Days', value="0"),
        app_commands.Choice(name='Last Week', value="1")
    ])
    async def get_opendoor_log(self,interaction:discord.Interaction, filter:app_commands.Choice[str]=None):
        if not filter:
            interaction.response.send_message(file=discord.File("./lib/data/lock/lock-log.json"))
        else:
            with open('./lib/data/lock/lock-log.json', 'r') as file:
                data = json.load(file)
                if filter == 0:
                    filtered = self.filter_last_n_days(data=data, days=5)
                elif filter == 1:
                    filtered = self.filter_last_n_days(data=data, days=14)
                    
                temp_file = tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.json')
                json.dump(filtered, temp_file)

                interaction.response.send_message(content="Hier ist der Verlauf:", file=discord.File(temp_file))
                temp_file.close()
                    




    @app_commands.command(name="opendoor_graph", description="[FSINFO] Zeigt opendoor Graph")
    @app_commands.describe(datum0 = "Optional von - YYYY-MM-dd", datum1 = "Optional bis - YYYY-MM-dd")
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