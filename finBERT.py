# import requests
# from bs4 import BeautifulSoup

# def extract_text_from_html_url(url):
#     print(f"Fetching bill from: {url}")
#     response = requests.get(url)
    
#     if not response.ok:
#         print("Failed to fetch the bill text.")
#         return None
    
#     soup = BeautifulSoup(response.text, "html.parser")

#     # Remove script and style tags
#     for tag in soup(["script", "style"]):
#         tag.decompose()

#     clean_text = soup.get_text(separator=' ', strip=True)
#     return clean_text


# from transformers import AutoTokenizer, AutoModelForSequenceClassification
# import torch
# import numpy as np

# tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
# model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")

# def analyze_sentiment_chunks(text, chunk_size=512):
#     tokens = tokenizer.tokenize(text)
#     chunks = [' '.join(tokens[i:i+chunk_size]) for i in range(0, len(tokens), chunk_size)]

#     sentiments = []
#     for chunk in chunks:
#         inputs = tokenizer(chunk, return_tensors="pt", truncation=True, max_length=512)
#         outputs = model(**inputs)
#         probs = torch.nn.functional.softmax(outputs.logits, dim=1)
#         sentiments.append(probs.detach().numpy())

#     avg_sentiment = np.mean(sentiments, axis=0)
#     label_map = {0: "negative", 1: "neutral", 2: "positive"}
#     sentiment_label = label_map[np.argmax(avg_sentiment)]

#     return sentiment_label, avg_sentiment


# url = "https://www.congress.gov/117/bills/hr3076/BILLS-117hr3076enr.htm"
# text = extract_text_from_html_url(url)

# if text:
#     sentiment, scores = analyze_sentiment_chunks(text)
#     print(f"Sentiment: {sentiment}")
#     print(f"Scores: {scores}")

import requests
from bs4 import BeautifulSoup
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import numpy as np

# Load FinBERT once
tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")

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

# Function to analyze long text in chunks using FinBERT
def analyze_sentiment_chunks(text, chunk_size=1024):
    words = text.split()
    chunks = [' '.join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]

    sentiments = []
    for i, chunk in enumerate(chunks):
        inputs = tokenizer(chunk, return_tensors="pt", truncation=True, max_length=512)
        outputs = model(**inputs)
        probs = torch.nn.functional.softmax(outputs.logits, dim=1)
        sentiments.append(probs.detach().numpy())

    avg_sentiment = np.mean(sentiments, axis=0).flatten()
    label_map = {0: "negative", 1: "neutral", 2: "positive"}
    sentiment_label = label_map[np.argmax(avg_sentiment)]

    return sentiment_label, avg_sentiment

# MAIN EXECUTION BLOCK
if __name__ == "__main__":
    # url = "https://www.congress.gov/119/bills/hr313/BILLS-119hr313eh.xml"  # Replace with your own bill URL
    url = "https://www.congress.gov/119/bills/hjres75/BILLS-119hjres75eh.xml"
    text = extract_text_from_html_url(url)

    if text:
        sentiment, scores = analyze_sentiment_chunks(text)
        print(f"\nSentiment: {sentiment}")
        print(f"Scores → Negative: {scores[0]:.4f}, Neutral: {scores[1]:.4f}, Positive: {scores[2]:.4f}")
    else:
        print("Skipping sentiment analysis due to missing or invalid bill text.")
