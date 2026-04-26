import requests
from bs4 import BeautifulSoup
import re

# Use a likely valid PID (first one in a2la_pids_final.txt)
url = "https://customer.a2la.org/index.cfm?event=directory.detail&labPID=00B1A7E9-867B-46D7-90C1-72A09B59F85F"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Check for organization name field
org_name_field = soup.find('label', string=re.compile(r'Organization Name:', re.I))
print(f"Org Name field found: {org_name_field is not None}")
if org_name_field:
    org_name_p = org_name_field.find_next('p', class_='form-control-static')
    if org_name_p:
        print(f"Business Name: {org_name_p.get_text(strip=True)}")

# Check for "Apologies" in title
title = soup.find('title')
if title:
    print(f"Title: {title.get_text(strip=True)}")

