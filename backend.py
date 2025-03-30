import requests
from bs4 import BeautifulSoup
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import numpy as np
import os
import google.generativeai as genai

# Load FinBERT once
tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")

# Congress API Key
api = os.getenv("CONGRESS_API_KEY")

# GEMINI: 1Configure API key
api2 = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api2)
# GEMINI: 2Load the model
gen_model = genai.GenerativeModel("gemini-1.5-pro")


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



# GEMINI: 4Construct prompt with bill text
def generate_bill_analysis(congress, bill_number, bill_text):
    prompt = f"""
For bill number {bill_number}, Congress {congress}, perform the following tasks:

1. Rate the sentiment with respect to the stock market as positive, negative, or neutral (output just the result)
2. For the rating, give the confidence level of the rating in percentage (output just the percentage)
3. Summarize the bill in plain language in 100 words.
4. Assess its potential financial implications and justify reasoning based on the content rating in 100 words.

Here is the full text of the bill:
\"\"\"
{bill_text}
\"\"\"
"""
    return gen_model.generate_content(prompt).text


#____________________________MAIN__START_________________________
# Main Execution
# def main():
#     bills = get_latest_bills(3)
#     for bill in bills['bills']:
#         title = bill["title"]
#         congress = bill['congress']
#         bill_type = bill['type']
#         bill_number = bill['number']

#         bill_data = get_bill_details(congress, bill_type, bill_number)
#         likelihood = predict_likelihood(bill_data)
#         industries = map_to_industry(bill_data.get("subjects", []), title=bill_data["title"])

#         print(
#             f"\nBill Summary\n Title: {title}\n Bill ID: {bill_type} {bill_number}\n Congress: {congress}\n Likelihood of Passage: {likelihood}\n Affected Industries: {industries if industries else 'Unknown'}")

#         link = f"https://www.congress.gov/{congress}/bills/{bill_type.lower()}{bill_number}/BILLS-{congress}{bill_type.lower()}{bill_number}eh.xml"
#         text = extract_text_from_html_url(link)
#         if text:
#             bill_text = text[:8000] 
#             sentiment, scores = analyze_sentiment_chunks(bill_text)
#             # print(f" finBERK Sentiment: {sentiment}")
#             label_map = {"negative": 0, "neutral": 1, "positive": 2}
#             index = label_map[sentiment]
#             score = scores[index]
#             print(f"\nfinBERK Sentiment: {sentiment}")
#             print(f"Score: {score:.4f}")

#             # Store both sentiment and score
#             finBERK_sentiment_result = (sentiment, score)


#             analysis = generate_bill_analysis(congress=congress, bill_number=bill_number, bill_text=bill_text)
#             print(analysis)
#         else:
#             print(f"Bill text unavailable for {bill_type} {bill_number}, skipping sentiment analysis.")

#         # if bill_text:
#         #     sentiment2, scores = analyze_sentiment_chunks(bill_text)
#         #     print(f" finBERK Sentiment: {sentiment2}")
#         #     analysis = generate_bill_analysis(congress=119, bill_number=1069, bill_text=bill_text)
#____________________________MAIN__END_________________________


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
            bill_text = text[:8000]

            # --- FinBERT Sentiment ---
            sentiment, scores = analyze_sentiment_chunks(bill_text)
            label_map = {"negative": 0, "neutral": 1, "positive": 2}
            reverse_label_map = {v: k for k, v in label_map.items()}
            index = label_map[sentiment]
            score = scores[index]
            print(f"\nfinBERK Sentiment: {sentiment}")
            print(f"Score: {score:.4f}")
            finBERK_sentiment_result = (sentiment, score)

            # --- Gemini Sentiment ---
            analysis = generate_bill_analysis(congress=congress, bill_number=bill_number, bill_text=bill_text)
            print(analysis)

            lines = analysis.strip().split("\n")
            gemini_sentiment = None
            gemini_score = None

            for line in lines:
                if line.lower().startswith("1."):
                    gemini_sentiment = line.split(".")[1].strip().lower()
                elif line.lower().startswith("2."):
                    percent_text = line.split(".")[1].strip().replace("%", "")
                    try:
                        gemini_score = float(percent_text) / 100
                    except ValueError:
                        gemini_score = None
                elif line.lower().startswith("3."):
                    summary = line.split("3.", 1)[1].strip()
                elif line.lower().startswith("4."):
                    insight = line.split("4.", 1)[1].strip()

            if gemini_sentiment is not None and gemini_score is not None:
                print(f"\nGemini Sentiment: {gemini_sentiment}")
                print(f"Gemini Confidence: {gemini_score:.4f}")

                # Convert sentiments to index
                fin_sent = finBERK_sentiment_result[0].lower()
                fin_score = finBERK_sentiment_result[1]
                fin_label_idx = label_map.get(fin_sent, 1)
                gemini_label_idx = label_map.get(gemini_sentiment, 1)

                # --- Weighted hybrid sentiment index ---
                hybrid_position = 0.3 * fin_label_idx + 0.7 * gemini_label_idx
                hybrid_index = int(round(hybrid_position))
                hybrid_sentiment = reverse_label_map[hybrid_index]

                # --- Weighted hybrid confidence ---
                hybrid_confidence = round(0.3 * fin_score + 0.7 * gemini_score, 4)

                print(f"\n✅ Hybrid Sentiment: {hybrid_sentiment.capitalize()}")
                print(f"📊 Hybrid Confidence: {hybrid_confidence:.4f}")
                print(f"\n📝 Text Summary:\n{summary}")
                print(f"\n💡 Financial Insight:\n{insight}")
            else:
                print("⚠️ Could not extract Gemini sentiment or score.")
        else:
            print(f"Bill text unavailable for {bill_type} {bill_number}, skipping sentiment analysis.")

if __name__ == "__main__":
    main()
