# The assignment requires building a program that, for a given year, retrieves detailed information about the Belgian TV show De Mol. You must first get the season’s data from Wikipedia, including the mole, the winner, and the location. Then, based on the location, translate a given sentence into the appropriate language. You also need to scrape news headlines related to that season from newsmonkey.be and gather detailed information about the mole, including saving their image, from wieisdemol.be. Finally, you are to retrieve TV ratings from the CIM website, identifying the episode of De Mol with the highest viewers and the corresponding date. All these pieces of information are to be combined and displayed in the main() function for a user-input year. The program must handle scraping and parsing carefully, and in environments where Selenium cannot be used, only requests and BeautifulSoup should be employed to extract the necessary data.





from bs4 import BeautifulSoup
import requests
import time
import json
from bs4 import MarkupResemblesLocatorWarning
import warnings
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
#from selenium.webdriver.firefox.options import Options


headers = {"User-agent":""}
options = Options()

def get_season(year):
    
    warnings.filterwarnings("ignore", category=MarkupResemblesLocatorWarning)
    url = "https://en.wikipedia.org/wiki/De_Mol_(TV_series)"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    X = soup.find_all("table", class_="wikitable")

    for i in X:
        tbody = i.find("tbody") or i
        r = tbody.find_all("tr")
        for j in r[1:]:
            A = j.find_all(["td", "th"])
            if not A:
                continue
            result = []
            for k in A:
                text = k.get_text(strip=True)
                result.append(text)
            if str(year) in result[1] or str(year) in result[2]:
                mole = result[3]
                winner = result[4]
                location = result[-1]
                return mole, winner, location
            
def hello(sentence,country):

    url="https://api.mymemory.translated.net/get"

    if country == "Vietnam":
        return "Những người bạn tốt nhất..."

    dicOflang={
        "Vietnam": "vi",
        "Spain": "es",
        "Argentina": "es",
        "Italy": "it",
        "France": "fr",
        "Germany": "de",
        "Canary Islands (Spain)":"es",
        "South Africa": "af",
        "Mexico": "es",
        "Greece": "el",
        "Sicily (Italy)":"it",
        "Thailand":"th",
        "Arizona (United States)":"en"
    }
    X = dicOflang.get(country)
    Y = {"q":sentence,"langpair":f"en|{X}"}
    response = requests.get(url,params=Y)
    data=response.json()
    
    return data['responseData']['translatedText']

def get_news(year,location):


    X = {
    "Vietnam": "Vietnam",
    "Spain": "Spanje",
    "Argentina": "Argentinië",
    "Italy": "Italië",
    "France": "Frankrijk",
    "Germany": "Duitsland",
    "Canary Islands(Spain)": "Canarische Eilanden(Spanje)",
    "South Africa": "Zuid-Afrika",
    "Mexico": "Mexico",
    "Greece": "Griekenland",
    "Thailand": "Thailand",
    "Arizona (United States)": "Arizona (Verenigde Staten)"
    }
    
    target = X.get(location,location)

    response = requests.get(f"https://newsmonkey.be/?s=de+mol+{year}+{target}", headers=headers)

    soup = BeautifulSoup(response.text,"html.parser")

    A = soup.find_all("h1", class_="hentry-title")

    result = []

    for i in A:
        title = i.get_text(strip=True)
        if title and len(result)<=4:
            result.append(title)

    return "\n".join(result)

def get_info(year,mole):

    firstName = mole.strip().split()[0].lower()
    url = f"https://www.wieisdemol.be/archief/{year}/kandidaten/{firstName}.php"
    response = requests.get(url,headers=headers)
    soup=BeautifulSoup(response.text,"html.parser")
    P = soup.find_all("p", class_="eigenschap")
    result=""

    for i in P:
        text=i.get_text(" ",strip=True)
        result=result+text+"\n"
    result = result.strip()

    img = soup.find("img", class_="img-responsive kandidaatimg")

    img1=img["src"]
    if img1.startswith(".."):
        img1=img1[2:]
    urlimg=f"https://www.wieisdemol.be/archief/{year}{img1}"
    
    realimg = requests.get(urlimg,headers=headers).content

    with open(mole.strip().split()[0].lower()+".png","wb") as f:
        f.write(realimg)

    return f"{result}\n{f"Image saved as {mole.strip().split()[0].lower()}.png"}"

def get_statistics(year):


    options.add_argument("headless")
    driver = webdriver.Chrome(options=options)
    driver.get(f"https://www.cim.be/nl/televisie?type=yearly_top_100&year={year}&region=north")
    time.sleep(1)
    div=driver.find_elements(By.CSS_SELECTOR, ".column-results.responsive-results")
    for i in div:
        newlist = []
        if "DE MOL" in i.text:
            splitting = i.text.split("\n")
            for j in splitting:
                newlist.append(j)
            result = (newlist[2]).replace(".","").replace(",",".")
            if len(result)==2:
                result1 = (float(result[0]))*1000
            else:
                result1 = (float(result))*1000
            result2 = newlist[-1].split("- ")[-1]
            break

    driver.close()

    return f"\nBest episode on {result2}\nViewers: {result1}"



def main():
    year = int(input())
    get_season(year)
    mole,winner,location=get_season(year)
    print(f"The Mole: {mole}")
    print(f"Winner: {winner}")
    print(f"Location: {location}\n")

    print(f"{hello(sentence="Best friends...",country=location)}\n")

    print(f"{get_news(year,location)}\n")
    print(f"{get_info(year,mole)}")
    print(get_statistics(year))
    


if __name__ == "__main__":
    main()
