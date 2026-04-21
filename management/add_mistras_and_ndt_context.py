#!/usr/bin/env python3
"""
Add Non-Destructive Testing (NDT) category, standards, and Mistras Group listing.
"""
import os

import requests

SUPABASE_URL = "https://haimjeaetrsaauitrhfy.supabase.co"
# Using the service role key from project records
SERVICE_ROLE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")

headers = {
    "apikey": SERVICE_ROLE_KEY,
    "Authorization": f"Bearer {SERVICE_ROLE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}

def get_id(table, field, value):
    url = f"{SUPABASE_URL}/rest/v1/{table}"
    params = {"select": "id", field: f"eq.{value}"}
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    return data[0]['id'] if data else None

def main():
    print("🚀 Starting NDT & Mistras Group data integration...\n")

    # 1. Create NDT Category
    materials_id = get_id("categories", "slug", "materials-testing")
    if not materials_id:
        print("❌ Parent category 'Materials Testing' not found.")
        return

    print(f"✅ Found Materials Testing category: {materials_id}")

    ndt_cat_id = get_id("categories", "slug", "ndt-testing-inspection")
    if not ndt_cat_id:
        print("📁 Creating NDT & Asset Integrity category...")
        cat_data = {
            "name": "Non-Destructive Testing (NDT) & Asset Integrity",
            "slug": "ndt-testing-inspection",
            "parent_id": materials_id,
            "description": "Global leaders in non-destructive testing, asset protection, and structural health monitoring services."
        }
        response = requests.post(f"{SUPABASE_URL}/rest/v1/categories", headers=headers, json=cat_data)
        if response.status_code in [200, 201]:
            ndt_cat_id = response.json()[0]['id']
            print(f"✅ Created NDT Category: {ndt_cat_id}")
        else:
            print(f"❌ Failed to create category: {response.text}")
            return
    else:
        print(f"✅ NDT Category already exists: {ndt_cat_id}")

    # 2. Add NDT Standards
    standards = [
        {"code": "ASNT SNT-TC-1A", "name": "Personnel Qualification and Certification in NDT", "standard_type": "certification"},
        {"code": "NAS 410", "name": "NAS Certification & Qualification of Nondestructive Test Personnel", "standard_type": "certification"},
        {"code": "ASTM E1417", "name": "Standard Practice for Liquid Penetrant Testing", "standard_type": "test_method"},
        {"code": "ASTM E1444", "name": "Standard Practice for Magnetic Particle Testing", "standard_type": "test_method"},
        {"code": "ASTM E1742", "name": "Standard Practice for Radiographic Examination", "standard_type": "test_method"},
        {"code": "ASTM E569", "name": "Standard Practice for Acoustic Emission Monitoring of Structures", "standard_type": "test_method"},
        {"code": "API 510", "name": "Pressure Vessel Inspection Code", "standard_type": "compliance"},
        {"code": "API 570", "name": "Piping Inspection Code", "standard_type": "compliance"},
        {"code": "API 653", "name": "Tank Inspection, Repair, Alteration, and Reconstruction", "standard_type": "compliance"},
        {"code": "ISO 9712", "name": "Non-destructive testing — Qualification and certification of NDT personnel", "standard_type": "certification"}
    ]

    print("\n📜 Synchronizing NDT Standards...")
    standards_map = {}
    for std in standards:
        std_id = get_id("standards", "code", std['code'])
        if not std_id:
            std['category_id'] = ndt_cat_id
            response = requests.post(f"{SUPABASE_URL}/rest/v1/standards", headers=headers, json=std)
            if response.status_code in [200, 201]:
                std_id = response.json()[0]['id']
                print(f"✅ Added Standard: {std['code']}")
            else:
                print(f"❌ Failed to add standard {std['code']}: {response.text}")
                continue
        else:
            print(f"⏭️  Standard {std['code']} already exists.")
        standards_map[std['code']] = std_id

    # 3. Add Mistras Group Listing
    global_loc_id = get_id("locations", "slug", "global")
    if not global_loc_id:
        global_loc_id = get_id("locations", "slug", "united-states") # Fallback
    
    print(f"\n🌍 Found Location ID: {global_loc_id}")

    mistras_listing_id = get_id("listings", "slug", "mistras-group")
    if not mistras_listing_id:
        print("🏢 Creating Mistras Group listing...")
        mistras_data = {
            "business_name": "MISTRAS Group, Inc.",
            "slug": "mistras-group",
            "category_id": ndt_cat_id,
            "location_id": global_loc_id,
            "website": "https://www.mistrasgroup.com/",
            "description": "MISTRAS Group (NYSE: MG) is a leading global 'Pure-Play' provider of integrated asset protection solutions. Since 1978, MISTRAS has specialized in protecting critical infrastructure through advanced Non-Destructive Testing (NDT), field inspection, laboratory testing, and proprietary monitoring technology. Their proprietary software, PCMS and MISTRAS Digital, enables data-driven integrity management for energy, aerospace, and industrial sectors. MISTRAS is world-renowned for its expertise in Acoustic Emission (AE) monitoring, providing real-time structural health diagnostics for high-value assets.",
            "address": "195 Clarksville Road, Princeton Junction, NJ 08550, USA",
            "phone": "+1 609-716-4000",
            "status": "active",
            "verified": True,
            "is_featured": True,
            "plan_type": "premium",
            "billing_tier": "enterprise",
            "region": "global"
        }
        response = requests.post(f"{SUPABASE_URL}/rest/v1/listings", headers=headers, json=mistras_data)
        if response.status_code in [200, 201]:
            mistras_listing_id = response.json()[0]['id']
            print(f"✅ Created Listing: {mistras_listing_id}")
        else:
            print(f"❌ Failed to create listing: {response.text}")
            return
    else:
        print(f"✅ Listing already exists: {mistras_listing_id}")

    # 4. Link Capabilities
    print("\n🔗 Linking Capabilities...")
    capabilities = [
        {"code": "ASNT SNT-TC-1A", "specs": {"level": "I, II, III", "methods": ["UT", "RT", "MT", "PT", "AE", "ET"]}},
        {"code": "NAS 410", "specs": {"sector": "Aerospace", "methods": ["UT", "RT", "MT", "PT", "ET"]}},
        {"code": "ASTM E569", "specs": {"application": "Acoustic Emission Monitoring", "systems": ["MONPAC", "TankPAC"]}},
        {"code": "ASTM E1417", "specs": {"method": "Liquid Penetrant", "sensitivity": "Level 1-4"}},
        {"code": "ASTM E1444", "specs": {"method": "Magnetic Particle", "technique": "Visible/Fluorescent"}},
        {"code": "ASTM E1742", "specs": {"method": "Radiographic", "equipment": "X-Ray, Gamma, Digital"}},
        {"code": "API 510", "specs": {"service": "Pressure Vessel Inspection"}},
        {"code": "API 570", "specs": {"service": "Piping Inspection"}},
        {"code": "API 653", "specs": {"service": "Aboveground Storage Tank Inspection"}},
        {"code": "ISO 17025", "specs": {"accreditation": ["A2LA", "UKAS", "DAkkS", "COFRAC"]}}
    ]

    # Special handling for ISO 17025 if not in standards_map (might exist with different code)
    iso_id = get_id("standards", "code", "ISO/IEC 17025")
    if iso_id:
        standards_map["ISO 17025"] = iso_id

    for cap in capabilities:
        std_code = cap['code']
        if std_code not in standards_map:
            # Try to find by code exact match if it was already there
            std_id = get_id("standards", "code", std_code)
            if std_id:
                standards_map[std_code] = std_id
            else:
                print(f"  ⚠️  Standard {std_code} not found, skipping capability.")
                continue
        
        std_id = standards_map[std_code]
        
        # Check if capability already exists
        url = f"{SUPABASE_URL}/rest/v1/listing_capabilities"
        params = {"listing_id": f"eq.{mistras_listing_id}", "standard_id": f"eq.{std_id}"}
        resp = requests.get(url, headers=headers, params=params)
        
        if not resp.json():
            cap_data = {
                "listing_id": mistras_listing_id,
                "standard_id": std_id,
                "specifications": cap['specs'],
                "verified": True
            }
            response = requests.post(url, headers=headers, json=cap_data)
            if response.status_code in [200, 201]:
                print(f"    ✅ Linked: {std_code}")
            else:
                print(f"    ❌ Failed to link {std_code}: {response.text}")
        else:
            print(f"    ⏭️  Capability {std_code} already linked.")

    # 5. Add to multiple categories
    print("\n🏷️  Adding multi-category associations...")
    other_cats = ["materials-testing", "oil-gas-testing", "engineering-services", "hydrogen-infrastructure-testing"]
    for cat_slug in other_cats:
        target_cat_id = get_id("categories", "slug", cat_slug)
        if target_cat_id:
            # Check if association exists
            url = f"{SUPABASE_URL}/rest/v1/listing_categories"
            params = {"listing_id": f"eq.{mistras_listing_id}", "category_id": f"eq.{target_cat_id}"}
            resp = requests.get(url, headers=headers, params=params)
            
            if not resp.json():
                assoc_data = {
                    "listing_id": mistras_listing_id,
                    "category_id": target_cat_id,
                    "is_primary": (cat_slug == "ndt-testing-inspection")
                }
                response = requests.post(url, headers=headers, json=assoc_data)
                if response.status_code in [200, 201]:
                    print(f"    ✅ Associated with: {cat_slug}")
                else:
                    print(f"    ❌ Failed to associate with {cat_slug}: {response.text}")
            else:
                print(f"    ⏭️  Association with {cat_slug} already exists.")

    print("\n✨ Mistras Group integration complete!")

if __name__ == "__main__":
    main()
