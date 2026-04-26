import requests

search_url = "https://customer.a2la.org/index.cfm?event=directory.search"
session = requests.Session()
session.get("https://customer.a2la.org/index.cfm?event=directory.index")

headers = {
    "X-Requested-With": "XMLHttpRequest",
    "Content-Type": "application/x-www-form-urlencoded"
}

# Try stringified criteria as a single form field
# ColdBox sometimes expects a form post with 'criteria' as a field containing the data
payload = "criteria=keyword%3DMechanical"

print("Test 9: POST to directory.search with form-encoded criteria string")
response = session.post(search_url, data=payload, headers=headers)
print(f"Status: {response.status_code}")
try:
    print(response.text[:500])
except:
    pass

