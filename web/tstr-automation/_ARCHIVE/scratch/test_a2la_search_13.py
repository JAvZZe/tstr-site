import requests
import json

search_url = "https://customer.a2la.org/index.cfm?event=directory.search"
session = requests.Session()
session.get("https://customer.a2la.org/index.cfm?event=directory.index")

headers = {
    "X-Requested-With": "XMLHttpRequest",
    "Content-Type": "application/json; charset=utf-8",
}

# Try sending exactly what a form would send if it were JSON
payload = {
    "criteria": "keyword=Mechanical&programIds=&state=&country=&category="
}

print("Test 13: POST to directory.search with full criteria string")
response = session.post(search_url, data=json.dumps(payload), headers=headers)
print(f"Status: {response.status_code}")
if "Apologies" in response.text:
    print("Detected 'Apologies' error page.")
else:
    print(f"Response length: {len(response.text)}")
    print(response.text[:500])

