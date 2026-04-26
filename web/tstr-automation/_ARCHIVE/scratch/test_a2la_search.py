import requests
from bs4 import BeautifulSoup
import re

# Searching for Mechanical testing which includes materials
search_url = "https://customer.a2la.org/index.cfm?event=directory.index"
data = {
    "search": "Mechanical",
    "btnSearch": "Search"
}

response = requests.post(search_url, data=data)
print(f"Status Code: {response.status_code}")
print(f"Content Length: {len(response.text)}")

soup = BeautifulSoup(response.text, 'html.parser')
# Look for lab detail links
links = soup.find_all('a', href=re.compile(r'labPID=', re.I))
print(f"Found {len(links)} links with labPID")

for link in links[:5]:
    print(f"Link: {link.get('href')}")
    print(f"Text: {link.get_text(strip=True)}")

