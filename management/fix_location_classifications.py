#!/usr/bin/env python3
"""
Fix location data classification issues
"""

import requests

SUPABASE_URL = "https://haimjeaetrsaauitrhfy.supabase.co"
SERVICE_ROLE_KEY = "sb_secret_zRN1fTFOYnN7cEbEIfAP7A_YrEKBfI2"

headers = {
    "apikey": SERVICE_ROLE_KEY,
    "Authorization": f"Bearer {SERVICE_ROLE_KEY}",
    "Content-Type": "application/json",
}


def update_location(location_id, updates):
    """Update a location record"""
    url = f"{SUPABASE_URL}/rest/v1/locations?id=eq.{location_id}"
    response = requests.patch(url, headers=headers, json=updates)
    if response.status_code == 204:
        print(f"✅ Updated location {location_id}")
        return True
    else:
        print(
            f"❌ Failed to update location {location_id}: {response.status_code} {response.text}"
        )
        return False


def delete_location(location_id):
    """Delete a location record"""
    url = f"{SUPABASE_URL}/rest/v1/locations?id=eq.{location_id}"
    response = requests.delete(url, headers=headers)
    if response.status_code == 204:
        print(f"✅ Deleted location {location_id}")
        return True
    else:
        print(
            f"❌ Failed to delete location {location_id}: {response.status_code} {response.text}"
        )
        return False


def main():
    print("🔧 Fixing location data classification issues...\n")

    # 1. Fix "New York" city -> should be region (state)
    print("1. Converting 'New York' from city to region...")
    update_location("ff98c268-a7f6-463f-8c89-a45e29c2d5ef", {"level": "region"})

    # 2. Delete incorrect "Global" city entry
    print("2. Deleting incorrect 'Global' city entry...")
    delete_location("4e362b36-cecc-4211-8fa4-bf130b845fa9")

    # 3. Delete redundant "Singapore" city entry
    print("3. Deleting redundant 'Singapore' city entry...")
    delete_location("0b7795f4-9ca1-4630-87d9-b94ce4d2a969")

    # 4. Remove duplicate London entry
    print("4. Deleting duplicate 'London' entry...")
    delete_location("8849f79a-45d6-4d05-af28-285704013d33")

    # 5. Fix country parent relationships
    print("5. Moving countries to correct regional parents...")

    # Europe region ID: fca58d48-fd86-4ce5-834d-2af0c9f66331
    # North America region ID: f5dd17ac-34b0-4927-a382-1620e5dee1e3

    update_location(
        "278460d5-e563-4fdb-93c5-530558c2545a",
        {"parent_id": "fca58d48-fd86-4ce5-834d-2af0c9f66331"},
    )  # Germany
    update_location(
        "8aa3f6ff-cd02-4ef6-9e53-caad984fd38e",
        {"parent_id": "fca58d48-fd86-4ce5-834d-2af0c9f66331"},
    )  # Netherlands
    update_location(
        "0ad2249c-5410-4770-ad07-2bf50e1f26d1",
        {"parent_id": "f5dd17ac-34b0-4927-a382-1620e5dee1e3"},
    )  # Canada

    # 6. Fix name issues
    print("6. Fixing name issues...")
    update_location(
        "cc4b7836-3379-4e5e-a9c8-2c100677d0ba", {"name": "Kuwait", "slug": "kuwait"}
    )  # Kuwait Kuwait

    # 7. Standardize city name casing
    print("7. Standardizing city name casing...")

    city_casing_fixes = [
        ("505ab576-6390-4220-a7d0-eecb0872958e", "North Brunswick", "north-brunswick"),
        ("64c89153-bdfe-4e4e-b2d9-666157b40978", "Hill AFB", "hill-afb"),
        ("b02a198e-a36b-4aa1-a8cf-1adb42cdbba7", "Nederland", "nederland"),
        ("6ac44ba7-fdbb-4dd6-a7bc-e7daa628579c", "Morrisville", "morrisville"),
        ("d67c6ff7-b99e-4931-b972-92862a3c4771", "Brainerd", "brainerd"),
        ("97bd893c-181e-421d-9e1c-48514405f4c7", "Abilene", "abilene"),
        ("9d9dc3fb-91ee-4dc1-8266-8b8d7dbfdcf7", "Puposky", "puposky"),
        ("f0266a27-3651-497c-ab46-e8cd24cb320b", "Independence", "independence"),
        ("93803cfb-60f6-423d-8867-286a45d7439c", "Romulus", "romulus"),
        ("f57de571-0c12-49de-b793-0b64a5e9db11", "Stillwater", "stillwater"),
        ("46b29f09-3f23-40ce-9046-d3a4c15d02e4", "Addison", "addison"),
        ("8133b34d-65de-483c-ba89-9f88abfdedd4", "Elmhurst", "elmhurst"),
        ("97013aed-47d3-4104-8079-fac294d59627", "Minneapolis", "minneapolis"),
        ("a20af9da-00c6-4d32-aa47-2d9c1465e479", "Warwick", "warwick"),
        ("cdb57e3a-c8db-4336-816c-ada4f1bb6f7b", "Kokomo", "kokomo"),
        ("0b241618-6328-40e6-b775-4354a6116dc0", "Westminster", "westminster"),
        ("4520cf54-6195-4e57-a7d2-5dc9d40f9de4", "Plano", "plano"),
        ("d6eeb742-68f7-4c21-834e-80a32282d12c", "Cleveland", "cleveland"),
        ("040ba3b4-cb18-476f-b428-d6db22079f33", "Al Qurain", "al-qurain"),
        ("425cb59b-99ba-4ef0-9bb6-e7b515ad9b4a", "New Berlin", "new-berlin"),
        ("fe02d095-f38f-4692-94a1-260804af2e93", "Des Moines", "des-moines"),
        ("2ef25314-322d-448c-b1f1-d4bc8179c30e", "Harrisburg", "harrisburg"),
        ("5b3ae6a0-52c4-455f-9e95-c0cad03ca0af", "Naples", "naples"),
        ("9c1cdcbe-f245-4d95-9799-f07bc4f05355", "Milford", "milford"),
        ("837223af-99f5-4a5c-acd4-cdeb74337581", "Livonia", "livonia"),
        ("fc1a649b-59c4-498a-95ac-539cce9e0949", "Hudson", "hudson"),
        ("c1a2a157-1e65-44dc-9e78-66dc1d89c3ef", "Upper Marlboro", "upper-marlboro"),
        ("1a2092f2-5715-4520-be90-da38140d81dc", "Kentwood", "kentwood"),
        ("c8a8c491-ed8c-428c-ad6e-53130e040748", "Munich", "munich-germany"),
        ("78d6c1bf-3a87-4f47-8fec-dd79957a613e", "Apeldoorn", "apeldoorn-netherlands"),
        ("1f00cc78-1b80-4d37-a700-9f5a0047c05b", "Surrey", "surrey-canada"),
        (
            "47a889b4-984c-45e7-864f-8db351d03c2d",
            "Bartlesville",
            "bartlesville-united-states",
        ),
    ]

    for location_id, name, slug in city_casing_fixes:
        update_location(location_id, {"name": name, "slug": slug})

    print("\n✅ Location data fixes completed!")


if __name__ == "__main__":
    main()
