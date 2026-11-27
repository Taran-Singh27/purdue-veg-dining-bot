import requests
from datetime import datetime
from zoneinfo import ZoneInfo

def find_food_location(location, food):

    api = "https://api.hfs.purdue.edu/menus/v2/locations/" + location + "/" + datetime.now(ZoneInfo("America/Indiana/Indianapolis")).strftime('%Y-%m-%d')
    response = requests.get(api)

    
    if response.status_code == 200:
        data = response.json()
        
        food_items = {}

        for meal in data["Meals"]:
            if meal["Name"] == food:
                for station in meal["Stations"]:
                    stationName = []
                    for item in station["Items"]:
                        if item["IsVegetarian"] == True:
                            stationName.append(item["Name"])
                    food_items[station["Name"]] = stationName

        return food_items
    else:
       return "There was some issue with the API. Error code " + str(response.status_code)


## results = find_food_location("Wiley", "Lunch")
## print(results)