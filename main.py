#!/usr/bin/python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Flat
import smtplib
from email.mime.text import MIMEText


def send_results(flats):
    has_new_flats = False
    message = ""
    for flat in flats:
        has_new_flats = True
        message += flat.name + " - " + flat.location + " - " + flat.price + " " + flat.link + "\n"

    if has_new_flats:
        msg = MIMEText(message.encode('utf-8'), 'plain', 'utf-8')
        msg['Subject'] = 'New Flats'
        msg['From'] = 'jowood@blackbox.impecabel.com'
        msg['To'] = 'jowood09@gmail.com'
        s = smtplib.SMTP('localhost')
        s.sendmail(me, [you], msg.as_string())
        s.quit()




    


engine = create_engine('sqlite:///flats.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


for x in range(1, 2):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    url = "https://www.olx.pt/imoveis/apartamento-casa-a-venda/apartamentos-arrenda/gloria/?search%5Bdescription%5D=1&search%5Bdist%5D=10&search%5Bfilter_enum_tipologia%5D%5B0%5D=t1&search%5Bfilter_enum_tipologia%5D%5B1%5D=t2&page={0}"
    r = requests.get(url.format(x), headers=headers)
    page = r.text

    soup = BeautifulSoup(page, "html.parser")
    ads = soup.find_all("table", summary="Anúncio")

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
send_results(flats)
for flat in flats:
    print()
    print("title:", flat.name)
    print("link:", flat.link)
    print("price:", flat.price)
    print("location:", flat.location)
    print("date:", flat.created_date)