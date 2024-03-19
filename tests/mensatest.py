import requests

base_url = "https://www.mensa-kl.de/api.php"
params = {"format": "json", "date": 0}

response = requests.get(f"{base_url}", params=params)
response.raise_for_status()
data = response.json()
if data:
    ausgabe1 =""
    ausgabe2 =""
    ausgabe3 =""
    ausgabe4 =""
    for meal in data:
            title = meal["title_with_additives"]
            price = meal["price"]
            image_url = meal["image"]
            icon = meal["icon"]
            ausgabe = str(meal["loc"])

            if "1" in ausgabe:
                ausgabe1 += f"Ausgabe {ausgabe} **{title}** - {price}€\n"
            elif "Atrium" in ausgabe:
                ausgabe3 += f"{ausgabe} **{title}** - {price}€\n"
            elif "Abend" in ausgabe:
                ausgabe4 += f"Abendmensa {ausgabe} **{title}** - {price}€\n"
            else:
                ausgabe2 += f"{ausgabe} **{title}** - {price}€\n"

