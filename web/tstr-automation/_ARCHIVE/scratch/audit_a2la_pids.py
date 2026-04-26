import requests
from bs4 import BeautifulSoup
import re
import time

seed_pids_file = 'web/tstr-automation/scrapers/a2la/a2la_pids_final.txt'
valid_pids_file = 'web/tstr-automation/scrapers/a2la/a2la_pids_valid.txt'

with open(seed_pids_file, 'r') as f:
    pids = [line.strip() for line in f if line.strip()]

print(f"Auditing {len(pids)} PIDs...")

valid_pids = []
for i, pid in enumerate(pids):
    url = f"https://customer.a2la.org/index.cfm?event=directory.detail&labPID={pid}"
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        error_h2 = soup.find('h2', class_='text-danger', string=re.compile(r'An Unexpected Error Occured', re.I))
        title = soup.find('title')
        is_error = error_h2 or (title and 'Apologies' in title.get_text())
        
        if not is_error:
            valid_pids.append(pid)
            print(f"[{i+1}/{len(pids)}] VALID: {pid}")
        else:
            print(f"[{i+1}/{len(pids)}] ERROR: {pid}")
            
    except Exception as e:
        print(f"[{i+1}/{len(pids)}] FAILED to fetch {pid}: {e}")
    
    # Rate limit
    time.sleep(1)

print(f"Audit complete. Found {len(valid_pids)} valid PIDs.")

with open(valid_pids_file, 'w') as f:
    for pid in valid_pids:
        f.write(f"{pid}\n")

print(f"Valid PIDs saved to {valid_pids_file}")
