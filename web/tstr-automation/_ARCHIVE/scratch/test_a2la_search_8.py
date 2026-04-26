import requests

# Searching for Mechanical testing which includes materials
search_url = "https://customer.a2la.org/index.cfm?event=directory.search"

# Try with a real session and proper form data as the criteria
session = requests.Session()
session.get("https://customer.a2la.org/index.cfm?event=directory.index") # Get cookies

headers = {
    "X-Requested-With": "XMLHttpRequest"
}

# The JS says { criteria: $frmSearch.serializeForm() }
# We'll try common form fields from directory.index
payload = {
    "criteria": {
        "keyword": "Mechanical",
        "programIds": "",
        "state": "",
        "country": "",
        "category": ""
    }
}

print("Test 8: POST to directory.search with criteria dict")
response = session.post(search_url, json=payload, headers=headers)
print(f"Status: {response.status_code}")
print(f"Content Length: {len(response.text)}")
print(response.text[:500])

