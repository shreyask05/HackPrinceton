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


def get_bill_details(congress, bill_type,bill_number):
    print("Getting bill details")
    url = f"https://api.congress.gov/v3/bill/{congress}/{bill_type}/{bill_number}?api_key={api}"
    response = requests.get(url)
    #print(json.dumps(response.json(), indent=4))
    data = response.json()
    return {
        "title": data.get("title"),
        "bill_type": bill_type,
        "bill_number": bill_number,
        "congress": congress,
        "sponsors": [s.get("name", "") for s in data.get("sponsors", [])],
        "latest_action": data.get("latestAction", {}).get("text", "N/A"),
        "committees": [c.get("name", "") for c in data.get("committees", [])],
        "subjects": [s.get("name", "") for s in data.get("subjects", [])],
    }


def get_bill_subject(congress, bill_type,bill_number):
    print("Getting bill subject")
    url = f"https://api.congress.gov/v3/bill/{congress}/{bill_type}/{bill_number}/subjects?api_key={api}"
    response = requests.get(url)
    #print(json.dumps(response.json(), indent=4))
    return response.json()


def get_bill_summary(congress, bill_type,bill_number):
    print("Getting bill summary")
    url = f"https://api.congress.gov/v3/bill/{congress}/{bill_type}/{bill_number}/summaries?api_key={api}"
    response = requests.get(url)
    #print(json.dumps(response.json(), indent=4))
    return response.json()


def predict_likelihood(bill_data):
    """
    Predicts the likelihood of a bill passing based on predefined rules.
    """
    score = 0

    # 1️⃣ Check Sponsorship
    sponsors = bill_data.get("sponsors", [])
    if len(sponsors) >= 5:  # More sponsors = more support
        score += 2
    if any("R" in s or "D" in s for s in sponsors):  # Bipartisan support
        score += 3

    # 2️⃣ Check Bill Progress
    latest_action = bill_data.get("latest_action", "").lower()
    if "passed house" in latest_action:
        score += 4
    if "passed senate" in latest_action:
        score += 5
    if "vetoed" in latest_action or "failed" in latest_action:
        score -= 5

    # 3️⃣ Committee Assignment (Bills in powerful committees are more likely to pass)
    important_committees = ["Finance", "Appropriations", "Ways and Means"]
    if any(comm in bill_data.get("committees", "") for comm in important_committees):
        score += 2

    # 4️⃣ Bill Type Influence
    bill_type = bill_data.get("bill_type", "").upper()
    if bill_type in ["HR", "S"]:  # House and Senate bills (more impactful)
        score += 2
    elif bill_type in ["HRES", "SRES"]:  # Resolutions (often symbolic)
        score -= 2

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
def map_to_industry(subjects):
    """
    Maps bill subjects to related industries.
    """
    matched_industries = set()
    for subject in subjects:
        for industry, keywords in INDUSTRY_KEYWORDS.items():
            if any(keyword.lower() in subject.lower() for keyword in keywords):
                matched_industries.add(industry)
    return list(matched_industries)

def main():
    print()
    #testing endpoints individually
    '''
    get_latest_bills(2)
    get_bill_details(117,'hr',3076)
    get_bill_subject(117, 'hr', 3076)
    get_bill_summary(117,'hr',3076)
    '''

    # testing concurrent calls / data propagation
    '''
    bill_details = []
    bills = get_latest_bills(1)
    for bill in bills['bills']:
        congress = bill['congress']
        bill_type = bill['type']
        bill_number = bill['number']
        bill_details.append((congress, bill_type, bill_number))

    print(bill_details)

    for tup in bill_details:
        c,typ,num = tup
        get_bill_details(c,typ,num)
    '''

    #testing score system
    bills = get_latest_bills(1)
    for bill in bills['bills']:
        congress = bill['congress']
        bill_type = bill['type']
        bill_number = bill['number']

        bill_data = get_bill_details(congress, bill_type, bill_number)
        if not bill_data:
            continue

        likelihood = predict_likelihood(bill_data)
        industries = map_to_industry(bill_data.get("subjects", []))

        # Print results
        print("\n🔹 Bill Summary 🔹")
        print(f"📜 Title: {bill_data['title']}")
        print(f"📌 Bill ID: {bill_type} {bill_number}")
        print(f"🏛️ Congress: {congress}")
        print(f"🔍 Likelihood of Passage: {likelihood}")
        print(f"🏭 Affected Industries: {industries if industries else 'Unknown'}")
        print("-" * 50)

if __name__ == "__main__":
    main()





