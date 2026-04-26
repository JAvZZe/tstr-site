import requests
from bs4 import BeautifulSoup
import re

# Searching for Mechanical testing which includes materials
search_url = "https://customer.a2la.org/index.cfm?event=directory.search"

# Test 4: Try the .search event instead of .index or .detail
print("Test 4: event=directory.search")
data = {
    "keyword": "Mechanical",
    "btnSearch": "Search"
}
response = requests.post(search_url, data=data)
print(f"Status: {response.status_code}, Length: {len(response.text)}")
soup = BeautifulSoup(response.text, 'html.parser')
links = soup.find_all('a', href=re.compile(r'labPID=', re.I))
print(f"Found {len(links)} links")
for link in links[:5]:
    print(f"  {link.get('href')}")
    print(f"  {link.get_text(strip=True)}")

