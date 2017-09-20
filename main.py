from bs4 import BeautifulSoup
import requests

class Flat:
    pass


url = 'https://www.olx.pl/nieruchomosci/mieszkania/wynajem/gdansk/?search%5Bfilter_float_price%3Afrom%5D=600&search%5Bfilter_float_price%3Ato%5D=1200&search%5Bdist%5D=10'


r = requests.get(url)
page = r.text

soup = BeautifulSoup(page, "html.parser")

ads = soup.find_all("table", summary="Ogłoszenie")

flats = []

for ad in ads:
    flat = Flat()
    flat.name = ad.find("td", valign="top")\
        .find("strong")\
        .get_text()\
        .strip()
    flat.link = ad.find("a").get('href')
    flat.price = ad.find("p", class_="price").get_text().strip()
    flat.location = ad.find("td", valign="bottom")\
        .find("small")\
        .get_text()\
        .strip()

    flats.append(flat)

for flat in flats:
    print()
    print("nazwa:", flat.name)
    print("link:", flat.link)
    print("cena:", flat.price)
    print("lokalizacja:", flat.location)

