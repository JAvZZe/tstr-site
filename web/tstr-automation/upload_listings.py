
import json
import requests
import os
import sys
import uuid
import re

# CONFIG
JSON_FILE = "insert_new_linkedin_companies.json"
SUPABASE_URL = "https://haimjeaetrsaauitrhfy.supabase.co"
SUPABASE_KEY = "sb_secret_zRN1fTFOYnN7cEbEIfAP7A_YrEKBfI2" 

def upload_listings():
    if not os.path.exists(JSON_FILE):
        print(f"File not found: {JSON_FILE}")
        sys.exit(1)

    with open(JSON_FILE, 'r') as f:
        listings = json.load(f)

    if not listings:
        print("No listings to upload.")
        return

    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal"
    }

    # 1. Fetch Categories
    cat_map = {}
    try:
        resp = requests.get(f"{SUPABASE_URL}/rest/v1/categories?select=id,slug", headers=headers)
        resp.raise_for_status()
        for c in resp.json():
            cat_map[c['slug']] = c['id']
    except Exception as e:
        print(f"Error fetching categories: {e}")
        return

    # 2. Fetch Locations (Need 'Global' or valid fallback)
    # The error showed "global" in the failing row for `region_slug` maybe?
    # Failing row: (..., 0, global, null...) 
    # Wait, the error `null value in column "location_id"` means we inserted NULL.
    # We need a valid UUID for `location_id`.
    
    location_id = None
    try:
        # Try to find 'Global' location
        resp = requests.get(f"{SUPABASE_URL}/rest/v1/locations?slug=eq.global&select=id", headers=headers)
        data = resp.json()
        if data:
            location_id = data[0]['id']
            print(f"Found Global Location ID: {location_id}")
        else:
            # Fallback: Just get ANY location (e.g. first one)
            print("Global location not found. Fetching any location...")
            resp = requests.get(f"{SUPABASE_URL}/rest/v1/locations?limit=1&select=id", headers=headers)
            data = resp.json()
            if data:
                location_id = data[0]['id']
                print(f"Using Fallback Location ID: {location_id}")
            else:
                print("CRITICAL: No locations found in DB!")
                return
    except Exception as e:
        print(f"Error fetching locations: {e}")
        return

    default_cat_id = cat_map.get('materials-testing')
    default_cat_id_fallback = list(cat_map.values())[0] if cat_map else None

    payload = []
    existing_slugs = set() 

    for item in listings:
        slug_base = re.sub(r'[^a-zA-Z0-9]', '-', item['company_name'].lower())
        slug_base = re.sub(r'-+', '-', slug_base).strip('-')
        slug = f"{slug_base}-{str(uuid.uuid4())[:4]}"
        
        while slug in existing_slugs:
             slug = f"{slug_base}-{str(uuid.uuid4())[:4]}"
        existing_slugs.add(slug)

        cat_slug = item['primary_category']
        cat_id = cat_map.get(cat_slug, default_cat_id) or default_cat_id_fallback

        record = {
            "business_name": item['company_name'],
            "slug": slug,
            "description": item['description'],
            "category_id": cat_id,
            "location_id": location_id, # FIX: Added this
            "status": "pending",
            "verified": False,
            "is_featured": False
        }
        payload.append(record)

    # 3. Upload in Batches
    BATCH_SIZE = 100
    print(f"Uploading {len(payload)} records with Location ID {location_id}...")
    
    for i in range(0, len(payload), BATCH_SIZE):
        batch = payload[i:i+BATCH_SIZE]
        print(f"Uploading batch {i//BATCH_SIZE + 1}...")
        
        try:
            resp = requests.post(
                f"{SUPABASE_URL}/rest/v1/listings",
                headers=headers,
                json=batch
            )
            if resp.status_code in [200, 201]:
                print(f"Batch {i//BATCH_SIZE + 1} Success.")
            else:
                print(f"Batch {i//BATCH_SIZE + 1} Failed: {resp.status_code} - {resp.text}")
        except Exception as e:
            print(f"Exception: {e}")

    print("Upload complete.")

if __name__ == "__main__":
    upload_listings()
