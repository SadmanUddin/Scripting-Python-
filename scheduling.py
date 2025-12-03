import time
from datetime import datetime 
from bs4 import BeautifulSoup
import requests
import json
import threading
import subprocess
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from geopy.geocoders import Nominatim
import re

def daily_tarot(date):
    X = [
        "%Y.%m.%d", "%d/%m/%Y", "%Y/%m/%d", "%m/%d/%Y", "%b %d, %Y", "%B %d, %Y", "%Y.%d.%m"
    ]
    for i in X:
        try:
            real_date = datetime.strptime(date, i)
            break
        except ValueError:
            continue
    
    dateX = real_date.strftime("%Y-%m-%d")

    url = f"https://www.tarot.com/daily-tarot-card/{dateX}"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    script = soup.find("script", type="application/ld+json")
    data = json.loads(script.string)
    card_name=data['articleBody']
    main=card_name.split(":",1)
    title_name=main[0].strip()
    main_title=" ".join(title_name.split(" ")[1:])
    card_dis=main[1].strip()
    return {'card_name': main_title, 'card_description': card_dis}

def moon_phase(date):
    url = f"https://www.farmsense.net/api/astro-widgets/phase/?date={date.timestamp()}"
    X = requests.get(url)
    data = X.json()
    print(data)


def solar_data(date,location):

    X = [
        "%Y.%m.%d", "%d/%m/%Y", "%Y/%m/%d", "%m/%d/%Y", "%b %d, %Y", "%B %d, %Y"
    ]
    for i in X:
        try:
            real_date = datetime.strptime(date, i)
            break
        except ValueError:
            continue

    dateX = real_date.strftime("%Y/%m/%d")
    X = Nominatim(user_agent="sadman")
    loc=X.geocode(location)
    lat=loc.latitude
    lng=loc.longitude
    url=f"https://api.sunrise-sunset.org/json?lat={lat}&lng={lng}&date={dateX}"
    res=requests.get(url)
    data=res.json()
    sunrise = data["results"]["sunrise"]
    sunset=data["results"]["sunset"]
    solar_noon=data["results"]["solar_noon"]
    day_length=data["results"]["day_length"]
    
    return {"sunrise": sunrise, "sunset": sunset, "day_length": day_length, "solar_noon": solar_noon}


def upcoming_events(date):
    X = [
        "%Y.%m.%d", "%d/%m/%Y", "%Y/%m/%d", "%m/%d/%Y", "%b %d, %Y", "%B %d, %Y"
    ]
    for i in X:
        try:
            real_date = datetime.strptime(date, i)
            break
        except ValueError:
            continue
    exact_year=real_date.year
    url=f"http://www.seasky.org/astronomy/astronomy-calendar-{real_date.year}.html"
    res=requests.get(url)
    soup=BeautifulSoup(res.text,"html.parser")
    data=soup.find_all("li")
    ignore={"Home","Explore the Sea","Explore the Sky","About","FAQs","Site Map","Privacy","Contact"}
    regex_for_date=r"^(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d+"
    result = []
    for i in data:
        data_text=i.get_text(" ",strip=True)
        skip = False
        for j in ignore:
            if j in data_text:
                skip = True
                break
        else:
            new_date=re.match(regex_for_date,data_text)
            Y=new_date.group(0)
            A = f"{Y}, {exact_year}"
            full_string=f"{A}: {data_text}"
            result.append(full_string)
    return result

    


def main():
    date = input().strip()
    location = input()
    mode=input()
    A={}
    def fetch_tarot():
        A['tarot'] = daily_tarot(date)
    def fetch_solar():
        A['solar'] = solar_data(date, location)
    def fetch_events():
        A['events'] = upcoming_events(date)
    
    if mode=="single":
        daily_tarot(date)
        main_data = daily_tarot(date)
        card_name=main_data['card_name']
        card_discription=main_data['card_description']
        print(f"Card name: {card_name}\nCard description: {card_discription}\n")

        solar_dict = solar_data(date, location)

        print(f"Sunrise: {solar_dict['sunrise']}")
        print(f"Sunset: {solar_dict['sunset']}")
        print(f"Day Length: {solar_dict['day_length']}")
        print(f"Solar Noon: {solar_dict['solar_noon']}")
        X = [
            "%Y.%m.%d", "%d/%m/%Y", "%Y/%m/%d", "%m/%d/%Y", "%b %d, %Y", "%B %d, %Y"
        ]
        for i in X:
            try:
                real_date = datetime.strptime(date, i)
                break
            except ValueError:
                continue
        exact_year=real_date.year
        print(f"\nAstronomical Events for {exact_year}:")
        events=upcoming_events(date)
        for i in events:
            print(f"- {i}")
        print("\nSingle-threaded operation complete!")
    else:
        threads = [
            threading.Thread(target=fetch_tarot),
            threading.Thread(target=fetch_solar),
            threading.Thread(target=fetch_events)
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
    
        card_name = A['tarot']['card_name']
        card_discription = A['tarot']['card_description']
        print(f"Card name: {card_name}\nCard description: {card_discription}\n")

        solar_dict = A['solar']
        print(f"Sunrise: {solar_dict['sunrise']}")
        print(f"Sunset: {solar_dict['sunset']}")
        print(f"Day Length: {solar_dict['day_length']}")
        print(f"Solar Noon: {solar_dict['solar_noon']}")
    
        X = ["%Y.%m.%d", "%d/%m/%Y", "%Y/%m/%d", "%m/%d/%Y", "%b %d, %Y", "%B %d, %Y"]
        for fmt in X:
            try:
                real_date = datetime.strptime(date, fmt)
                break
            except ValueError:
                continue
        exact_year = real_date.year

        print(f"\nAstronomical Events for {exact_year}:")
        for e in A['events']:
            print(f"- {e}")
        print("\nMulti-threaded operation complete!")
        


if __name__ == "__main__": 
    main()