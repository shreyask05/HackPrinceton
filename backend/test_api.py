import json
import os
import requests as req


congress_api_key = os.getenv('CONGRESS_API_KEY')
#print("api key is: " + congress_api_key)

url = f"https://api.congress.gov/v3/bill/117/hr/3076/subjects?api_key={congress_api_key}"
response = req.get(url)
with open("response.json", "w") as f:
    json.dump(response.json(), file=f, indent=4)
print(response.json())