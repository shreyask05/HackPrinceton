import os
import requests
import json

api = os.getenv("CONGRESS_API_KEY")

def get_latest_bills(num_bills):
    print("Getting latest bills")
    url = f"https://api.congress.gov/v3/bill?api_key={api}"
    params = {'limit': num_bills}
    response = requests.get(url, params=params)
    print(json.dumps(response.json(), indent=4))
    return response.json()


def get_bill_details(congress, bill_type,bill_number):
    print("Getting bill details")
    url = f"https://api.congress.gov/v3/bill/{congress}/{bill_type}/{bill_number}?api_key={api}"
    response = requests.get(url)
    print(json.dumps(response.json(), indent=4))


def get_bill_subject(congress, bill_type,bill_number):
    print("Getting bill subject")
    url = f"https://api.congress.gov/v3/bill/{congress}/{bill_type}/{bill_number}/subjects?api_key={api}"
    response = requests.get(url)
    print(json.dumps(response.json(), indent=4))


def get_bill_summary(congress, bill_type,bill_number):
    print("Getting bill summary")
    url = f"https://api.congress.gov/v3/bill/{congress}/{bill_type}/{bill_number}/summaries?api_key={api}"
    response = requests.get(url)
    print(json.dumps(response.json(), indent=4))


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

if __name__ == "__main__":
    main()





