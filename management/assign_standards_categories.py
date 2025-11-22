#!/usr/bin/env python3
"""
Assign standards to their appropriate categories
"""

import requests
import json

SUPABASE_URL = "https://haimjeaetrsaauitrhfy.supabase.co"
SERVICE_ROLE_KEY = "sb_secret_zRN1fTFOYnN7cEbEIfAP7A_YrEKBfI2"

headers = {
    "apikey": SERVICE_ROLE_KEY,
    "Authorization": f"Bearer {SERVICE_ROLE_KEY}",
    "Content-Type": "application/json"
}

# Standard to category mapping based on their purpose
STANDARD_CATEGORY_MAP = {
    # Hydrogen/Oil & Gas standards
    'ISO 19880-3': 'oil-gas-testing',
    'SAE J2601': 'oil-gas-testing',
    'ISO 11114-1': 'oil-gas-testing',
    'ISO 14687': 'oil-gas-testing',
    'ISO 19881': 'oil-gas-testing',
    'API 571': 'oil-gas-testing',
    'API 580': 'oil-gas-testing',
    'ASTM D7042': 'oil-gas-testing',
    'NACE MR0175': 'oil-gas-testing',
    
    # Pharmaceutical standards
    'USP <797>': 'pharmaceutical-testing',
    'USP <71>': 'pharmaceutical-testing',
    'FDA 21 CFR Part 211': 'pharmaceutical-testing',
    'ICH Q7': 'pharmaceutical-testing',
    'ISO 13485': 'pharmaceutical-testing',
    
    # Biotech standards
    'ISO 10993': 'biotech-testing',
    'FDA 21 CFR Part 210': 'biotech-testing',
    'ISO 20387': 'biotech-testing',
    'USP <1046>': 'biotech-testing',
    'ISO 13408': 'biotech-testing',
    
    # Environmental standards
    'EPA Method 1664': 'environmental-testing',
    'ISO 14001': 'environmental-testing',
    'ASTM D5174': 'environmental-testing',
    'EPA Method 8260': 'environmental-testing',
    
    # Materials testing standards
    'ASTM E8': 'materials-testing',
    'ISO 6892-1': 'materials-testing',
    'ASTM D638': 'materials-testing',
    'ISO 148-1': 'materials-testing',
    'ASTM E3': 'materials-testing',
    
    # General/Multiple categories (ISO 17020, ISO 17025)
    'ISO 17020': None,  # Applicable to all
    'ISO 17025': None,  # Applicable to all
}

def get_data(table, filters=None):
    """Fetch data from Supabase"""
    url = f"{SUPABASE_URL}/rest/v1/{table}"
    params = {"select": "*"}
    if filters:
        params.update(filters)
    
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    return None

def update_standard(standard_id, category_id):
    """Update standard's category"""
    url = f"{SUPABASE_URL}/rest/v1/standards"
    params = {"id": f"eq.{standard_id}"}
    data = {"category_id": category_id}
    
    response = requests.patch(url, headers=headers, params=params, json=data)
    return response.status_code in [200, 204]

def main():
    print("🔧 Assigning standards to categories...\n")

    # Get categories
    categories = get_data("categories")
    if not categories:
        print("❌ Failed to fetch categories")
        return

    cat_map = {cat['slug']: cat['id'] for cat in categories}
    print(f"📊 Found {len(categories)} categories")
    
    # Get standards
    standards = get_data("standards", {"is_active": "eq.true"})
    if not standards:
        print("❌ Failed to fetch standards")
        return

    print(f"📋 Found {len(standards)} standards\n")

    # Assign categories
    updated = 0
    skipped = 0
    
    for std in standards:
        code = std['code']
        target_category_slug = STANDARD_CATEGORY_MAP.get(code)
        
        if target_category_slug is None:
            print(f"  ⊘ {code}: Keep as general (applies to all)")
            skipped += 1
            continue
        
        if target_category_slug not in cat_map:
            print(f"  ⚠️  {code}: Category '{target_category_slug}' not found")
            continue
        
        category_id = cat_map[target_category_slug]
        
        if update_standard(std['id'], category_id):
            cat_name = next(c['name'] for c in categories if c['id'] == category_id)
            print(f"  ✅ {code} → {cat_name}")
            updated += 1
        else:
            print(f"  ❌ {code}: Update failed")

    print(f"\n📊 Summary:")
    print(f"  • Updated: {updated}")
    print(f"  • Skipped (general): {skipped}")
    print(f"  • Total: {len(standards)}")
    print("\n✅ Category assignment complete!\n")

if __name__ == "__main__":
    main()
