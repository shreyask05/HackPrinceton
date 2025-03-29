import json
import os
from bs4 import BeautifulSoup
import requests

api = os.getenv("CONGRESS_API_KEY")
session = requests.Session()

print("Getting bill text")
#url = f"https://api.congress.gov/v3/bill/119/sres/148/text?api_key={api}"
url = "https://www.congress.gov/bill/119th-congress/senate-resolution/148/text"
html = session.get(url).text
response = requests.get(url)
soup = BeautifulSoup(html, "html.parser")
text = soup.getText()
print(f"text: {text}")
session.close()