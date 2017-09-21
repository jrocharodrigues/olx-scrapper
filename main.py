from bs4 import BeautifulSoup
import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Flat


engine = create_engine('sqlite:///flats.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


for x in range(1, 4):
    url = "https://www.olx.pl/nieruchomosci/mieszkania/wynajem/gdansk/?search%5Bfilter_float_price%3Afrom%5D=600&search%5Bfilter_float_price%3Ato%5D=1200&search%5Bdist%5D=10&page={0}"
    r = requests.get(url.format(x))
    page = r.text

    soup = BeautifulSoup(page, "html.parser")
    ads = soup.find_all("table", summary="Ogłoszenie")

    for ad in ads:

        name = ad.find("td", valign="top")\
            .find("strong")\
            .get_text()\
            .strip()

        flat = session.query(Flat).filter_by(name = name).one_or_none()

        if not flat:
            flat = Flat()
            flat.name = name
            flat.link = ad.find("a").get('href')
            flat.price = ad.find("p", class_="price").get_text().strip()
            flat.location = ad.find("td", valign="bottom") \
                .find("small") \
                .get_text() \
                .strip()
            flat.is_new = True

        else:
            flat.is_new = False

        session.add(flat)
        session.commit()


flats = session.query(Flat).filter_by(is_new = True).all()

for flat in flats:
    print()
    print("nazwa:", flat.name)
    print("link:", flat.link)
    print("cena:", flat.price)
    print("lokalizacja:", flat.location)
    print("data dodania:", flat.created_date)