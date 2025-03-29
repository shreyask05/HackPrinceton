import requests
from bs4 import BeautifulSoup
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import numpy as np
import os

# Load FinBERT once
tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")

# Congress API Key
api = os.getenv("CONGRESS_API_KEY")


# Function to extract bill text from an HTML page
def extract_text_from_html_url(url):
    print(f"Fetching bill from: {url}")
    response = requests.get(url)

    if not response.ok:
        print("Failed to fetch the bill text.")
        return None

    if "We couldn't find that page" in response.text:
        print("Page not found on congress.gov")
        return None

    soup = BeautifulSoup(response.text, "html.parser")

    # Remove script and style tags
    for tag in soup(["script", "style"]):
        tag.decompose()

    clean_text = soup.get_text(separator=' ', strip=True)
    return clean_text


# Function to analyze sentiment of text in chunks
def analyze_sentiment_chunks(text, chunk_size=1024):
    words = text.split()
    chunks = [' '.join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]

    sentiments = []
    for chunk in chunks:
        inputs = tokenizer(chunk, return_tensors="pt", truncation=True, max_length=512)
        outputs = model(**inputs)
        probs = torch.nn.functional.softmax(outputs.logits, dim=1)
        sentiments.append(probs.detach().numpy())

    avg_sentiment = np.mean(sentiments, axis=0).flatten()
    label_map = {0: "negative", 1: "neutral", 2: "positive"}
    sentiment_label = label_map[np.argmax(avg_sentiment)]

    return sentiment_label, avg_sentiment


# Function to fetch latest bills
def get_latest_bills(num_bills):
    url = f"https://api.congress.gov/v3/bill/119?sort=updateDate+desc&api_key={api}"
    params = {'limit': num_bills, 'fromDateTime': '2025-03-10T00:00:00Z', 'toDateTime': '2025-05-15T00:00:00Z'}
    response = requests.get(url, params=params)
    return response.json()


# Function to get bill details
def get_bill_details(congress, bill_type, bill_number):
    url = f"https://api.congress.gov/v3/bill/{congress}/{bill_type}/{bill_number}/text?api_key={api}"
    response = requests.get(url)
    data = response.json()

    bill_data = data.get("bill", {})
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


# Function to predict likelihood of bill passing
def predict_likelihood(bill_data):
    score = 0

    if len(bill_data.get("sponsors", [])) >= 5:
        score += 2
    if any("R" in s or "D" in s for s in bill_data.get("sponsors", [])):
        score += 3

    latest_action = bill_data.get("latest_action", "").lower()
    if "passed house" in latest_action:
        score += 4
    if "passed senate" in latest_action:
        score += 5
    if "vetoed" in latest_action or "failed" in latest_action:
        score -= 5

    important_committees = ["Finance", "Appropriations", "Ways and Means"]
    if any(comm in bill_data.get("committees", "") for comm in important_committees):
        score += 2

    bill_type = bill_data.get("bill_type", "").upper()
    if bill_type in ["HR", "S"]:
        score += 2
    elif bill_type in ["HRES", "SRES"]:
        score -= 2

    if score >= 7:
        return "High"
    elif score >= 5:
        return "Moderate"
    elif score >= 2:
        return "Low"
    else:
        return "Very Low"


# Industry Mapping
def map_to_industry(subjects, title=""):
    INDUSTRY_KEYWORDS = {
        "Technology": ["AI", "Artificial Intelligence", "Semiconductor", "Cybersecurity"],
        "Healthcare": ["Medicare", "Drug", "Pharmaceutical", "Insurance"],
        "Energy": ["Renewable", "Oil", "Gas", "Solar", "Wind"],
        "Finance": ["Tax", "Regulation", "Crypto", "Banking"]
    }
    matched_industries = set()
    for subject in subjects:
        for industry, keywords in INDUSTRY_KEYWORDS.items():
            if any(keyword.lower() in subject.lower() for keyword in keywords):
                matched_industries.add(industry)
    if not matched_industries:
        for industry, keywords in INDUSTRY_KEYWORDS.items():
            if any(keyword.lower() in title.lower() for keyword in keywords):
                matched_industries.add(industry)
    return list(matched_industries)


# Main Execution
def main():
    bills = get_latest_bills(3)
    for bill in bills['bills']:
        title = bill["title"]
        congress = bill['congress']
        bill_type = bill['type']
        bill_number = bill['number']

        bill_data = get_bill_details(congress, bill_type, bill_number)
        likelihood = predict_likelihood(bill_data)
        industries = map_to_industry(bill_data.get("subjects", []), title=bill_data["title"])

        print(
            f"\nBill Summary\n Title: {title}\n Bill ID: {bill_type} {bill_number}\n Congress: {congress}\n Likelihood of Passage: {likelihood}\n Affected Industries: {industries if industries else 'Unknown'}")

        link = f"https://www.congress.gov/{congress}/bills/{bill_type.lower()}{bill_number}/BILLS-{congress}{bill_type.lower()}{bill_number}eh.xml"
        text = extract_text_from_html_url(link)
        if text:
            sentiment, scores = analyze_sentiment_chunks(text)
            print(f" Sentiment: {sentiment}")


if __name__ == "__main__":
    main()
