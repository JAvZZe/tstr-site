#!/usr/bin/env python3
"""
Analyze listings and suggest standard assignments
"""

import requests
import json
from collections import defaultdict

SUPABASE_URL = "https://haimjeaetrsaauitrhfy.supabase.co"
SERVICE_ROLE_KEY = "sb_secret_zRN1fTFOYnN7cEbEIfAP7A_YrEKBfI2"

headers = {
    "apikey": SERVICE_ROLE_KEY,
    "Authorization": f"Bearer {SERVICE_ROLE_KEY}",
    "Content-Type": "application/json"
}

def fetch_data(table, select="*", filters=None):
    """Fetch data from Supabase"""
    url = f"{SUPABASE_URL}/rest/v1/{table}"
    params = {"select": select}
    if filters:
        params.update(filters)
    
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching {table}: {response.text}")
        return None

def main():
    print("🔍 Analyzing TSTR.site listings...\n")

    # Get categories
    categories = fetch_data("categories", "id,name,slug", {"order": "name"})
    if not categories:
        return

    print("📊 Categories:")
    cat_map = {}
    for cat in categories:
        print(f"  - {cat['name']} ({cat['slug']})")
        cat_map[cat['id']] = cat['name']
    print()

    # Get listings
    listings = fetch_data(
        "listings",
        "id,business_name,category_id,address",
        {"status": "eq.active", "order": "business_name"}
    )
    if not listings:
        return

    print(f"📋 Total Active Listings: {len(listings)}\n")

    # Group by category
    by_category = defaultdict(list)
    for listing in listings:
        cat_name = cat_map.get(listing['category_id'], 'Uncategorized')
        by_category[cat_name].append(listing)

    print("📈 Listings by Category:")
    for cat_name, cat_listings in sorted(by_category.items()):
        print(f"\n  {cat_name}: {len(cat_listings)} listings")
        print("  " + "-" * 50)
        for listing in cat_listings[:5]:
            print(f"    • {listing['business_name']}")
            addr = listing.get('address', 'No address')
            if addr and len(addr) > 60:
                addr = addr[:57] + "..."
            print(f"      {addr}")
        if len(cat_listings) > 5:
            print(f"    ... and {len(cat_listings) - 5} more")

    # Get standards
    standards = fetch_data(
        "standards",
        "id,code,name,issuing_body,category_id",
        {"is_active": "eq.true", "order": "code"}
    )
    if not standards:
        return

    print(f"\n\n🎯 Available Standards: {len(standards)}")

    # Group standards by category
    std_by_category = defaultdict(list)
    for std in standards:
        cat_name = cat_map.get(std['category_id'], 'General')
        std_by_category[cat_name].append(std)

    print("\n📋 Standards by Category:")
    for cat_name, cat_standards in sorted(std_by_category.items()):
        print(f"\n  {cat_name}: {len(cat_standards)} standards")
        for std in cat_standards:
            print(f"    • {std['code']} - {std['name']}")

    # Check existing capabilities
    capabilities = fetch_data("listing_capabilities", "count")
    cap_count = capabilities[0]['count'] if capabilities and len(capabilities) > 0 else 0
    print(f"\n\n📊 Current Capabilities: {cap_count}")

    # Save data for assignment script
    data = {
        'categories': cat_map,
        'listings': listings,
        'standards': standards,
        'by_category': {k: [listing['id'] for listing in v] for k, v in by_category.items()}
    }
    
    with open('/tmp/listings_data.json', 'w') as f:
        json.dump(data, f, indent=2)
    
    print("\n💾 Data saved to /tmp/listings_data.json")
    print("\n✅ Analysis complete!\n")

if __name__ == "__main__":
    main()
