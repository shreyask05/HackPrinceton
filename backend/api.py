import os
import json
import requests
api = os.getenv("CONGRESS_API_KEY")

url = f"https://api.congress.gov/v3/bill/117/hr/3076/actions?api_key={api}"
response = requests.get(url)
print(json.dumps(response.json(), indent=2))