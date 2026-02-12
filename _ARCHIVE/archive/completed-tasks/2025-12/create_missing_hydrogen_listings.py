#!/usr/bin/env python3
"""
Create missing hydrogen listings from high-value CSV data
"""

import csv
import requests
import uuid
from typing import Dict, List

# Supabase configuration
SUPABASE_URL = "https://haimjeaetrsaauitrhfy.supabase.co"
SUPABASE_KEY = "sb_secret_zRN1fTFOYnN7cEbEIfAP7A_YrEKBfI2"  # Service key for writes


def get_existing_listings() -> List[Dict]:
    """Get all existing hydrogen listings to avoid duplicates"""
    url = f"{SUPABASE_URL}/rest/v1/listings"
    params = {
        "select": "business_name,website",
        "category_id": "eq.2817126e-65fa-4ddf-8ec6-dbedb021001a",
    }
    headers = {"apikey": SUPABASE_KEY, "Authorization": f"Bearer {SUPABASE_KEY}"}

    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    return response.json()


def create_listing(csv_data: Dict) -> bool:
    """Create a new listing from CSV data"""
    url = f"{SUPABASE_URL}/rest/v1/listings"
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal",
    }

    # Generate slug from company name
    slug = (
        csv_data["Company Name"]
        .lower()
        .replace(" ", "-")
        .replace(",", "")
        .replace("/", "-")
    )
    slug = slug.replace("(", "").replace(")", "").replace("+", "plus")

    # Map headquarters to location_id and region
    location_map = {
        "Switzerland": "fca58d48-fd86-4ce5-834d-2af0c9f66331",  # Europe
        "UK": "6c7e103a-e091-4f4c-8061-49a0f69b7890",  # United Kingdom
        "France": "fca58d48-fd86-4ce5-834d-2af0c9f66331",  # Europe
        "USA": "4a1482aa-6387-4f44-84ea-bbe11eb2f4f1",  # United States
        "Norway": "fca58d48-fd86-4ce5-834d-2af0c9f66331",  # Europe
        "Austria": "fca58d48-fd86-4ce5-834d-2af0c9f66331",  # Europe
        "Netherlands": "fca58d48-fd86-4ce5-834d-2af0c9f66331",  # Europe
        "Spain": "fca58d48-fd86-4ce5-834d-2af0c9f66331",  # Europe
        "Germany": "fca58d48-fd86-4ce5-834d-2af0c9f66331",  # Europe
        "Canada": "f5dd17ac-34b0-4927-a382-1620e5dee1e3",  # North America
    }

    region_map = {
        "Switzerland": "europe",
        "UK": "europe",
        "France": "europe",
        "USA": "north-america",
        "Norway": "europe",
        "Austria": "europe",
        "Netherlands": "europe",
        "Spain": "europe",
        "Germany": "europe",
        "Canada": "north-america",
    }

    location_id = "aac4019b-7e93-4aec-ba55-150103da7d6f"  # Default: Global
    region = "global"

    for country, loc_id in location_map.items():
        if country in csv_data["Headquarters Region"]:
            location_id = loc_id
            region = region_map[country]
            break

    # Create enhanced description
    services = csv_data["Key Hydrogen Testing Services"].split(";")
    services = [s.strip() for s in services if s.strip()]

    sectors = csv_data["Target Sectors"].split(";")
    sectors = [s.strip() for s in sectors if s.strip()]

    description = f"Leading provider in {csv_data['Headquarters Region']}. "
    description += f"Specializes in: {', '.join(services[:3])}. "
    description += f"Primary sectors: {', '.join(sectors[:2])}. "

    # Add lead intent signals
    signals = csv_data["Lead/Buy Intent Signals (High Value Indicators)"]
    if "global leader" in signals.lower():
        description += (
            "Global market leader with extensive certification capabilities. "
        )
    if "ISO" in signals:
        description += "ISO certification specialist. "
    if "safety" in signals.lower():
        description += "Safety certification expert. "

    listing_data = {
        "id": str(uuid.uuid4()),
        "category_id": "2817126e-65fa-4ddf-8ec6-dbedb021001a",
        "location_id": location_id,
        "business_name": csv_data["Company Name"],
        "slug": slug,
        "description": description.strip(),
        "website": csv_data["Website"],
        "email": "",  # Not provided in CSV
        "phone": "",  # Not provided in CSV
        "address": csv_data["Headquarters Region"],
        "latitude": None,
        "longitude": None,
        "plan_type": "free",
        "is_featured": False,
        "featured_until": None,
        "status": "active",
        "verified": False,
        "claimed": False,
        "views": 0,
        "published_at": None,
        "featured": False,
        "priority_rank": 0,
        "region": region,
    }

    response = requests.post(url, headers=headers, json=listing_data)
    response.raise_for_status()
    return response.status_code == 201


def main():
    """Create missing listings"""
    print("Loading existing listings...")
    existing = get_existing_listings()
    existing_names = {item["business_name"].lower() for item in existing}
    existing_websites = {item["website"].lower() for item in existing}

    print("Loading CSV data...")
    with open("hydrogen_testing_providers_high_value.csv", "r", encoding="utf-8") as f:
        csv_reader = csv.DictReader(f)
        csv_data = list(csv_reader)

    print("Creating missing listings...")
    created = 0
    skipped = 0

    for row in csv_data:
        name = row["Company Name"]
        website = row["Website"].lower()

        # Skip if already exists
        if name.lower() in existing_names or website in existing_websites:
            print(f"Skipping {name} - already exists")
            skipped += 1
            continue

        try:
            if create_listing(row):
                print(f"✅ Created: {name}")
                created += 1
            else:
                print(f"❌ Failed to create: {name}")
        except Exception as e:
            print(f"❌ Error creating {name}: {e}")

    print("\nSummary:")
    print(f"Created: {created}")
    print(f"Skipped: {skipped}")
    print(f"Total processed: {len(csv_data)}")


if __name__ == "__main__":
    main()
