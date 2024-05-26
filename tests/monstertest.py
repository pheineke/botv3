import json
import requests
from bs4 import BeautifulSoup

class MonsterTest():
    def __init__(self) -> None:
        self.cookies = self.get_cookies()

    def get_cookies(self):
            cookie_file = open('./lib/data/monster/cookies.json')
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
                "https://www.globus.de/produkte/getraenke/soft-drinks/energy-sportgetraenke/5060335635242/energy-drink-absolutely-zero-zuckerfrei"]
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
            if "Energy Drink, " in product_name:
                product_name.replace("Energy Drink, ", "")
            if "Energy " in product_name:
                product_name.replace("Energy ", "")
            if "Energy-Drink " in product_name:
                product_name.replace("Energy-Drink ", "")
            if "Energydrink " in product_name:
                product_name.replace("Energydrink ", "")
                
            product_info["Produktname"] = product_name

            # Im Sortiment Information
            im_sortiment = soup.find("span", class_="delivery--text").get_text(strip=True)
            product_info["Im Sortiment"] = im_sortiment

            # Regal Information
            regalsoup = soup.find("span", class_="product--shelfinfos-text")
            if regalsoup:
                regal_info = regalsoup.get_text(strip=True)
            else: regal_info = "No Info"
            product_info["Regal"] = regal_info

            # Preis Information
            price_info = soup.find("span", class_="price--content").get_text(strip=True)
            product_info["Preis"] = price_info

            imgsoup = soup.find("span", class_="image--element").get("data-img-webp-original")
            if imgsoup:
                webp_original_url = imgsoup
            else: webp_original_url = "No Info"
            product_info["Image-WEBP"] = webp_original_url

            products[product_name] = product_info

        return products
    
m = MonsterTest()
print(m.get_monsters())