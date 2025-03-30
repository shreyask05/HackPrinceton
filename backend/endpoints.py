import os
import requests
import json

api = os.getenv("CONGRESS_API_KEY")


def get_latest_bills(num_bills):
    print("Getting latest bills")
    url = f"https://api.congress.gov/v3/bill?api_key={api}"
    params = {'limit': num_bills}
    response = requests.get(url, params=params)
    #print(json.dumps(response.json(), indent=4))
    return response.json()


def get_bill_details(congress, bill_type, bill_number):
    print("Getting bill details")
    url = f"https://api.congress.gov/v3/bill/{congress}/{bill_type}/{bill_number}?api_key={api}"
    response = requests.get(url)
    data = response.json()
    return {
        "title": data.get("title", "Unknown"),
        "bill_type": bill_type,
        "bill_number": bill_number,
        "congress": congress,
        "sponsors": [s.get("name", "") for s in data.get("sponsors", [])],
        "latest_action": data.get("latestAction", {}).get("text", "N/A"),
        "committees": [c.get("name", "") for c in data.get("committees", [])],
        "subjects": [s.get("name", "") for s in data.get("subjects", [])],
    }


def get_bill_text(congress, bill_type, bill_number):
    print("Getting bill text")
    url = f"https://api.congress.gov/v3/bill/{congress}/{bill_type}/{bill_number}/text?api_key={api}"
    response = requests.get(url)
    print(json.dumps(response.json(), indent=4))


def predict_likelihood(bill_data):
    """
    Predicts the likelihood of a bill passing based on predefined rules.
    """
    score = 0

    # Check Sponsorship
    sponsors = bill_data.get("sponsors", [])
    if len(sponsors) >= 5:
        score += 2
        print("+2")
    if any("R" in s or "D" in s for s in sponsors):
        score += 3
        print("+3")

    # Check Bill Progress
    latest_action = bill_data.get("latest_action", "").lower()
    if "passed house" in latest_action:
        score += 4
        print("+4")
    if "passed senate" in latest_action:
        score += 5
        print("+5")
    if "vetoed" in latest_action or "failed" in latest_action:
        score -= 5
        print("-5")

    # Committee Assignment
    important_committees = ["Finance", "Appropriations", "Ways and Means"]
    if any(comm in bill_data.get("committees", "") for comm in important_committees):
        score += 2
        print("+2")

    # Bill Type Influence
    bill_type = bill_data.get("bill_type", "").upper()
    if bill_type in ["HR", "S"]:
        score += 2
        print("+2")
    elif bill_type in ["HRES", "SRES"]:
        score -= 2
        print("-2")

    print(f"score is {score}")
    # Assign Likelihood Based on Score
    if score >= 7:
        return "High"
    elif score >= 3:
        return "Moderate"
    else:
        return "Low"


INDUSTRY_KEYWORDS = {
    "Technology": ["AI", "Artificial Intelligence", "Semiconductor", "Cybersecurity"],
    "Healthcare": ["Medicare", "Drug", "Pharmaceutical", "Insurance"],
    "Energy": ["Renewable", "Oil", "Gas", "Solar", "Wind"],
    "Finance": ["Tax", "Regulation", "Crypto", "Banking"]
}


def map_to_industry(subjects, title=""):
    """
    Maps bill subjects to related industries.
    Falls back to title keywords if subjects are unavailable.
    """
    matched_industries = set()

    # Check subjects first
    for subject in subjects:
        for industry, keywords in INDUSTRY_KEYWORDS.items():
            if any(keyword.lower() in subject.lower() for keyword in keywords):
                matched_industries.add(industry)

    # Fallback: Check title if no subjects match
    if not matched_industries:
        for industry, keywords in INDUSTRY_KEYWORDS.items():
            if any(keyword.lower() in title.lower() for keyword in keywords):
                matched_industries.add(industry)

    return list(matched_industries)


def main():
    print()

    # Fetch latest bills and analyze them
    bills = get_latest_bills(1)

    for bill in bills['bills']:
        #print(bill)
        title = bill["title"]
        congress = bill['congress']
        bill_type = bill['type']
        bill_number = bill['number']

        # Get detailed data about the bill
        bill_data = get_bill_details(congress, bill_type, bill_number)
        print(bill_data)
        if not bill_data:
            print(f"Skipping Bill {bill_number} due to missing details.")
            continue

        # Predict likelihood of passage
        likelihood = predict_likelihood(bill_data)

        # Map to industries (fallback to title if no subjects)
        industries = map_to_industry(bill_data.get("subjects", []), title=bill_data["title"])

        # Print results
        print("\nBill Summary")
        print(f" Title: {title}")
        print(f" Bill ID: {bill_type} {bill_number}")
        print(f" Congress: {congress}")
        print(f" Likelihood of Passage: {likelihood}")
        print(f" Affected Industries: {industries if industries else 'Unknown'}")
        print("-" * 50)


if __name__ == "__main__":
    main()
