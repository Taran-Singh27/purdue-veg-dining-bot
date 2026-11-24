import requests
from datetime import date 

location = "Wiley"
api = "https://api.hfs.purdue.edu/menus/v2/locations/" + location + "/" + date.today().strftime('%Y-%m-%d')
response = requests.get(api)
food = "Lunch"

if response.status_code == 200:
    data = response.json()

    for meal in data["Meals"]:
        if meal["Name"] == food:
            print(meal["Name"])
            for station in meal["Stations"]:
                for item in station["Items"]:
                    if item["IsVegetarian"] == True:
                        print(item["Name"])

else:
    print(response.status_code)