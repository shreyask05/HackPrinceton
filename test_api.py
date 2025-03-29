import json
import os
import requests

api = os.getenv("CONGRESS_API_KEY")


def get_bill_details(congress, bill_type, bill_number):
    print("Getting bill details")
    url = f"https://api.congress.gov/v3/bill/{congress}/{bill_type}/{bill_number}?api_key={api}"
    response = requests.get(url)
    data = response.json()

    bill_data = data.get("bill", {})  # Ensure we access the nested 'bill' object

    return {
        "title": bill_data.get("title", "Unknown"),
        "bill_type": bill_type,
        "bill_number": bill_number,
        "congress": congress,
        "sponsors": [s.get("fullName", "Unknown") for s in bill_data.get("sponsors", [])],
        "latest_action": bill_data.get("latestAction", {}).get("text", "N/A"),
        "committees": bill_data.get("committees", {}).get("url", "N/A"),
        "subjects": bill_data.get("subjects", {}).get("url", "N/A"),
    }



res = get_bill_details(118, 'hr', 9758)
print(res)
print('committee info')

url = res['committees'] + '&api_key=' + str(api)
response = requests.get(url)
print(json.dumps(response.json(), indent=2))

print('subject info')
url = res['subjects'] + '&api_key=' + str(api)
response = requests.get(url)
print(json.dumps(response.json(), indent=2))