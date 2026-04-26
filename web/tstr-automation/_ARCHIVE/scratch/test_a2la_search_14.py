import requests
import json

# Try another search url pattern
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

print("Test 14: POST to /index.cfm/directory/search")
response = session.post(search_url, data=json.dumps(payload), headers=headers)
print(f"Status: {response.status_code}")
if "Apologies" in response.text:
    print("Detected 'Apologies' error page.")
else:
    print(f"Response length: {len(response.text)}")
    print(response.text[:500])

