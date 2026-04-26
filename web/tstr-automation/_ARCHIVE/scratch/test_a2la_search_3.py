import requests
from bs4 import BeautifulSoup
import re

# Searching for Mechanical testing which includes materials
search_url = "https://customer.a2la.org/index.cfm?event=directory.index"

# Test 3: Search with data-name value "Mechanical Field of Testing"
print("Test 3: category=60")
data = {
    "search": "",
    "category": "60",
    "btnSearch": "Search"
}
response = requests.post(search_url, data=data)
print(f"Status: {response.status_code}, Length: {len(response.text)}")
soup = BeautifulSoup(response.text, 'html.parser')
links = soup.find_all('a', href=re.compile(r'labPID=', re.I))
print(f"Found {len(links)} links")
for link in links[:3]:
    print(f"  {link.get('href')}")

