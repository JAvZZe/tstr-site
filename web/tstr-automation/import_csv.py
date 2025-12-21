#!/usr/bin/env python3
"""
Import environmental testing data from CSV to Supabase
"""

import csv
import requests
import re
import os

# Supabase config
SUPABASE_URL = "https://haimjeaetrsaauitrhfy.supabase.co"
SUPABASE_KEY = "sb_secret_RgE06wiCRdOOlhV4KJER0g_BfDJjWuB"
CATEGORY_ID = "a80a47e9-ca57-4712-9b55-d3139b98a6b7"  # environmental-testing
DEFAULT_LOCATION_ID = "aac4019b-7e93-4aec-ba55-150103da7d6f"  # Global

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
}


def create_slug(business_name):
    """Create URL-safe slug from business name"""
    if not business_name:
        return "listing"
    slug = re.sub(r"[^a-z0-9]+", "-", business_name.lower()).strip("-")
    return slug[:100] if len(slug) > 100 else slug


def import_listings(csv_path):
    """Import listings from CSV"""
    with open(csv_path, "r", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            # Prepare listing data
            listing_data = {
                "business_name": row.get("business_name", ""),
                "slug": create_slug(row.get("business_name", "")),
                "description": row.get("description", ""),
                "category_id": CATEGORY_ID,
                "location_id": DEFAULT_LOCATION_ID,
                "address": row.get("address", ""),
                "phone": row.get("phone", ""),
                "email": row.get("email", ""),
                "website": row.get("website", ""),
                "latitude": row.get("latitude") or None,
                "longitude": row.get("longitude") or None,
                "status": "active",
            }

            # Insert listing
            response = requests.post(
                f"{SUPABASE_URL}/rest/v1/listings", json=listing_data, headers=HEADERS
            )

            if response.status_code == 201:
                listing_id = response.json()[0]["id"]
                print(f"✓ Inserted: {listing_data['business_name']}")

                # TODO: Insert custom fields if needed
            else:
                print(
                    f"✗ Failed: {listing_data['business_name']} - {response.status_code} {response.text}"
                )


if __name__ == "__main__":
    csv_path = "scraped_data/environmental-testing_dry_run.csv"
    if os.path.exists(csv_path):
        import_listings(csv_path)
    else:
        print(f"CSV file not found: {csv_path}")
