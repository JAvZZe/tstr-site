import requests
from bs4 import BeautifulSoup
import re

# Searching for Mechanical testing which includes materials
search_url = "https://customer.a2la.org/index.cfm?event=directory.index"

# Test 6: GET request with keyword
print("Test 6: GET event=directory.index&keyword=Mechanical")
url = "https://customer.a2la.org/index.cfm?event=directory.index&keyword=Mechanical"
response = requests.get(url)
print(f"Status: {response.status_code}, Length: {len(response.text)}")
soup = BeautifulSoup(response.text, 'html.parser')
links = soup.find_all('a', href=re.compile(r'labPID=', re.I))
print(f"Found {len(links)} links")

