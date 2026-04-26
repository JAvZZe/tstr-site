import requests
from bs4 import BeautifulSoup
import re

url = "https://customer.a2la.org/index.cfm?event=directory.detail&labPID=12A618F6-8114-4994-A522-26D9F1AA0986"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Check for "An Unexpected Error Occured"
error_h2 = soup.find('h2', class_='text-danger', string=re.compile(r'An Unexpected Error Occured', re.I))
print(f"Error H2 found: {error_h2 is not None}")
if error_h2:
    print(f"Text: {error_h2.get_text(strip=True)}")

# Check for "Apologies" in title
title = soup.find('title')
if title:
    print(f"Title: {title.get_text(strip=True)}")
    print(f"Apologies in title: {'Apologies' in title.get_text()}")

# Check for organization name field (which should NOT be present in error page)
org_name_field = soup.find('label', string=re.compile(r'Organization Name:', re.I))
print(f"Org Name field found: {org_name_field is not None}")

