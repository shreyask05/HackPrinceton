# import requests
# import json

# # Example: Fetch recent bills related to finance
# BASE_URL = "https://www.govtrack.us/api/v2/bill"

# # You can filter by subject, sponsor, status, etc.
# params = {
#     "sort": "-introduced_date",        # Most recent first
#     "limit": 20,                      # Number of results
#     "q": "health"
# }

# response = requests.get(BASE_URL, params=params)

# if response.status_code == 200:
#     data = response.json()
#     filtered_bills = [
#         bill for bill in data["objects"]
#         if bill["current_status_label"] != "Introduced"
#     ]

#     for bill in filtered_bills:
#         #print(bill)
#         print("Title:", bill["title"])
#         print("Introduced:", bill["introduced_date"])
#         print("Current Status Label:", bill["current_status_label"])
#         print("Full Text Link:", bill["link"])
#         print("-----\n")
# else:
#     print("Error:", response.status_code)

import google.generativeai as genai

# Configure with your API key
genai.configure(api_key="AIzaSyBg8cUQtS_zXZ1Dk8B2cTa7sVaB_eaAuKA")

# List available models to see what's available
models = genai.list_models()
model = genai.GenerativeModel("gemini-1.5-pro") 

prompt = "For bill number 1069, Congress 119, Summarize the bill and assess its potential economic impact and the financial implications. Rate the sentiment as positive, negative, or neutral, and justify your reasoning"
response = model.generate_content(prompt)
print(response.text)