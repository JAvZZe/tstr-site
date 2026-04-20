# ruff: noqa: E402
import os
from dotenv import load_dotenv
# Load environment variables from .env file in the same directory as this script
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))



# Load environment variables from .env file in the same directory as this script

import json
import re

import requests

# Path to .env

env_path = "/media/al/AI_DATA/AI_PROJECTS_SPACE/ACTIVE_PROJECTS/tstr-site-working/web/tstr-frontend/.env"
load_dotenv(env_path)

URL = os.getenv("PUBLIC_SUPABASE_URL")
# Use Service Role Key for writes
KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

if not URL or not KEY:
    print("Error: Missing credentials in .env")
    exit(1)

HEADERS = {
    "apikey": KEY,
    "Authorization": f"Bearer {KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}

KNOWN_CONGLOMERATES = [
    "SGS", "Intertek", "Bureau Veritas", "Eurofins", "Mistras", "Applus", 
    "ALS", "TUV SUD", "TUV Rheinland", "TUV Nord", "Dekra", "UL Solutions", 
    "BSI", "Halliburton", "Schlumberger"
]

def detect_parent(name):
    name_upper = name.upper()
    for brand in KNOWN_CONGLOMERATES:
        if name_upper.startswith(brand.upper()):
            return brand
    return None

def get_or_create_parent(parent_name, category_id):
    # Check if parent exists
    query_url = f"{URL}/rest/v1/listings?business_name=eq.{parent_name}&parent_listing_id=is.null&select=id"
    resp = requests.get(query_url, headers=HEADERS)
    data = resp.json()
    
    if data:
        return data[0]['id']
        
    # Create parent
    slug = re.sub(r"[^a-z0-9]+", "-", parent_name.lower()).strip("-")
    parent_data = {
        "business_name": parent_name,
        "slug": f"group-{slug}",
        "category_id": category_id,
        "status": "active",
        "description": f"Parent brand for {parent_name} group of testing facilities."
    }
    resp = requests.post(f"{URL}/rest/v1/listings", headers=HEADERS, data=json.dumps(parent_data))
    if resp.status_code in [200, 201]:
        created = resp.json()
        print(f"Created Parent: {parent_name}")
        return created[0]['id']
    return None

def run():
    print("Fetching listings...")
    query_url = f"{URL}/rest/v1/listings?parent_listing_id=is.null&select=id,business_name,category_id"
    resp = requests.get(query_url, headers=HEADERS)
    listings = resp.json()
    
    print(f"Processing {len(listings)} listings...")
    for listing in listings:
        name = listing['business_name']
        parent_name = detect_parent(name)
        
        if parent_name and parent_name.upper() != name.upper():
            print(f"Linking '{name}' to '{parent_name}'...")
            parent_id = get_or_create_parent(parent_name, listing['category_id'])
            if parent_id:
                patch_url = f"{URL}/rest/v1/listings?id=eq.{listing['id']}"
                requests.patch(patch_url, headers=HEADERS, data=json.dumps({"parent_listing_id": parent_id}))
                print(f"✓ Linked {name}")

if __name__ == "__main__":
    run()
