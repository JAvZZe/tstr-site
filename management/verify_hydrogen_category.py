#!/usr/bin/env python3
"""
Verify hydrogen listings are in correct category
"""
import os

import requests

SUPABASE_URL = "https://haimjeaetrsaauitrhfy.supabase.co"
SERVICE_ROLE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")

headers = {
    "apikey": SERVICE_ROLE_KEY,
    "Authorization": f"Bearer {SERVICE_ROLE_KEY}",
    "Content-Type": "application/json"
}

def get_hydrogen_category_id():
    """Get hydrogen category ID"""
    url = f"{SUPABASE_URL}/rest/v1/categories"
    params = {"select": "id,name,slug", "slug": "eq.hydrogen-infrastructure-testing"}
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    return data[0] if data and len(data) > 0 else None

def get_listings_in_category(category_id):
    """Get all listings in a category"""
    url = f"{SUPABASE_URL}/rest/v1/listings"
    params = {
        "select": "id,business_name,category_id",
        "category_id": f"eq.{category_id}"
    }
    response = requests.get(url, headers=headers, params=params)
    return response.json()

if __name__ == "__main__":
    print("🔍 Verifying hydrogen category assignments...\n")
    
    # Get category
    h2_cat = get_hydrogen_category_id()
    if not h2_cat:
        print("❌ Hydrogen category not found")
        exit(1)
    
    print(f"✅ Category: {h2_cat['name']}")
    print(f"   Slug: {h2_cat['slug']}")
    print(f"   ID: {h2_cat['id']}\n")
    
    # Get listings
    listings = get_listings_in_category(h2_cat['id'])
    
    if isinstance(listings, list):
        print(f"📋 Listings in this category: {len(listings)}\n")
        for listing in listings:
            if isinstance(listing, dict) and 'business_name' in listing:
                print(f"  ✅ {listing['business_name']}")
    else:
        print(f"❌ Error getting listings: {listings}")
    
    print("\n✅ Verification complete!")
