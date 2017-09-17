from bs4 import BeautifulSoup
import requests


url = 'https://www.olx.pl/nieruchomosci/mieszkania/wynajem/gdansk/?search%5Bfilter_float_price%3Afrom%5D=600&search%5Bfilter_float_price%3Ato%5D=1200&search%5Bdist%5D=10'


r = requests.get(url)
page = r.text

soup = BeautifulSoup(page)

links = soup.find_all("a")

for link in links:
    print (link.get("href"))

