import requests
import json

# Example: Fetch recent bills related to finance
BASE_URL = "https://www.govtrack.us/api/v2/bill"

# You can filter by subject, sponsor, status, etc.
params = {
    "sort": "-introduced_date",        # Most recent first
    # "limit": 10,                       # Number of results
    "q": "finance",
}

response = requests.get(BASE_URL, params=params)

if response.status_code == 200:
    data = response.json()
    filtered_bills = [
        bill for bill in data["objects"]
        if bill["current_status_label"] != "Introduced"
    ]

    for bill in filtered_bills:
        #print(bill)
        print("Title:", bill["title"])
        print("Introduced:", bill["introduced_date"])
        print("Current Status Label:", bill["current_status_label"])
        print("Full Text Link:", bill["link"])
        print("-----\n")
else:
    print("Error:", response.status_code)
