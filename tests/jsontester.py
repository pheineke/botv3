import json
import matplotlib.pyplot as plt
from datetime import datetime


data = {
    "2024-05-01 13:46:47": {
        "Energy Drink, Lewis Hamilton Zero": {
            "Produktname": "Energy Drink, Lewis Hamilton Zero",
            "Im Sortiment": "Im Sortiment in Kaiserslautern",
            "Regal": "Regal: 500 - Meter: 16 - Boden: 02",
            "Preis": "1,49\u00a0\u20ac",
            "Image-WEBP": "https://www.globus.de/produkte/media/image/d7/bc/56/5060896625829_4693709.webp"
        },
        "Energy Drink, Watermelon": {
            "Produktname": "Energy Drink, Watermelon",
            "Im Sortiment": "Im Sortiment in Kaiserslautern",
            "Regal": "Regal: 500 - Meter: 13 - Boden: 03",
            "Preis": "1,49\u00a0\u20ac",
            "Image-WEBP": "https://www.globus.de/produkte/media/image/af/01/e1/5060751219095_4272666.webp"
        },
        "Energy Ultra Rosa Dose": {
            "Produktname": "Energy Ultra Rosa Dose",
            "Im Sortiment": "Im Sortiment in Kaiserslautern",
            "Regal": "Regal: 500 - Meter: 15 - Boden: 01",
            "Preis": "1,49\u00a0\u20ac",
            "Image-WEBP": "https://www.globus.de/produkte/media/image/b4/bd/c9/5060947541153_4693711.webp"
        },
        "Energy Drink, Ultra Fiesta": {
            "Produktname": "Energy Drink, Ultra Fiesta",
            "Im Sortiment": "Im Sortiment in Kaiserslautern",
            "Regal": "Regal: 500 - Meter: 13 - Boden: 05",
            "Preis": "1,49\u00a0\u20ac",
            "Image-WEBP": "https://www.globus.de/produkte/media/image/cc/65/eb/5060751212249_3961391.webp"
        },
        "Energy Drink, The Doctor": {
            "Produktname": "Energy Drink, The Doctor",
            "Im Sortiment": "Im Sortiment in Kaiserslautern",
            "Regal": "Regal: 500 - Meter: 16 - Boden: 01",
            "Preis": "1,49\u00a0\u20ac",
            "Image-WEBP": "https://www.globus.de/produkte/media/image/c2/2b/84/5060335635266_20000729133.webp"
        },
        "Energy Drink, Ultra White": {
            "Produktname": "Energy Drink, Ultra White",
            "Im Sortiment": "Im Sortiment in Kaiserslautern",
            "Regal": "Regal: 500 - Meter: 15 - Boden: 03",
            "Preis": "1,49\u00a0\u20ac",
            "Image-WEBP": "https://www.globus.de/produkte/media/image/f4/3a/22/5060337500401_4272847.webp"
        },
        "Energy Aussie Style Lemonade Dose": {
            "Produktname": "Energy Aussie Style Lemonade Dose",
            "Im Sortiment": "Im Sortiment in Kaiserslautern",
            "Regal": "Regal: 500 - Meter: 15 - Boden: 01",
            "Preis": "1,49\u00a0\u20ac",
            "Image-WEBP": "https://www.globus.de/produkte/media/image/1a/45/78/5060947541986_4272679.webp"
        },
        "Energy-Drink Ultra Paradise": {
            "Produktname": "Energy-Drink Ultra Paradise",
            "Im Sortiment": "Im Sortiment in Kaiserslautern",
            "Regal": "Regal: 500 - Meter: 13 - Boden: 04",
            "Preis": "1,49\u00a0\u20ac",
            "Image-WEBP": "https://www.globus.de/produkte/media/image/e6/11/e4/5060639126897_3961415.webp"
        },
        "Energy Drink, Zero Original": {
            "Produktname": "Energy Drink, Zero Original",
            "Im Sortiment": "Im Sortiment in Kaiserslautern",
            "Regal": "Regal: 500 - Meter: 13 - Boden: 03",
            "Preis": "1,49\u00a0\u20ac",
            "Image-WEBP": "https://www.globus.de/produkte/media/image/7f/19/3b/5060947549555_4692242.webp"
        },
        "Energydrink, Monarch": {
            "Produktname": "Energydrink, Monarch",
            "Im Sortiment": "Im Sortiment in Kaiserslautern",
            "Regal": "Regal: 500 - Meter: 13 - Boden: 02",
            "Preis": "1,49\u00a0\u20ac",
            "Image-WEBP": "https://www.globus.de/produkte/media/image/7f/e9/f0/5060751212393_4693416.webp"
        },
        "Energy Eistee, Rehab Peach": {
            "Produktname": "Energy Eistee, Rehab Peach",
            "Im Sortiment": "Im Sortiment in Kaiserslautern",
            "Regal": "Regal: 500 - Meter: 13 - Boden: 04",
            "Preis": "1,49\u00a0\u20ac",
            "Image-WEBP": "https://www.globus.de/produkte/media/image/db/f3/3a/5060337507608_1473773.webp"
        },
        "Energy Drink, Nitro": {
            "Produktname": "Energy Drink, Nitro",
            "Im Sortiment": "Im Sortiment in Kaiserslautern",
            "Regal": "Regal: 400 - Meter: 13 - Boden: 02",
            "Preis": "1,49\u00a0\u20ac",
            "Image-WEBP": "https://www.globus.de/produkte/media/image/cb/ab/e1/5060751216520_3556040.webp"
        },
        "Khaotic, Juiced": {
            "Produktname": "Khaotic, Juiced",
            "Im Sortiment": "Im Sortiment in Kaiserslautern",
            "Regal": "Regal: 400 - Meter: 13 - Boden: 03",
            "Preis": "1,49\u00a0\u20ac",
            "Image-WEBP": "https://www.globus.de/produkte/media/image/e2/12/cc/5060896622859_4272670.webp"
        },
        "Energy Drink, Assault": {
            "Produktname": "Energy Drink, Assault",
            "Im Sortiment": "Im Sortiment in Kaiserslautern",
            "Regal": "Regal: 500 - Meter: 16 - Boden: 02",
            "Preis": "1,49\u00a0\u20ac",
            "Image-WEBP": "https://www.globus.de/produkte/media/image/10/49/1d/5060335635235_20000799426.webp"
        },
        "Energy Drink, Pipeline Punch": {
            "Produktname": "Energy Drink, Pipeline Punch",
            "Im Sortiment": "Im Sortiment in Kaiserslautern",
            "Regal": "Regal: 500 - Meter: 13 - Boden: 01",
            "Preis": "1,49\u00a0\u20ac",
            "Image-WEBP": "https://www.globus.de/produkte/media/image/71/5f/1a/5060517883607_1513932.webp"
        },
        "Energy Drink, Juiced Mango Loco": {
            "Produktname": "Energy Drink, Juiced Mango Loco",
            "Im Sortiment": "Im Sortiment in Kaiserslautern",
            "Regal": "Regal: 500 - Meter: 13 - Boden: 02",
            "Preis": "1,49\u00a0\u20ac",
            "Image-WEBP": "https://www.globus.de/produkte/media/image/d1/bf/3f/5060517888510_4693432.webp"
        },
        "Energy Drink, Original": {
            "Produktname": "Energy Drink, Original",
            "Im Sortiment": "Im Sortiment in Kaiserslautern",
            "Regal": "Regal: 500 - Meter: 16 - Boden: 03",
            "Preis": "1,49\u00a0\u20ac",
            "Image-WEBP": "https://www.globus.de/produkte/media/image/17/dc/b1/5060335635228_20000576050.webp"
        },
        "Energy Drink, Absolutely Zero, zuckerfrei": {
            "Produktname": "Energy Drink, Absolutely Zero, zuckerfrei",
            "Im Sortiment": "Im Sortiment in Kaiserslautern",
            "Regal": "Regal: 500 - Meter: 13 - Boden: 03",
            "Preis": "1,49\u00a0\u20ac",
            "Image-WEBP": "https://www.globus.de/produkte/media/image/d4/43/ff/5060335635242_4692240.webp"
        }
    }
}

import json
import matplotlib.pyplot as plt
from datetime import datetime

def plot_preise():

    for timestamp, produkte in data.items():
        energy_drinks = {}
        for produkt, daten in produkte.items():
            if 'Energy Drink' in produkt:
                preis = daten.get('Preis')
                energy_drink_name = produkt.split(',')[0]  # Nur der Energy Drink Name ohne spezifische Sorte
                if energy_drink_name not in energy_drinks:
                    energy_drinks[energy_drink_name] = []
                energy_drinks[energy_drink_name].append((timestamp, float(preis[:-2].replace(",", "."))))

        for energy_drink, preisverlauf in energy_drinks.items():
            preisverlauf.sort(key=lambda x: datetime.strptime(x[0], "%Y-%m-%d %H:%M:%S"))  # Sortieren nach Zeitstempel

            timestamps = [entry[0] for entry in preisverlauf]
            preise = [entry[1] for entry in preisverlauf]

            plt.figure(figsize=(10, 6))
            plt.plot(timestamps, preise, marker='o', linestyle='-')
            plt.xlabel('Zeitstempel')
            plt.ylabel('Preis (€)')
            plt.title(f'Preisverlauf für {energy_drink}')
            plt.xticks(rotation=45)
            plt.tight_layout()

            plt.show()



plot_preise()
