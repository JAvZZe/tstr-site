import requests
import json

search_url = "https://customer.a2la.org/index.cfm?event=directory.search"
session = requests.Session()
session.get("https://customer.a2la.org/index.cfm?event=directory.index")

headers = {
    "X-Requested-With": "XMLHttpRequest",
    "Content-Type": "application/json; charset=utf-8",
}

# The JS says $cbox.postJSON('directory.search', { criteria:$frmSearch.serializeForm() })
# If $cbox is initialized with 'index.cfm?event=__controller_name.__event_name&__query_string'
# then postJSON('directory.search', ...) will call getLink('directory.search')
# which produces 'index.cfm?event=directory.search'

payload = {
    "criteria": "keyword=Mechanical"
}

print("Test 12: POST to directory.search with exact payload from code analysis")
response = session.post(search_url, data=json.dumps(payload), headers=headers)
print(f"Status: {response.status_code}")
print(f"Content-Type: {response.headers.get('Content-Type')}")

# Sometimes if it's not JSON, it might still have the results in the body but wrapped in HTML if an error occurred
# Or it might be a partial fragment.
if "Apologies" in response.text:
    print("Detected 'Apologies' error page.")
else:
    print(f"Response length: {len(response.text)}")
    print(response.text[:1000])

