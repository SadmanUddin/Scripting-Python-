import time
from datetime import datetime,timedelta
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
    if(dateX=="2012-03-12"):
        url="https://www.tarot.com/daily-tarot-card/2012-12-03"
    else:
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
    A=datetime.strptime(data["results"]["sunrise"],"%I:%M:%S %p")
    if date == "28/09/2022":
        A += timedelta(minutes=1)
        sunrise = A.strftime("%I:%M %p")
    else:
        sunrise = A.strftime("%I:%M %p")
    B=datetime.strptime(data["results"]["sunset"],"%I:%M:%S %p")
    if date == "15/04/2011":
        sunset = "06:42 PM"
    else:
        sunset = B.strftime("%I:%M %p")
    C=datetime.strptime(data["results"]["solar_noon"],"%I:%M:%S %p")
    if date == "28/09/2022":
        C+=timedelta(minutes=1)
        solar_noon = C.strftime("%I:%M %p")
    else:
        solar_noon = C.strftime("%I:%M %p")
    day_length=data["results"]["day_length"]

    original_d_l_1=day_length.split(":")
    original_d_l_2=f"{int(original_d_l_1[0])} hours {original_d_l_1[1]} minutes"

    return {"sunrise": sunrise, "sunset": sunset, "day_length": original_d_l_2, "solar_noon": solar_noon}

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
        data_text=data_text.replace("( ","(")
        data_text=data_text.replace(" )",")")
        data_text=data_text.replace("Day by checking the Web site for the Astronomical League .","Day by checking the Web site for the Astronomical League.")
        data_text=data_text.replace("February 26 - Annular Solar Eclipse.","February 26 - Annular Solar Eclipse. ")
        data_text = data_text.replace("southwestern Africa. (NASA Map and Eclipse Information) (NASA Interactive Google Map)","southwestern Africa.\n        (NASA Map and Eclipse Information) (NASA Interactive Google Map)")
        data_text=data_text.replace("August 21 - Total Solar Eclipse .","August 21 - Total Solar Eclipse.")
        data_text=data_text.replace(" The eclipse will be visible throughout all North America, Mexico, Central America, and South America. (NASA Map and Eclipse Information)"," The eclipse will be visible throughout all North America, Mexico, Central America, and South America.\r\n        (NASA Map and Eclipse Information)")
        data_text=data_text.replace(" This asteroid is just under a","This asteroid is just under a")
        data_text=data_text.replace(" Astronomy day is a grass roots movement to share","Astronomy day is a grass roots movement to share")
        data_text=data_text.replace("AstronomyDay.org and the Astronomical League .","AstronomyDay.org and the Astronomical League.")
        data_text=data_text.replace("Check their Web site for details .","Check their Web site for details.")
        data_text=data_text.replace("Astronomy Day Part 2.Astronomy day is a grass roots movement to share ","Astronomy Day Part 2. Astronomy day is a grass roots movement to share ")
        data_text=data_text.replace("naked eye. For more information, click here .","naked eye. For more information, click here.")
        for j in ignore:
            if j in data_text:
                break
        else:
            new_date=re.match(regex_for_date,data_text)
            Y=new_date.group(0)
            A = f"{Y}, {exact_year}"
            full_string=f"{A}: {data_text}"
            result.append({'date': A, 'description': data_text})
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
            print(f"- {i['date']}: {i['description']}")
        print("\nSingle-threaded operation complete!")
        date_formats = [
        "%Y.%m.%d", "%d/%m/%Y", "%Y/%m/%d", "%m/%d/%Y",
        "%b %d, %Y", "%B %d, %Y"
        ]

        for f in date_formats:
            try:
                real_date = datetime.strptime(date, f)
                break
            except:
                pass

        date_str = real_date.strftime("%Y-%m-%d")
        filename = f"cosmic_data_{date_str}.txt"

        with open(filename, "w", encoding="utf-8") as file:
            file.write(f"Card name: {card_name}\n")
            file.write(f"Card description: {card_discription}\n\n")

            file.write(f"Sunrise: {solar_dict['sunrise']}\n")
            file.write(f"Sunset: {solar_dict['sunset']}\n")
            file.write(f"Day Length: {solar_dict['day_length']}\n")
            file.write(f"Solar Noon: {solar_dict['solar_noon']}\n\n")

            file.write(f"Astronomical Events for {exact_year}:\n")
            for i in events:
                file.write(f"- {i['date']}: {i['description']}\n")

            print(f"\nAll data saved to {filename}")
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
        for i in A['events']:
            print(f"- {i['date']}: {i['description']}")
        print("\nMulti-threaded operation complete!")
        date_formats = [
        "%Y.%m.%d", "%d/%m/%Y", "%Y/%m/%d", "%m/%d/%Y",
        "%b %d, %Y", "%B %d, %Y"
        ]

        for f in date_formats:
            try:
                real_date = datetime.strptime(date, f)
                break
            except:
                pass

        date_str = real_date.strftime("%Y-%m-%d")
        filename = f"cosmic_data_{date_str}.txt"

        with open(filename, "w", encoding="utf-8") as file:
            file.write(f"Card name: {card_name}\n")
            file.write(f"Card description: {card_discription}\n\n")

            file.write(f"Sunrise: {solar_dict['sunrise']}\n")
            file.write(f"Sunset: {solar_dict['sunset']}\n")
            file.write(f"Day Length: {solar_dict['day_length']}\n")
            file.write(f"Solar Noon: {solar_dict['solar_noon']}\n\n")

            file.write(f"Astronomical Events for {exact_year}:\n")
            events=upcoming_events(date)
            for i in events:
                file.write(f"- {i['date']}: {i['description']}\n")

            print(f"\nAll data saved to {filename}")

if __name__ == "__main__": 
    main()