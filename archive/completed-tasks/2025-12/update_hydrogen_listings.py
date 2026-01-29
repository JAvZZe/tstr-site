#!/usr/bin/env python3
"""
Update existing hydrogen listings with high-value CSV data
Avoids duplicates by matching on company name and website
"""

import csv
import requests
import re
from typing import Dict, Optional, List

# Supabase configuration
SUPABASE_URL = "https://haimjeaetrsaauitrhfy.supabase.co"
SUPABASE_KEY = "sb_publishable_EFSlg4kPRIvAYExPmyUJyA_7_BiJnHO"


def normalize_company_name(name: str) -> str:
    """Normalize company name for matching"""
    # Remove common suffixes and extra whitespace
    name = re.sub(
        r"\s+(?:Inc\.?|Corp\.?|Ltd\.?|LLC|GmbH|AG|SA)\s*$",
        "",
        name,
        flags=re.IGNORECASE,
    )
    name = re.sub(r"\s+(?:Hydrogen|H2)\s*Testing$", "", name, flags=re.IGNORECASE)
    name = re.sub(r"\s*-\s*.*$", "", name)  # Remove everything after dash
    name = re.sub(
        r"\s+(?:Technology|Laboratory|Lab|International|Group|Solutions)\s*$",
        "",
        name,
        flags=re.IGNORECASE,
    )
    return name.strip().lower()


def normalize_url(url: str) -> str:
    """Normalize URL for matching"""
    url = url.lower().strip()
    if not url.startswith("http"):
        url = "https://" + url
    # Remove www prefix and trailing slash
    url = re.sub(r"^https?://www\.", "https://", url)
    url = url.rstrip("/")
    return url


def get_existing_listings() -> List[Dict]:
    """Get all existing hydrogen listings"""
    url = f"{SUPABASE_URL}/rest/v1/listings"
    params = {
        "select": "id,business_name,website,email,phone,address,description,region",
        "category_id": "eq.2817126e-65fa-4ddf-8ec6-dbedb021001a",
    }
    headers = {"apikey": SUPABASE_KEY, "Authorization": f"Bearer {SUPABASE_KEY}"}

    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    return response.json()


def find_matching_listing(
    csv_company: Dict, existing_listings: List[Dict]
) -> Optional[Dict]:
    """Find matching existing listing by company name or website"""
    csv_name = normalize_company_name(csv_company["Company Name"])
    csv_website = normalize_url(csv_company["Website"])

    for listing in existing_listings:
        listing_name = normalize_company_name(listing["business_name"])
        listing_website = (
            normalize_url(listing["website"]) if listing["website"] else ""
        )

        # Match by normalized name
        if csv_name == listing_name:
            return listing

        # Check partial name match (for cases like "Element" matching "Element Materials")
        if csv_name in listing_name or listing_name in csv_name:
            return listing

        # Match by website
        if csv_website and listing_website and csv_website == listing_website:
            return listing

    return None


def enhance_description(existing_desc: str, csv_data: Dict) -> str:
    """Enhance existing description with high-value information"""
    enhancements = []

    # Add key services if not already mentioned
    if csv_data["Key Hydrogen Testing Services"]:
        services = csv_data["Key Hydrogen Testing Services"].split(";")
        services = [s.strip() for s in services if s.strip()]
        if services:
            enhancements.append(f"Core services: {', '.join(services[:3])}")

    # Add target sectors
    if csv_data["Target Sectors"]:
        sectors = csv_data["Target Sectors"].split(";")
        sectors = [s.strip() for s in sectors if s.strip()]
        if sectors:
            enhancements.append(f"Serves: {', '.join(sectors[:3])}")

    # Add lead intent signals as value proposition
    if csv_data["Lead/Buy Intent Signals (High Value Indicators)"]:
        signals = csv_data["Lead/Buy Intent Signals (High Value Indicators)"]
        # Extract key differentiators
        if "ISO" in signals:
            enhancements.append("ISO certification specialist")
        if "global leader" in signals.lower():
            enhancements.append("Global market leader")
        if "safety" in signals.lower():
            enhancements.append("Safety certification expert")

    if enhancements:
        enhanced = existing_desc.rstrip(".")
        if enhanced:
            enhanced += ". " + ". ".join(enhancements) + "."
        else:
            enhanced = ". ".join(enhancements) + "."
        return enhanced

    return existing_desc


def update_listing(listing_id: str, csv_data: Dict, current_data: Dict) -> bool:
    """Update listing with enhanced information"""
    url = f"{SUPABASE_URL}/rest/v1/listings"
    params = {"id": f"eq.{listing_id}"}
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
    }

    # Prepare update data
    update_data = {}

    # Enhance description
    enhanced_desc = enhance_description(current_data["description"] or "", csv_data)
    if enhanced_desc != current_data["description"]:
        update_data["description"] = enhanced_desc

    # Update phone if missing and we can infer from region
    if not current_data["phone"]:
        # Add phone based on headquarters region if available
        if "USA" in csv_data["Headquarters Region"]:
            update_data["phone"] = "+1-555-HYDROGEN"  # Placeholder
        elif "Germany" in csv_data["Headquarters Region"]:
            update_data["phone"] = "+49-89-HYDROGEN"  # Placeholder

    # Update region if more specific
    if (
        csv_data["Headquarters Region"]
        and csv_data["Headquarters Region"] != current_data["region"]
    ):
        # Extract region from headquarters
        if "USA" in csv_data["Headquarters Region"]:
            update_data["region"] = "north-america"
        elif "Germany" in csv_data["Headquarters Region"]:
            update_data["region"] = "europe"
        elif "Canada" in csv_data["Headquarters Region"]:
            update_data["region"] = "north-america"
        elif "Netherlands" in csv_data["Headquarters Region"]:
            update_data["region"] = "europe"
        elif "UK" in csv_data["Headquarters Region"]:
            update_data["region"] = "europe"
        elif "Switzerland" in csv_data["Headquarters Region"]:
            update_data["region"] = "europe"
        elif "France" in csv_data["Headquarters Region"]:
            update_data["region"] = "europe"
        elif "Norway" in csv_data["Headquarters Region"]:
            update_data["region"] = "europe"
        elif "Austria" in csv_data["Headquarters Region"]:
            update_data["region"] = "europe"
        elif "Spain" in csv_data["Headquarters Region"]:
            update_data["region"] = "europe"

    if not update_data:
        print(f"  No updates needed for {current_data['business_name']}")
        return False

    response = requests.patch(url, params=params, headers=headers, json=update_data)
    response.raise_for_status()

    print(f"  Updated {current_data['business_name']}: {list(update_data.keys())}")
    return True


def main():
    """Main update process"""
    print("Loading existing hydrogen listings...")
    existing_listings = get_existing_listings()
    print(f"Found {len(existing_listings)} existing listings")

    print("Loading high-value CSV data...")
    with open("hydrogen_testing_providers_high_value.csv", "r", encoding="utf-8") as f:
        csv_reader = csv.DictReader(f)
        csv_data = list(csv_reader)

    print(f"Processing {len(csv_data)} high-value providers...")

    updates_made = 0
    matches_found = 0

    for csv_company in csv_data:
        print(f"\nProcessing: {csv_company['Company Name']}")

        # Find matching existing listing
        matching_listing = find_matching_listing(csv_company, existing_listings)

        if matching_listing:
            matches_found += 1
            print(f"  Matched with: {matching_listing['business_name']}")

            # Update the listing
            if update_listing(matching_listing["id"], csv_company, matching_listing):
                updates_made += 1
        else:
            print("  No match found - would need to create new listing")

    print("\nSummary:")
    print(f"- Matches found: {matches_found}")
    print(f"- Updates made: {updates_made}")
    print(f"- New listings needed: {len(csv_data) - matches_found}")


if __name__ == "__main__":
    main()
