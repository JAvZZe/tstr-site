import requests
from bs4 import BeautifulSoup
import re

# Searching for Mechanical testing which includes materials
search_url = "https://customer.a2la.org/index.cfm?event=directory.index"

# Test 5: Try searching by Certificate Number which usually works
print("Test 5: keyword=1761.01 (Element Materials Technology)")
data = {
    "keyword": "1761.01",
    "btnSearch": "Search"
}
response = requests.post(search_url, data=data)
print(f"Status: {response.status_code}, Length: {len(response.text)}")
soup = BeautifulSoup(response.text, 'html.parser')
links = soup.find_all('a', href=re.compile(r'labPID=', re.I))
print(f"Found {len(links)} links")
for link in links:
    print(f"  {link.get('href')}")
    print(f"  {link.get_text(strip=True)}")

