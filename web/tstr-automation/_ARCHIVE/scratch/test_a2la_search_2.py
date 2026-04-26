import requests
from bs4 import BeautifulSoup
import re

# Searching for Mechanical testing which includes materials
search_url = "https://customer.a2la.org/index.cfm?event=directory.index"

# Test 1: Just Search
print("Test 1: search=Mechanical")
data = {
    "search": "Mechanical",
    "btnSearch": "Search"
}
response = requests.post(search_url, data=data)
print(f"Status: {response.status_code}, Length: {len(response.text)}")
soup = BeautifulSoup(response.text, 'html.parser')
links = soup.find_all('a', href=re.compile(r'labPID=', re.I))
print(f"Found {len(links)} links")

# Test 2: Search with Category
print("\nTest 2: Mechanical Category")
data = {
    "search": "",
    "category": "Mechanical",
    "btnSearch": "Search"
}
response = requests.post(search_url, data=data)
print(f"Status: {response.status_code}, Length: {len(response.text)}")
soup = BeautifulSoup(response.text, 'html.parser')
links = soup.find_all('a', href=re.compile(r'labPID=', re.I))
print(f"Found {len(links)} links")

