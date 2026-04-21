#!/usr/bin/env python3
"""
Update listings to Hydrogen Infrastructure Testing category
"""
import os

import requests

SUPABASE_URL = "https://haimjeaetrsaauitrhfy.supabase.co"
SERVICE_ROLE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")

headers = {
    "apikey": SERVICE_ROLE_KEY,
    "Authorization": f"Bearer {SERVICE_ROLE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}

def get_hydrogen_category_id():
    """Get hydrogen category ID"""
    url = f"{SUPABASE_URL}/rest/v1/categories"
    params = {"select": "id", "slug": "eq.hydrogen-infrastructure-testing"}
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    return data[0]['id'] if data and len(data) > 0 else None

def update_listing_category(listing_id, category_id):
    """Update a listing's category"""
    url = f"{SUPABASE_URL}/rest/v1/listings"
    params = {"id": f"eq.{listing_id}"}
    data = {"category_id": category_id}
    
    response = requests.patch(url, headers=headers, params=params, json=data)
    return response.status_code in [200, 204]

if __name__ == "__main__":
    print("🔬 Updating hydrogen listings to new category...\n")
    
    # Get category ID
    h2_cat_id = get_hydrogen_category_id()
    if not h2_cat_id:
        print("❌ Hydrogen category not found")
        exit(1)
    
    print(f"✅ Hydrogen category ID: {h2_cat_id}\n")
    
    # Read listing IDs
    try:
        with open('/tmp/hydrogen_listing_ids.txt', 'r') as f:
            listing_ids = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print("❌ No listing IDs file found. Run find_hydrogen_listings.py first.")
        exit(1)
    
    print(f"📋 Updating {len(listing_ids)} listings...\n")
    
    # Update each listing
    success_count = 0
    for listing_id in listing_ids:
        if update_listing_category(listing_id, h2_cat_id):
            print(f"  ✅ Updated listing {listing_id[:8]}...")
            success_count += 1
        else:
            print(f"  ❌ Failed to update listing {listing_id[:8]}...")
    
    print(f"\n✅ Successfully updated {success_count}/{len(listing_ids)} listings")
