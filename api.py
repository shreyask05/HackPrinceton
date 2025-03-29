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

import requests
from bs4 import BeautifulSoup
import google.generativeai as genai

# Step 1: Configure API key
genai.configure(api_key="AIzaSyBg8cUQtS_zXZ1Dk8B2cTa7sVaB_eaAuKA")

# Step 2: Load the model
model = genai.GenerativeModel("gemini-1.5-pro")

# Step 3: Function to get bill text from HTML
def extract_text_from_html_url(url):
    print(f"Fetching bill from: {url}")
    response = requests.get(url)
    
    if not response.ok or "We couldn't find that page" in response.text:
        print("❌ Page not found or failed request.")
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    for tag in soup(["script", "style"]):
        tag.decompose()

    return soup.get_text(separator=' ', strip=True)

# Step 4: Construct prompt with bill text
def generate_bill_analysis(congress, bill_number, bill_text):
    prompt = f"""
For bill number {bill_number}, Congress {congress}, perform the following tasks:
1. Summarize the bill in plain language.
2. Assess its potential economic impact and financial implications.
3. Rate the sentiment with respect to the stock market as positive, negative, or neutral and confidence score in numbers— and justify your reasoning based on the content.

Here is the full text of the bill:
\"\"\"
{bill_text}
\"\"\"
"""
    return model.generate_content(prompt).text

# Step 5: Example usage
if __name__ == "__main__":
    # Replace with actual bill link (HTML version)
    # url = "https://www.congress.gov/119/bills/hr1069/BILLS-119hr1069ih.htm"
    # url = "https://www.congress.gov/119/bills/hjres75/BILLS-119hjres75eh.xml"
    # url = "https://www.congress.gov/117/plaws/publ167/PLAW-117publ167.htm" #CHIPS ACT Positive, High
    # url = "https://www.congress.gov/119/bills/hr25/BILLS-119hr25ih.xml" #Netural, Low; Scores → Negative: 0.0191, Neutral: 0.0790, Positive: 0.9020
    url = "https://www.congress.gov/118/bills/hr25/BILLS-118hr25ih.xml" #Netural, Low; Scores → Negative: 0.0190, Neutral: 0.0775, Positive: 0.9035
    bill_text = extract_text_from_html_url(url)
    bill_text = bill_text[:8000]  # approx. ~2-3 pages

    if bill_text:
        analysis = generate_bill_analysis(congress=119, bill_number=1069, bill_text=bill_text)
        print("\n📘 Bill Analysis:\n")
        print(analysis)
    else:
        print("⚠️ Skipping Gemini analysis due to missing bill text.")
