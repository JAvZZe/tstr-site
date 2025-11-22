#!/usr/bin/env python3
"""
Add Hydrogen Infrastructure Testing category
"""

import requests
import uuid

SUPABASE_URL = "https://haimjeaetrsaauitrhfy.supabase.co"
SERVICE_ROLE_KEY = "sb_secret_zRN1fTFOYnN7cEbEIfAP7A_YrEKBfI2"

headers = {
    "apikey": SERVICE_ROLE_KEY,
    "Authorization": f"Bearer {SERVICE_ROLE_KEY}",
    "Content-Type": "application/json"
}

def category_exists(slug):
    """Check if category already exists"""
    url = f"{SUPABASE_URL}/rest/v1/categories"
    params = {"select": "id", "slug": f"eq.{slug}"}
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    return len(data) > 0

def add_category(name, slug):
    """Add a new category"""
    if category_exists(slug):
        print(f"⚠️  Category '{name}' already exists")
        return False
    
    url = f"{SUPABASE_URL}/rest/v1/categories"
    data = {
        "id": str(uuid.uuid4()),
        "name": name,
        "slug": slug
    }
    
    response = requests.post(url, headers=headers, json=data)
    if response.status_code in [200, 201]:
        print(f"✅ Added category: {name}")
        return True
    else:
        print(f"❌ Failed to add category: {response.text}")
        return False

if __name__ == "__main__":
    print("🔬 Adding Hydrogen Infrastructure Testing category...\n")
    add_category("Hydrogen Infrastructure Testing", "hydrogen-infrastructure-testing")
    print("\n✅ Done!")
