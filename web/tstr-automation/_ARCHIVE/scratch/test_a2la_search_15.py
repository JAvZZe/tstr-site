import requests
import json
from bs4 import BeautifulSoup
import re

search_url = "https://customer.a2la.org/index.cfm/directory/search"
session = requests.Session()
session.get("https://customer.a2la.org/index.cfm?event=directory.index")

headers = {
    "X-Requested-With": "XMLHttpRequest",
    "Content-Type": "application/json; charset=utf-8",
}

payload = {
    "criteria": "keyword=Mechanical"
}

print("Test 15: POST to /index.cfm/directory/search and look for results")
response = session.post(search_url, data=json.dumps(payload), headers=headers)
print(f"Status: {response.status_code}")

soup = BeautifulSoup(response.text, 'html.parser')
links = soup.find_all('a', href=re.compile(r'labPID=', re.I))
print(f"Found {len(links)} links with labPID")

for link in links[:10]:
    print(f"  {link.get('href')} - {link.get_text(strip=True)}")

