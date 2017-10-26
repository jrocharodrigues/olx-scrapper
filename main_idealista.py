#!/usr/bin/python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Flat
import smtplib
from email.mime.text import MIMEText
import datetime


def send_results(flats):
    has_new_flats = False
    message = ""
    for flat in flats:
        has_new_flats = True
        message += flat.name + " - " + flat.location + " - " + flat.price + " " + flat.link + + "\r\n\r\n"

    if has_new_flats:
        msg = MIMEText(message.encode('utf-8'), 'plain', 'utf-8')
        me = 'jowood@blackbox.impecabel.com'
        you = 'jowood09@gmail.com'
        msg['Subject'] = 'New Flats Idealista'
        msg['From'] = me
        msg['To'] = you
        s = smtplib.SMTP('localhost')
        s.sendmail(me, [you], msg.as_string())
        s.quit()




    


engine = create_engine('sqlite:///flats_idealista.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


for x in range(1, 2):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    url = "https://www.idealista.pt/areas/arrendar-casas/pagina-{0}2?shape=%28%28qdtvFx%7Bot%40oEqGoyKewBkvFek%5EtbQj%7DAtsApm_%40%29%29&ordem=atualizado-desc"
    r = requests.get(url.format(x), headers=headers)
    page = r.text

    soup = BeautifulSoup(page, "html.parser")
    ads = soup.find_all("article")

    for ad in ads:

        name = ad.find("a", valign="top")\
            .get_text()\
            .strip()

        flat = session.query(Flat).filter_by(name = name).one_or_none()

        if not flat:
            flat = Flat()
            flat.name = name
            flat.link = ad.find("a").get('href')
            flat.price =ad.find("span", {'class':'item-price'}).get_text().strip()
            flat.location = ""
            flat.is_new = True

        else:
            flat.is_new = False

        session.add(flat)
        session.commit()


flats = session.query(Flat).filter_by(is_new = True).all()
send_results(flats)
for flat in flats:
    print()
    print(datetime.datetime.now())
    print("title:", (flat.name).encode('utf-8'))
    print("link:", (flat.link).encode('utf-8'))
    print("price:", (flat.price).encode('utf-8'))
    print("location:", (flat.location).encode('utf-8'))
    print("date:", flat.created_date)