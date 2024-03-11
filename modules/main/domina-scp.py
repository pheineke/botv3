import requests,os
from dotenv import load_dotenv
from bs4 import BeautifulSoup as bs 
import pprint

load_dotenv()



def scraper(apartment='B-112'):
    login_url = "https://domina.wohnheim.uni-kl.de/login.pl"
    search_url = "https://domina.wohnheim.uni-kl.de/searchhost.pl"


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
    response2 = s.post(search_url, search)


    soup0 = bs(response2.text, "html.parser")

    # Die Tabelle abrufen
    table = soup0.find('table', class_='greyBox')

    # Ein leeres Dictionary erstellen, um die Daten zu speichern
    overview0 = {}

    # Alle Zeilen in der Tabelle finden
    rows = table.find_all('tr')

    # Durch jede Zeile iterieren und Daten extrahieren
    for row in rows:
        # Jede Zeile besteht aus zwei Zellen: Zelle 1 (index 0) enthält den Schlüssel und Zelle 2 (index 1) enthält den Wert
        cells = row.find_all('td')
        key = cells[0].text.strip()
        value = cells[1].text.strip()
        overview0[key] = value

    soup1 = bs(response2.text, 'html.parser')

    # Die Tabelle finden
    table = soup1.find('table', class_='greyBox')

    # Ein leeres Dictionary erstellen, um die Daten zu speichern
    overview1 = {}

    # Alle Zeilen in der Tabelle finden
    rows = table.find_all('tr')

    # Durch jede Zeile iterieren und Daten extrahieren
    for row in rows:
        # Jede Zeile besteht aus zwei Zellen: Zelle 1 (index 0) enthält den Schlüssel und Zelle 2 (index 1) enthält den Wert
        cells = row.find_all('td')
        key = cells[0].text.strip()
        value = cells[1].text.strip()
        overview1[key] = value


    pprint.pprint(overview0)
    pprint.pprint(overview1)

scraper()