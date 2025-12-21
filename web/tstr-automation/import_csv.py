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

# Custom field mappings
CUSTOM_FIELD_IDS = {
    "test_types": "ca1e913d-607a-4f5e-805a-a0d7c259c844",
    "field_lab_services": "de4f9cb6-e4b4-4f70-8614-5c4852c66d8f",
    "esg_reporting": "d4398344-5a21-4fc0-a2bc-1a4dbe185f1f",
    "compliance_standards": "8b53a055-d783-467f-9328-7e4c3d30ab9f",
    "monitoring_tech": "4e8559ae-cfd3-4b5d-b07e-2e81e0bd8ab4",
    "custom_programs": "ecaf5bd9-ea2f-44cd-b60e-0718110340ce",
    "sampling_equipment": "0bb668df-b16f-4feb-8a62-8a21fce923ff",
}


def create_slug(business_name):
    """Create URL-safe slug from business name"""
    if not business_name:
        return "listing"
    slug = re.sub(r"[^a-z0-9]+", "-", business_name.lower()).strip("-")
    return slug[:100] if len(slug) > 100 else slug


def insert_custom_fields(listing_id, row):
    """Insert custom field values for a listing"""
    for field_name, field_id in CUSTOM_FIELD_IDS.items():
        value = row.get(field_name)
        if not value or value == "":
            continue

        # Handle different field types
        if field_name in ["esg_reporting", "custom_programs"]:
            # Boolean fields
            if value.lower() in ["true", "1", "yes"]:
                field_value = "true"
            else:
                continue  # Skip false values
        elif field_name in ["test_types", "field_lab_services", "compliance_standards"]:
            # Multi-select fields - value is already a string, keep as is
            field_value = value
        else:
            # Text fields
            field_value = value

        custom_data = {
            "listing_id": listing_id,
            "custom_field_id": field_id,
            "value": field_value,
        }

        response = requests.post(
            f"{SUPABASE_URL}/rest/v1/listing_custom_fields",
            json=custom_data,
            headers=HEADERS,
        )

        if response.status_code == 201:
            print(f"  ✓ Custom field {field_name}: {field_value}")
        else:
            print(
                f"  ✗ Custom field {field_name} failed: {response.status_code} {response.text}"
            )


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

            # Check if listing already exists
            slug = listing_data["slug"]
            check_response = requests.get(
                f"{SUPABASE_URL}/rest/v1/listings?slug=eq.{slug}&category_id=eq.{CATEGORY_ID}",
                headers=HEADERS,
            )

            if check_response.status_code == 200 and check_response.json():
                # Listing exists
                listing_id = check_response.json()[0]["id"]
                print(f"✓ Exists: {listing_data['business_name']} (ID: {listing_id})")
            else:
                # Insert listing
                response = requests.post(
                    f"{SUPABASE_URL}/rest/v1/listings",
                    json=listing_data,
                    headers=HEADERS,
                )

                if response.status_code == 201:
                    listing_id = response.json()[0]["id"]
                    print(f"✓ Inserted: {listing_data['business_name']}")
                else:
                    print(
                        f"✗ Failed: {listing_data['business_name']} - {response.status_code} {response.text}"
                    )
                    continue

            # Insert custom fields
            insert_custom_fields(listing_id, row)


if __name__ == "__main__":
    csv_path = "scraped_data/environmental-testing_dry_run.csv"
    if os.path.exists(csv_path):
        import_listings(csv_path)
    else:
        print(f"CSV file not found: {csv_path}")
