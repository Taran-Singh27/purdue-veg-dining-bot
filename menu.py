import requests

response = requests.get("https://api.hfs.purdue.edu/menus/v2/locations/Wiley/2026-11-23")

if response.status_code == 200:
    data = response.json()
    print(data)
else:
    print(response.status_code)