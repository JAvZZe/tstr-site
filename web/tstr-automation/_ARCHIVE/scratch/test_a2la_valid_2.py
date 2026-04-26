import requests
from bs4 import BeautifulSoup
import re

pids = [
    "031C4AF0-B0DA-4AD7-BCDE-940DEECDE25E",
    "07745F0D-416C-4BB1-9CAC-3588866196F3",
    "1D5CD78D-2A8B-4EC2-AFA8-B9C80F0AACAF"
]

for pid in pids:
    url = f"https://customer.a2la.org/index.cfm?event=directory.detail&labPID={pid}"
    print(f"Testing {pid}...")
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    title = soup.find('title')
    title_text = title.get_text(strip=True) if title else "NO TITLE"
    print(f"  Title: {title_text}")
    
    org_name_field = soup.find('label', string=re.compile(r'Organization Name:', re.I))
    print(f"  Org Name field found: {org_name_field is not None}")
    if org_name_field:
        org_name_p = org_name_field.find_next('p', class_='form-control-static')
        if org_name_p:
            print(f"  Business Name: {org_name_p.get_text(strip=True)}")
    print("-" * 20)

