import re
import discord
from discord import app_commands
from discord.ext import commands

from datetime import datetime, timedelta
import requests,os
from dotenv import load_dotenv
from bs4 import BeautifulSoup as bs 
import pprint



class Dominascrp(commands.Cog):
    def __init__(self, bot:commands.Bot) -> None:
        self.bot = bot
        load_dotenv()

    def scraper(self, apartment='B-112'):
        login_url = "https://domina.wohnheim.uni-kl.de/login.pl"
        search_url = "https://domina.wohnheim.uni-kl.de/searchhost.pl"

        #ACHTUNG PASSWORT
        payload = { 
            "username": os.getenv('DOMINA_username'), 
            "password": os.getenv('DOMINA_password')
        }
        search = {
            "searchtext":f"{apartment}",
            "action":"search"
        }

        s = requests.session() 
        response = s.post(login_url, data=payload)
        if response.status_code == 200:
            response2 = s.post(search_url, search)
            if response2.status_code == 200:
                soup = bs(response2.text, 'html.parser').find_all('table', class_='greyBox')

                # Find both greyBox tables (assuming they are unique on the page)
                grey_boxes = soup

                # Create an empty dictionary to store the scraped data
                overview = {}

                # Iterate through each greyBox table
                for i, grey_box in enumerate(grey_boxes):
                    # Create a sub-dictionary for each table's data
                    table_data = {}

                    # Find all rows (<tr>) within the current greyBox
                    rows = grey_box.find_all('tr')

                    # Iterate through each row
                    for row in rows:
                        # Extract key-value pairs from each row's cells (<td>)
                        key, value = row.find_all('td', bgcolor="#dddddd")[0].text, row.find_all('td', bgcolor="#dddddd")[1].text
                        table_data[key] = value

                    # Add the sub-dictionary for the current greyBox to the main data dictionary
                    overview[f"greyBox_{i+1}"] = table_data  # Use f-string for clear numbering

                
                
                # Parse the HTML content
                soup = bs(response2.text, 'html.parser')

                # Find the table element
                table = soup.find('p')
                content = [x.split('\n') for x in table.text.strip().replace('\n\n','\n').split('\n\n')]
                tabelle = {}
                for elem in content:
                    key,value,value2 = elem[0],elem[1],elem[2]
                    tblrow = {}
                    tblrow[value] = value2
                    tabelle[key] = tblrow

                tabelle = dict(sorted(tabelle.items(), key=lambda x: datetime.strptime(x[0], '%d.%m.%Y %H:%M'), reverse=True))

        return overview, tabelle


    
    
    @app_commands.command(name="wohnheimsperre", description="Zeig Sperrstatus eines Apartments")
    async def wohnheimsperre(self, interaction:discord.Interaction, apartment:str, days:str=None):
        def check_format(string):
                pattern = r'^[A-Z]-\d{3}$'
                if re.match(pattern, string):
                    getint = string.split('-')
                    return (0 < int(getint[1]) < 1000)
                else:
                    return False
                
        def filter_last_x_days(x, data):
            returndata = ""
            end_date = datetime.now()  # Aktuelles Datum
            start_date = end_date - timedelta(days=x)  # Berechne Startdatum
            for key, value in data.items():
                date_obj = datetime.strptime(key, '%d.%m.%Y %H:%M')
                if start_date <= date_obj <= end_date:
                    temp_dict = {}
                    temp_dict[key] = value
                    returndata += f"{temp_dict}\n"

            return returndata

        if check_format(apartment):
            try:
                overview,tabelle = self.scraper(apartment=apartment)
            except:
                interaction.response.send_message("Either false Apart. or Website not reachable", ephemeral=True)

            if days:
                tabelle_new = filter_last_x_days(days, tabelle)
            else:
                tabelle_new = tabelle
                
            embed=discord.Embed(title="APART")
            embed.add_field(name="Overview:", value=pprint.pformat(overview), inline=False)
            embed.add_field(name="TABLE", value=tabelle_new, inline=False)
                        
            interaction.response.send_message(embed=embed)
        else:
            interaction.response.send_message("Wrong Apart. Format", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Dominascrp(bot))

