import requests

search_url = "https://customer.a2la.org/index.cfm?event=directory.search"
session = requests.Session()
session.get("https://customer.a2la.org/index.cfm?event=directory.index")

headers = {
    "X-Requested-With": "XMLHttpRequest"
}

# The JS says:
# let search = function(onComplete){
#     $cbox.postJSON('directory.search', {
#             criteria:$frmSearch.serializeForm()
#         },

# If postJSON is a wrapper for $.post(url, data, callback, 'json'), 
# then data is { criteria: "..." }

payload = {
    "criteria": "keyword=Mechanical"
}

print("Test 10: POST to directory.search with criteria as form field")
response = session.post(search_url, data=payload, headers=headers)
print(f"Status: {response.status_code}")
try:
    print(response.text[:500])
except:
    pass

