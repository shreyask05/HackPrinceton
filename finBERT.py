import requests
from bs4 import BeautifulSoup
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import numpy as np
from transformers import BertTokenizer, BertForSequenceClassification
from transformers import pipeline

# Load FinBERT once
tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")

# tokenizer = BertTokenizer.from_pretrained('yiyanghkust/finbert-tone')
# model = BertForSequenceClassification.from_pretrained('yiyanghkust/finbert-tone',num_labels=3)


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
    # url = "https://www.congress.gov/119/bills/hjres75/BILLS-119hjres75eh.xml"
    url = "https://www.congress.gov/117/plaws/publ167/PLAW-117publ167.htm" #CHIPS ACT
    #url = "https://www.congress.gov/119/bills/hr25/BILLS-119hr25ih.xml" #Scores → Negative: 0.0191, Neutral: 0.0790, Positive: 0.9020
    #url = "https://www.congress.gov/118/bills/hr25/BILLS-118hr25ih.xml" #Scores → Negative: 0.0190, Neutral: 0.0775, Positive: 0.9035
    text = extract_text_from_html_url(url)
    print(text)
    # text = "Pre-tax loss totaled euro 0.3 million, compared to a loss of euro 2.2 million in the first quarter of 2005."
    if text:
        sentiment, scores = analyze_sentiment_chunks(text)
        print(f"\nSentiment: {sentiment}")
        print(f"Scores → Negative: {scores[0]:.4f}, Neutral: {scores[1]:.4f}, Positive: {scores[2]:.4f}")
    else:
        print("Skipping sentiment analysis due to missing or invalid bill text.")

    # test_texts = [
    # "This bill provides tax credits to low-income families.",        # Probably positive
    # "This bill kills endangered species.",         # Should be negative
    # "This bill amends administrative procedures for departments."    # Likely neutral
    # ]

    # for t in test_texts:
    #     sentiment, scores = analyze_sentiment_chunks(t)
    #     print(f"Input: {t}\nSentiment: {sentiment}, Scores: {scores}\n")


#----------------------_SENTENCE_WISE_-------------------------------------
# import requests
# from bs4 import BeautifulSoup
# from transformers import AutoTokenizer, AutoModelForSequenceClassification
# import torch
# import numpy as np
# import nltk
# from nltk.tokenize import sent_tokenize
# from collections import Counter

# nltk.download("punkt")

# # Load FinBERT
# tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
# model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")

# # Optional: Extract bill text from a Congress.gov HTML page
# def extract_text_from_html_url(url):
#     print(f"📥 Fetching bill from: {url}")
#     response = requests.get(url)
    
#     if not response.ok or "We couldn't find that page" in response.text:
#         print("❌ Invalid or missing bill page.")
#         return None

#     soup = BeautifulSoup(response.text, "html.parser")
#     for tag in soup(["script", "style"]):
#         tag.decompose()
    
#     return soup.get_text(separator=' ', strip=True)

# # Sentence-level FinBERT sentiment analysis
# def analyze_sentences(sentences):
#     label_map = {0: "negative", 1: "neutral", 2: "positive"}
#     results = []

#     for i, sentence in enumerate(sentences):
#         inputs = tokenizer(sentence, return_tensors="pt", truncation=True, max_length=512)
#         outputs = model(**inputs)
#         probs = torch.nn.functional.softmax(outputs.logits, dim=1)
#         sentiment = label_map[np.argmax(probs.detach().numpy())]
#         confidence = np.max(probs.detach().numpy())

#         results.append({
#             "sentence": sentence,
#             "sentiment": sentiment,
#             "confidence": confidence
#         })

#     return results

# # Print summary of sentiment results
# def summarize_sentiment(results):
#     sentiments = [r["sentiment"] for r in results]
#     counts = Counter(sentiments)

#     print("\n🧾 Sentiment Summary:")
#     for s in ["positive", "neutral", "negative"]:
#         print(f"{s.title():<10}: {counts[s]}")

#     print("\n📌 Top Influential Sentences:")
#     for r in sorted(results, key=lambda x: x["confidence"], reverse=True)[:5]:
#         print(f"[{r['sentiment']}] ({r['confidence']:.2f}) → {r['sentence'][:120]}...")

# # MAIN
# if __name__ == "__main__":
#     #Option 1: Use real bill from Congress.gov
#     url = "https://www.congress.gov/117/bills/hr3076/BILLS-117hr3076enr.htm"
#     # url = "https://www.congress.gov/117/plaws/publ167/PLAW-117publ167.pdf"
#     text = extract_text_from_html_url(url)

#     # Option 2: Use example string for testing
#     # text = """
#     # This bill provides tax credits to low-income families. It eliminates consumer protections for mortgage borrowers.
#     # It amends administrative procedures for internal government reviews. It supports renewable energy development.
#     # """

#     if text:
#         sentences = sent_tokenize(text)
#         print(f"\n🧠 Analyzing {len(sentences)} sentences...")
#         results = analyze_sentences(sentences)
#         summarize_sentiment(results)
#     else:
#         print("⚠️ No text available to analyze.")
