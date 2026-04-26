import requests
import json

search_url = "https://customer.a2la.org/index.cfm?event=directory.search"
session = requests.Session()
session.get("https://customer.a2la.org/index.cfm?event=directory.index")

headers = {
    "X-Requested-With": "XMLHttpRequest",
    "Content-Type": "application/json; charset=utf-8",
    "Accept": "application/json, text/javascript, */*; q=0.01"
}

# criteria: $frmSearch.serializeForm()
# serializeForm() in jQuery usually produces "key=value&key2=value2"

payload = {
    "criteria": "keyword=Mechanical"
}

print("Test 11: POST to directory.search with correct headers and JSON payload")
response = session.post(search_url, data=json.dumps(payload), headers=headers)
print(f"Status: {response.status_code}")
try:
    data = response.json()
    print(f"Response is JSON, length: {len(data) if isinstance(data, list) else 'N/A'}")
    if isinstance(data, list) and len(data) > 0:
        print(f"First result: {data[0]}")
except Exception as e:
    print(f"Response is not JSON: {e}")
    print(response.text[:500])

