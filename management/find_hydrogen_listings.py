#!/usr/bin/env python3
"""
Find hydrogen-related listings
"""

import requests

SUPABASE_URL = "https://haimjeaetrsaauitrhfy.supabase.co"
SERVICE_ROLE_KEY = "sb_secret_zRN1fTFOYnN7cEbEIfAP7A_YrEKBfI2"

headers = {
    "apikey": SERVICE_ROLE_KEY,
    "Authorization": f"Bearer {SERVICE_ROLE_KEY}",
    "Content-Type": "application/json"
}

def get_hydrogen_category_id():
    """Get hydrogen category ID"""
    url = f"{SUPABASE_URL}/rest/v1/categories"
    params = {"select": "id", "slug": "eq.hydrogen-infrastructure-testing"}
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    return data[0]['id'] if data else None

def find_hydrogen_listings():
    """Find listings that mention hydrogen"""
    url = f"{SUPABASE_URL}/rest/v1/listings"
    params = {
        "select": "id,business_name,description,category_id",
        "or": "(business_name.ilike.*hydrogen*,description.ilike.*hydrogen*)"
    }
    response = requests.get(url, headers=headers, params=params)
    return response.json()

def get_listings_with_hydrogen_standards():
    """Find listings linked to hydrogen standards"""
    # Get hydrogen standards IDs
    url = f"{SUPABASE_URL}/rest/v1/standards"
    params = {
        "select": "id,code",
        "or": "(code.ilike.*19880*,code.ilike.*J2601*,code.ilike.*11114*,code.ilike.*R134*)"
    }
    response = requests.get(url, headers=headers, params=params)
    standards = response.json()
    
    if not standards:
        return []
    
    standard_ids = [s['id'] for s in standards]
    
    # Get listings linked to these standards
    url = f"{SUPABASE_URL}/rest/v1/listing_standards"
    params = {
        "select": "listing_id",
        "standard_id": f"in.({','.join(standard_ids)})"
    }
    response = requests.get(url, headers=headers, params=params)
    links = response.json()
    
    if not links or not isinstance(links, list):
        return []
    
    listing_ids = list(set([link['listing_id'] for link in links if isinstance(link, dict) and 'listing_id' in link]))
    
    # Get listing details
    url = f"{SUPABASE_URL}/rest/v1/listings"
    params = {
        "select": "id,business_name,description,category_id",
        "id": f"in.({','.join(listing_ids)})"
    }
    response = requests.get(url, headers=headers, params=params)
    return response.json()

if __name__ == "__main__":
    print("🔍 Finding hydrogen-related listings...\n")
    
    h2_cat_id = get_hydrogen_category_id()
    if not h2_cat_id:
        print("❌ Hydrogen category not found")
        exit(1)
    
    print(f"✅ Hydrogen category ID: {h2_cat_id}\n")
    
    # Find by name/description
    name_listings = find_hydrogen_listings()
    print(f"📋 Found {len(name_listings)} listings mentioning 'hydrogen':")
    if isinstance(name_listings, list):
        for listing in name_listings:
            if isinstance(listing, dict) and 'business_name' in listing:
                print(f"  • {listing['business_name'][:60]}")
    else:
        print(f"  Raw response: {name_listings}")
    
    print()
    
    # Find by standards linkage
    standards_listings = get_listings_with_hydrogen_standards()
    print(f"📋 Found {len(standards_listings)} listings with H2 standards:")
    if isinstance(standards_listings, list):
        for listing in standards_listings:
            if isinstance(listing, dict) and 'business_name' in listing:
                print(f"  • {listing['business_name'][:60]}")
    else:
        print(f"  Raw response: {standards_listings}")
    
    # Combine and deduplicate
    all_ids = set()
    if isinstance(name_listings, list):
        all_ids.update([listing['id'] for listing in name_listings if isinstance(listing, dict) and 'id' in listing])
    if isinstance(standards_listings, list):
        all_ids.update([listing['id'] for listing in standards_listings if isinstance(listing, dict) and 'id' in listing])
    
    print(f"\n✅ Total unique listings to update: {len(all_ids)}")
    
    if all_ids:
        # Save IDs for next script
        with open('/tmp/hydrogen_listing_ids.txt', 'w') as f:
            for lid in all_ids:
                f.write(f"{lid}\n")
        
        print("💾 Saved IDs to /tmp/hydrogen_listing_ids.txt")
    else:
        print("⚠️  No listings found to update")
