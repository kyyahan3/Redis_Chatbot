import random
import json
import os
import redis

FILE_PATH ='./data'

def weather_data_generate():
    cities = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia", "San Antonio",
    "San Diego", "Dallas", "San Jose", "Austin", "Jacksonville", "Fort Worth", "Columbus", "Charlotte", "Indianapolis", 
    "Seattle", "Denver", "Washington", "Boston", "El Paso", "Nashville", "Oklahoma City", "Las Vegas", "Detroit", 
    "Portland", "Memphis", "Louisville", "Milwaukee", "Baltimore", "Albuquerque", "Tucson", "Fresno", "Mesa", 
    "Sacramento", "Atlanta", "Kansas City", "Colorado Springs", "Miami", "Raleigh", "Omaha", "Long Beach", 
    "Virginia Beach", "Oakland", "Minneapolis", "Tampa", "Tulsa", "Arlington", "New Orleans"]

    # Generate random weather data for each city
    weather_data = {}
    for city in cities:
        temperature = round(random.uniform(50, 100), 1)
        humidity = random.randint(20, 90)
        conditions = random.choice(["Sunny", "Partly Cloudy", "Cloudy", "Rainy", "Snowy"])

        weather_data[city] = {
        "temperature": temperature,
        "humidity": humidity,
        "conditions": conditions
        }

    # Convert the data to JSON format
    json_data = json.dumps(weather_data, indent=2)

    # Save the JSON data to a file (replace 'weather_data.json' with your desired filename)
    with open(os.path.join(FILE_PATH,'weather_data.json'), 'w') as file:
        file.write(json_data)

    print("Weather data has been generated and saved to 'weather_data.json'.")


def fun_facts_generate():
    # List of 50 random fun facts
    fun_facts = [
        "Honey never spoils. Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years old and still perfectly edible.",
        "Octopuses have three hearts: two pump blood to the gills, while the third pumps it to the rest of the body.",
        "A group of flamingos is called a 'flamboyance.'",
        "The shortest war in history was between Britain and Zanzibar on August 27, 1896. It lasted only 38 minutes.",
        "Bananas are berries, but strawberries are not.",
        "A newborn kangaroo is about 1 inch long, and it completes its development outside the womb, inside its mother's pouch.",
        "The unicorn is Scotland's national animal.",
        "Honeybees can recognize human faces.",
        "The Eiffel Tower can be 15 cm taller during the summer due to the expansion of the iron from the heat.",
        "The average person will spend six months of their life waiting for red lights to turn green.",
        "Cows have best friends and can become stressed when they are separated from them.",
        "The first recorded game of baseball was played in 1846 in Hoboken, New Jersey.",
        "Banging your head against a wall burns 150 calories per hour.",
        "The world's largest desert is not the Sahara but Antarctica.",
        "Polar bears are nearly undetectable by infrared cameras due to their transparent fur.",
        "The unicorn is Scotland's national animal.",
        "A group of pugs is called a 'grumble.'",
        "The only letter that doesn't appear in any U.S. state name is the letter 'Q.'",
        "A day on Venus is longer than a year on Venus. It takes 243 Earth days for Venus to complete one rotation on its axis.",
        "The longest English word without a vowel is 'rhythms.'",
        "Cows have best friends and can become stressed when they are separated from them.",
        "An octopus has three hearts. Two pump blood to the gills, and one pumps it to the rest of the body.",
        "Bananas are berries, but strawberries are not.",
        "A single strand of spaghetti is called a 'spaghetto.'",
        "There is enough gold in the Earth's core to coat its entire surface to a depth of 1.5 feet.",
        "The name for the shape of Pringles is called a 'Hyperbolic Paraboloid.'",
        "The world's largest desert is not the Sahara but Antarctica.",
        "Cats have a unique grooming pattern called the '3-point turn,' where they lick their lips, lick their front leg, and then wash their face.",
        "In Switzerland, it is illegal to own just one guinea pig because they are prone to loneliness.",
        "The longest time between two twins being born is 87 days.",
        "The longest hiccuping spree lasted 68 years.",
        "A 'jiffy' is a unit of time, equivalent to 1/100th of a second.",
        "The longest wedding veil was longer than 63 football fields.",
        "A 'jiffy' is a unit of time, equivalent to 1/100th of a second.",
        "The longest wedding veil was longer than 63 football fields.",
        "Pineapples take almost three years to grow.",
        "A day on Venus is longer than a year on Venus. It takes 243 Earth days for Venus to complete one rotation on its axis.",
        "The longest hiccuping spree lasted 68 years.",
        "The shortest war in history was between Britain and Zanzibar on August 27, 1896. It lasted only 38 minutes.",
        "The first recorded game of baseball was played in 1846 in Hoboken, New Jersey.",
        "The average person will spend six months of their life waiting for red lights to turn green.",
        "Pineapples take almost three years to grow.",
        "In Switzerland, it is illegal to own just one guinea pig because they are prone to loneliness.",
        "The only letter that doesn't appear in any U.S. state name is the letter 'Q.'",
        "The Eiffel Tower can be 15 cm taller during the summer due to the expansion of the iron from the heat.",
        "The name for the shape of Pringles is called a 'Hyperbolic Paraboloid.'",
        "The shortest war in history was between Britain and Zanzibar on August 27, 1896. It lasted only 38 minutes.",
    ]

    # Shuffle the fun facts to make them random
    random.shuffle(fun_facts)

    # Create a dictionary with the facts
    fun_facts_dict = {f"Fact {i + 1}": fact for i, fact in enumerate(fun_facts[:50])}

    # Save the data to a JSON file
    with open(os.path.join(FILE_PATH, "fun_facts.json"), "w") as json_file:
        json.dump(fun_facts_dict, json_file)

    print("Random fun facts generated and saved to fun_facts.json")

def import_fun_facts_redis(data_json_file):
    r = redis.StrictRedis(host='redis', port=6379, db=0)

    with open(os.path.join(FILE_PATH, data_json_file)) as json_file:
        data = json.load(json_file)
    for key, value in data.items():
        r.set(key, value)
    
    print(f"{data_json_file} imported to redis")

def import_weather_redis(data_json_file):
    r = redis.StrictRedis(host='redis', port=6379, db=0)

    with open(os.path.join(FILE_PATH, data_json_file)) as json_file:
        data = json.load(json_file)

    for city, weather_data in data.items():
            r.hmset(city, weather_data)

    print(f"{data_json_file} imported to redis")


# import_fun_facts_redis("fun_facts.json")
import_weather_redis("weather_data.json")
