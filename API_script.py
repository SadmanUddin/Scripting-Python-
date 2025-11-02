#The assignment is to build a Python digital assistant with four features: weather info (returning temperature, feels-like, conditions, humidity, wind), knowledge queries (returning a Wikipedia summary), translation (returning original and translated text for a chosen language), and entertainment (returning movie info from OMDB, a joke from icanhazdadjoke, or a quote from type.fit). All functions must return dictionaries, handle user inputs, and allow returning to the main menu.




import requests
import json
import time
import wikipedia

def weather(location):
    KEY = "" # You can use your own API keys...i cannot provide mine cause its paid
    X = f'https://api.openweathermap.org/data/2.5/weather?q={location}&units=metric&appid={KEY}'

    Data = requests.get(X)
    
    New_data = Data.json()

    temp = New_data["main"]["temp"]
    country = New_data["sys"]["country"]
    feelslike = New_data["main"]["feels_like"]
    condi = New_data["weather"][0]["description"].title()
    humi = New_data["main"]["humidity"]
    wind = round((New_data["wind"]["speed"] * 3.6))

    result=(
        f"WEATHER IN {location.upper()}, {country}:\n"
        f"Temperature: {temp}°C\n"
        f"Feels like: {feelslike}°C\n"
        f"Conditions: {condi}\n"
        f"Humidity: {humi}\n"
        f"Wind: {wind} km/h"
    )
    return result

def knowledge(query):
    result = wikipedia.summary(query,6)
    return result


def translate(text, target_language):
    translationtool = "https://api.mymemory.translated.net/get"
    questions = {"q":text, "langpair":f'en|{target_language}'}
    data = requests.post(translationtool, data=questions)

    new_data = data.json()
    result = new_data["responseData"]["translatedText"]
    return result

def entertainment(category, movie_title=None):
    key = "" #provide an API key of your own 
    if category == 1:
        link=f'http://www.omdbapi.com/?t={movie_title}&apikey={key}'
        data = requests.get(link)
        new_data = data.json()

        title = new_data['Title']
        year = new_data['Year']
        rating = new_data["imdbRating"]
        dir = new_data["Director"]
        cast = new_data["Actors"]
        plot = new_data["Plot"]


        result1 = (
             f'Title: {title} ({year})\n'
             f'Rating: {rating}\n'
             f'Director: {dir}\n'
             f'Cast: {cast}\n'
             f'Plot: {plot}\n'
         )
        
        return result1
    
    elif category == 2:
        link = requests.get("https://icanhazdadjoke.com/", headers={"Accept": "application/json"})

        data = link.json()

        result2 = data["joke"]

        return result2
    
    elif category == 3:
        data = requests.get("https://api.quotable.io/random")
        new_data = data.json()
        result3 = f"{new_data['content']} — {new_data['author']}"

        return result3




if __name__ == "__main__":

    while True:
        print("DIGITAL ASSISTANT")
        print("-----------------")
        print("1. Weather Information")
        print("2. Knowledge Query")
        print("3. Translation Service")
        print("4. Entertainment")
        print("5. Exit")

        number = input("Please select an option:")

        if number == "1":
            location = input("Enter location:")
            print(weather(location))
        elif number == "2":
            query = input("Search in wikipedia:")
            print(f"{query}:")
            print(knowledge(query))
        elif number == "3":
            text = input("Enter text to translate:")
            print("Available target languages:")
            print("1. Spanish")
            print("2. French")
            print("3. German")
            print("4. Italian")
            print("5. Dutch")
            choice = input("Select target language (1-5):")

            dic = {"1": "es", "2": "fr", "3": "de", "4": "it", "5": "nl"}
            target_language = dic.get(choice)
            print("Translation:")
            print(f'Original: {text}')
            print(f'Translated text: {translate(text,target_language)}')

        elif number == "4":
            print("Entertainment options:")
            print("1. Movie Information")
            print("2. Random Joke")
            print("3. Inspirational Quote")

            selection = input("Select entertainment type (1-3):")
            if selection == "1":
                x = input("Enter movie title:")
                print("MOVIE INFORMATION:")
                print(entertainment(1,x))
            elif selection == "2":
                print("RANDOM JOKE:")
                print(entertainment(2))
            elif selection == "3":
                print("QUOTE:")
                print(entertainment(3))
        elif number == "5":
            print("Thank you for using Digital Assistant!")
            break
        
        time.sleep(1)
        back = input("\nReturn to main menu? (y/n): ")
        if back.lower() != "y":
            print("Thank you for using Digital Assistant!")
            break

