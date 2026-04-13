#!/usr/bin/env python3
"""
Expand DNV and DEKRA, and add LRQA with detailed NDT/Asset Integrity data.
"""

import requests

SUPABASE_URL = "https://haimjeaetrsaauitrhfy.supabase.co"
SERVICE_ROLE_KEY = "sb_secret_zRN1fTFOYnN7cEbEIfAP7A_YrEKBfI2"

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

def update_listing(listing_id, data):
    url = f"{SUPABASE_URL}/rest/v1/listings"
    params = {"id": f"eq.{listing_id}"}
    response = requests.patch(url, headers=headers, params=params, json=data)
    return response.status_code in [200, 201, 204]

def main():
    print("🚀 Expanding DNV, DEKRA, and adding LRQA NDT profiles...\n")

    ndt_cat_id = get_id("categories", "slug", "ndt-testing-inspection")
    global_loc_id = get_id("locations", "slug", "global")
    
    # 1. Add/Sync Additional Standards
    new_standards = [
        {"code": "API RP 1173", "name": "Pipeline Safety Management System", "standard_type": "compliance", "category_id": ndt_cat_id},
        {"code": "ISO 10426", "name": "Petroleum and natural gas industries — Cements and materials for well cementing", "standard_type": "test_method", "category_id": ndt_cat_id},
        {"code": "ISO 19880-1", "name": "Gaseous hydrogen — Fuelling stations", "standard_type": "compliance", "category_id": ndt_cat_id}
    ]

    standards_map = {}
    for std in new_standards:
        std_id = get_id("standards", "code", std['code'])
        if not std_id:
            response = requests.post(f"{SUPABASE_URL}/rest/v1/standards", headers=headers, json=std)
            if response.status_code in [200, 201]:
                std_id = response.json()[0]['id']
                print(f"✅ Added Standard: {std['code']}")
        standards_map[std['code']] = std_id

    # Get existing standards for linking
    for code in ["ASNT SNT-TC-1A", "ISO 9712", "API 580", "API 581", "ISO 55001", "ISO 17025", "API 510"]:
        std_id = get_id("standards", "code", code)
        if std_id:
            standards_map[code] = std_id

    # 2. Update DNV
    dnv_id = "33eba0ec-f866-4475-bf5e-919912b485f7"
    print(f"🏢 Updating DNV (ID: {dnv_id})...")
    dnv_data = {
        "description": "DNV is a global independent expert in assurance and risk management. Their Asset Integrity Management (AIM) services are industry-leading, particularly for subsea and pipeline infrastructure. DNV’s Synergi Pipeline software, hosted on the Veracity data platform, provides a central source of truth for risk assessment, anomaly management, and regulatory compliance (API RP 1173). With deep expertise in NDT data integration and predictive analytics, DNV helps operators in the maritime, oil & gas, and energy transition sectors (including Hydrogen) maintain safe and sustainable operations.",
        "plan_type": "premium",
        "billing_tier": "enterprise",
        "is_featured": True,
        "region": "global"
    }
    if update_listing(dnv_id, dnv_data):
        print("  ✅ DNV profile updated.")

    # 3. Update DEKRA
    dekra_id = "735511b6-eae2-4b63-9029-6b80f75068c4"
    print(f"🏢 Updating DEKRA (ID: {dekra_id})...")
    dekra_data = {
        "description": "DEKRA is a global leader in safety, focusing on the entire lifecycle of industrial and automotive assets. Their Non-Destructive Testing (NDT) services combine traditional methods with advanced digital inspection solutions to ensure the integrity of critical components. DEKRA specializes in pressure equipment, power grids, and renewable energy infrastructure, providing expert certification and inspection according to international safety standards. Their industrial inspection platforms enable real-time field data capture and predictive maintenance planning for complex manufacturing and energy facilities.",
        "plan_type": "premium",
        "billing_tier": "enterprise",
        "is_featured": True,
        "region": "global"
    }
    if update_listing(dekra_id, dekra_data):
        print("  ✅ DEKRA profile updated.")

    # 4. Add LRQA
    lrqa_slug = "lrqa-asset-integrity"
    lrqa_id = get_id("listings", "slug", lrqa_slug)
    if not lrqa_id:
        print("🏢 Creating LRQA listing...")
        lrqa_data = {
            "business_name": "LRQA",
            "slug": lrqa_slug,
            "category_id": ndt_cat_id,
            "location_id": global_loc_id,
            "website": "https://www.lrqa.com/",
            "description": "LRQA is a leading global assurance provider, delivering inspection, certification, and NDT services across the energy and maritime sectors. Formerly part of Lloyd's Register, LRQA specializes in Asset Integrity Management, welding certification, and specialized NDT validation (including Matrix Array Ultrasonic Testing). They provide comprehensive technical assurance for complex assets, supporting the transition to clean energy through hydrogen certification and structural health monitoring. Their services ensure compliance with global standards such as API 580/581 and ISO 55001.",
            "status": "active",
            "verified": True,
            "is_featured": True,
            "plan_type": "premium",
            "billing_tier": "enterprise",
            "region": "global"
        }
        response = requests.post(f"{SUPABASE_URL}/rest/v1/listings", headers=headers, json=lrqa_data)
        if response.status_code in [200, 201]:
            lrqa_id = response.json()[0]['id']
            print(f"  ✅ LRQA listing created: {lrqa_id}")
    else:
        print(f"✅ LRQA listing already exists: {lrqa_id}")

    # 5. Link Capabilities
    listings = [
        {
            "id": dnv_id, 
            "name": "DNV",
            "caps": [
                {"code": "API RP 1173", "specs": {"service": "Pipeline Safety Management"}},
                {"code": "API 580", "specs": {"methodology": "RBI via Synergi Pipeline"}},
                {"code": "ISO 55001", "specs": {"software": ["Synergi", "Veracity"]}},
                {"code": "ISO 9712", "specs": {"certification": "NDT Personnel Certification"}},
                {"code": "ISO 19880-1", "specs": {"sector": "Hydrogen Infrastructure"}}
            ]
        },
        {
            "id": dekra_id,
            "name": "DEKRA",
            "caps": [
                {"code": "ASNT SNT-TC-1A", "specs": {"methods": ["UT", "RT", "MT", "PT", "ET"]}},
                {"code": "ISO 17025", "specs": {"scope": "Industrial Testing Labs"}},
                {"code": "API 510", "specs": {"service": "Pressure Equipment Inspection"}},
                {"code": "ISO 19880-1", "specs": {"service": "H2 Station Inspection"}}
            ]
        },
        {
            "id": lrqa_id,
            "name": "LRQA",
            "caps": [
                {"code": "ASNT SNT-TC-1A", "specs": {"methods": ["UT", "RT", "MAUT", "ET"]}},
                {"code": "API 580", "specs": {"service": "Risk-Based Inspection (RBI)"}},
                {"code": "ISO 55001", "specs": {"software": ["Asset Performance Management"]}},
                {"code": "API 510", "specs": {"service": "Pressure Vessel Integrity"}},
                {"code": "ISO 10426", "specs": {"sector": "Maritime Structural Integrity"}}
            ]
        }
    ]

    print("\n🔗 Linking Capabilities...")
    for item in listings:
        print(f"  Linking for {item['name']}...")
        for cap in item['caps']:
            std_code = cap['code']
            if std_code in standards_map:
                std_id = standards_map[std_code]
                url = f"{SUPABASE_URL}/rest/v1/listing_capabilities"
                cap_data = {
                    "listing_id": item['id'],
                    "standard_id": std_id,
                    "specifications": cap['specs'],
                    "verified": True
                }
                requests.post(url, headers=headers, json=cap_data)
                print(f"    ✅ {std_code}")

    # 6. Multi-category associations
    print("\n🏷️  Syncing Categories...")
    cats = ["ndt-testing-inspection", "materials-testing", "oil-gas-testing", "engineering-services", "hydrogen-infrastructure-testing"]
    for item in listings:
        print(f"  Categories for {item['name']}...")
        for slug in cats:
            cat_id = get_id("categories", "slug", slug)
            if cat_id:
                assoc_data = {
                    "listing_id": item['id'],
                    "category_id": cat_id,
                    "is_primary": (slug == "ndt-testing-inspection")
                }
                check_url = f"{SUPABASE_URL}/rest/v1/listing_categories"
                params = {"listing_id": f"eq.{item['id']}", "category_id": f"eq.{cat_id}"}
                if not requests.get(check_url, headers=headers, params=params).json():
                    requests.post(check_url, headers=headers, json=assoc_data)
                    print(f"    ✅ {slug}")
                else:
                    print(f"    ⏭️  {slug}")

    print("\n✨ Expansion complete!")

if __name__ == "__main__":
    main()
