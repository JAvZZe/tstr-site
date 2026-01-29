#!/usr/bin/env python3
"""
Test script to debug TNI LAMS search functionality
"""

import requests
from bs4 import BeautifulSoup
import time
import re

base_url = 'https://lams.nelac-institute.org'
search_url = f'{base_url}/search'

print("=" * 70)
print("TNI LAMS Search Test")
print("=" * 70)

# Create session
session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
})

try:
    # Fetch search page
    print("\n1. Fetching search page...")
    response = session.get(search_url)
    response.raise_for_status()
    print(f"   Status: {response.status_code}")

    soup = BeautifulSoup(response.content, 'html.parser')

    # Look for form fields
    print("\n2. Form fields found:")
    form_inputs = soup.find_all('input')
    for inp in form_inputs[:20]:  # Show first 20
        name = inp.get('name', 'N/A')
        input_type = inp.get('type', 'N/A')
        value = inp.get('value', '')
        if len(str(value)) > 50:
            value = str(value)[:50] + '...'
        print(f"   - {name} (type={input_type}): {value}")

    # Look for state dropdown
    print("\n3. Looking for state dropdown...")
    state_select = soup.find('select', {'name': lambda x: x and 'state' in x.lower()})
    if state_select:
        print(f"   Found: {state_select.get('name')}")
        options = state_select.find_all('option')
        print(f"   Options count: {len(options)}")
        print(f"   First 5 options: {[opt.get_text(strip=True) for opt in options[:5]]}")
    else:
        print("   Not found in standard <select> element")
        print("   Likely using Telerik RadComboBox (AJAX-based)")

    # Extract ViewState for form submission
    print("\n4. ViewState fields:")
    viewstate = soup.find('input', {'name': '__VIEWSTATE'})
    if viewstate:
        vs_value = viewstate.get('value', '')
        print(f"   __VIEWSTATE: {vs_value[:80]}... (length: {len(vs_value)})")

    viewstate_gen = soup.find('input', {'name': '__VIEWSTATEGENERATOR'})
    if viewstate_gen:
        print(f"   __VIEWSTATEGENERATOR: {viewstate_gen.get('value', 'N/A')}")

    event_validation = soup.find('input', {'name': '__EVENTVALIDATION'})
    if event_validation:
        ev_value = event_validation.get('value', '')
        print(f"   __EVENTVALIDATION: {ev_value[:80]}... (length: {len(ev_value)})")

    # Try a simple search
    print("\n5. Attempting search for Alabama labs...")

    form_data = {
        '__VIEWSTATE': viewstate.get('value', '') if viewstate else '',
        '__VIEWSTATEGENERATOR': viewstate_gen.get('value', '') if viewstate_gen else '',
        '__EVENTVALIDATION': event_validation.get('value', '') if event_validation else '',
        'ctl00$MainContent$rcbState': 'Alabama',
        'ctl00$MainContent$rcbState_ClientState': '',
        'ctl00$MainContent$rcbActive': 'Yes',
        'ctl00$MainContent$RadButton1': 'Search',
        '__EVENTTARGET': '',
        '__EVENTARGUMENT': ''
    }

    time.sleep(2)
    search_response = session.post(
        search_url,
        data=form_data,
        headers={'Referer': search_url}
    )
    print(f"   Search response status: {search_response.status_code}")

    # Parse results
    results_soup = BeautifulSoup(search_response.content, 'html.parser')

    # Look for results
    print("\n6. Looking for results...")

    # Try finding tables
    tables = results_soup.find_all('table')
    print(f"   Total tables found: {len(tables)}")

    for idx, table in enumerate(tables[:5]):
        rows = table.find_all('tr')
        if len(rows) > 1:
            print(f"\n   Table {idx + 1}: {len(rows)} rows")

            # Check headers
            headers = table.find_all('th')
            if headers:
                header_text = [h.get_text(strip=True) for h in headers]
                print(f"   Headers: {header_text}")

            # Show first data row
            data_rows = [r for r in rows if r.find_all('td')]
            if data_rows:
                first_row = data_rows[0]
                cells = first_row.find_all('td')
                cell_text = [c.get_text(strip=True)[:40] for c in cells[:5]]
                print(f"   First row: {cell_text}")

    # Look for Telerik RadGrid
    radgrid = results_soup.find('div', class_=re.compile(r'RadGrid'))
    if radgrid:
        print("\n   Found RadGrid element")

    # Check for "no results" message
    no_results = results_soup.find(text=lambda x: x and 'no' in x.lower() and 'found' in x.lower())
    if no_results:
        print(f"\n   No results message: {no_results}")

    # Save HTML for inspection
    print("\n7. Saving response HTML for inspection...")
    with open('/tmp/tni_search_results.html', 'w') as f:
        f.write(search_response.text)
    print("   Saved to: /tmp/tni_search_results.html")

    # Look for lab names
    print("\n8. Searching for lab-like content...")
    lab_pattern = re.compile(r'lab(?:oratory)?', re.IGNORECASE)
    potential_labs = results_soup.find_all(text=lab_pattern)
    if potential_labs:
        print(f"   Found {len(potential_labs)} text nodes containing 'lab'")
        for lab_text in potential_labs[:5]:
            print(f"   - {lab_text.strip()[:80]}")

except Exception as e:
    print(f"\nError: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)
print("Test Complete")
print("=" * 70)
