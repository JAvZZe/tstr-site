import requests

# The JS uses $cbox.postJSON('directory.search', { criteria: $frmSearch.serializeForm() })
# serializeForm() usually produces a URL-encoded string or a dict.
# Given it's passed as an object to postJSON, it's likely a nested object.

search_url = "https://customer.a2la.org/index.cfm?event=directory.search"

# We need the X-Requested-With header for many ColdBox/jQuery AJAX calls
headers = {
    "X-Requested-With": "XMLHttpRequest",
    "Content-Type": "application/json"
}

payload = {
    "criteria": "keyword=Mechanical"
}

print("Test 7: POST to directory.search with criteria string")
response = requests.post(search_url, json=payload, headers=headers)
print(f"Status: {response.status_code}")
try:
    data = response.json()
    print(f"Response is JSON, length: {len(data) if isinstance(data, list) else 'N/A'}")
    if isinstance(data, list) and len(data) > 0:
        print(f"First result keys: {data[0].keys()}")
        print(f"First result labPID: {data[0].get('labPID')}")
except:
    print("Response is not JSON")
    print(response.text[:200])

