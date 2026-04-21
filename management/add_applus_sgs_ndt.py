#!/usr/bin/env python3
"""
Expand Applus+ and SGS listings with detailed NDT/Asset Integrity data.
"""
import os

import requests

SUPABASE_URL = "https://haimjeaetrsaauitrhfy.supabase.co"
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

def update_listing(listing_id, data):
    url = f"{SUPABASE_URL}/rest/v1/listings"
    params = {"id": f"eq.{listing_id}"}
    response = requests.patch(url, headers=headers, params=params, json=data)
    return response.status_code in [200, 201, 204]

def main():
    print("🚀 Expanding Applus+ and SGS NDT profiles...\n")

    ndt_cat_id = get_id("categories", "slug", "ndt-testing-inspection")
    
    # 1. Add/Sync Additional Standards
    new_standards = [
        {"code": "API 580", "name": "Risk-Based Inspection", "standard_type": "compliance", "category_id": ndt_cat_id},
        {"code": "API 581", "name": "Risk-Based Inspection Methodology", "standard_type": "compliance", "category_id": ndt_cat_id},
        {"code": "ISO 19011", "name": "Guidelines for auditing management systems", "standard_type": "compliance", "category_id": ndt_cat_id},
        {"code": "ISO 55001", "name": "Asset management — Management systems", "standard_type": "compliance", "category_id": ndt_cat_id}
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
    for code in ["ASNT SNT-TC-1A", "ISO 9712", "API 510", "API 570", "API 653", "ASTM E1417", "ASTM E1444", "ASTM E1742"]:
        std_id = get_id("standards", "code", code)
        if std_id:
            standards_map[code] = std_id

    # 2. Update Applus+
    applus_id = "5c4213fa-a0a0-44b4-be91-00f291b847d4"
    print(f"🏢 Updating Applus+ (ID: {applus_id})...")
    applus_data = {
        "business_name": "Applus+",
        "description": "Applus+ is a global leader in the testing, inspection, and certification sector. Through its specialist division, Applus+ RTD, the company provides world-class Non-Destructive Testing (NDT) and Asset Integrity Management (AIM) solutions. Leveraging proprietary technologies like IWEX (3D Ultrasonic), RTD-INCOTEST (Pulsed Eddy Current), and Rayscan (Real-time Radiography), Applus+ delivers high-fidelity diagnostics for the energy, infrastructure, and aerospace sectors. Their digital ecosystem, including IDMS, Traza+, and NIIPRO, centralizes inspection data to optimize asset lifecycles and ensure regulatory compliance.",
        "plan_type": "premium",
        "billing_tier": "enterprise",
        "is_featured": True,
        "region": "global"
    }
    if update_listing(applus_id, applus_data):
        print("  ✅ Applus+ profile updated.")

    # 3. Update SGS
    sgs_id = "460b3d8a-efa3-49b7-a667-5f1ff6f601af"
    print(f"🏢 Updating SGS (ID: {sgs_id})...")
    sgs_data = {
        "business_name": "SGS",
        "description": "SGS is the world's leading testing, inspection, and certification company. Their comprehensive NDT and Asset Integrity services ensure safety and reliability across global supply chains and industrial operations. SGS utilizes advanced digital tools such as SGS MIMS (Mechanical Integrity Management System), SGS QiiQ (Remote Inspection), and UT FAST for thin-wall pipeline diagnostics. In partnership with Cenosco, SGS implements the market-standard IMS Suite for Risk-Based Inspection (RBI) and Corrosion Management, helping clients meet API-580/581 and OSHA standards while maximizing asset uptime.",
        "plan_type": "premium",
        "billing_tier": "enterprise",
        "is_featured": True,
        "region": "global"
    }
    if update_listing(sgs_id, sgs_data):
        print("  ✅ SGS profile updated.")

    # 4. Link Capabilities for both
    listings = [
        {
            "id": applus_id, 
            "name": "Applus+",
            "caps": [
                {"code": "ASNT SNT-TC-1A", "specs": {"methods": ["UT", "RT", "MT", "PT", "ET", "PEC"]}},
                {"code": "API 580", "specs": {"service": "Risk-Based Inspection (RBI)"}},
                {"code": "API 510", "specs": {"equipment": "Pressure Vessels"}},
                {"code": "API 570", "specs": {"equipment": "Piping Systems"}},
                {"code": "API 653", "specs": {"equipment": "Storage Tanks"}},
                {"code": "ASTM E1742", "specs": {"tech": "Rayscan Real-time RT"}},
                {"code": "ISO 55001", "specs": {"software": ["IDMS", "Traza+", "NIIPRO"]}}
            ]
        },
        {
            "id": sgs_id,
            "name": "SGS",
            "caps": [
                {"code": "ASNT SNT-TC-1A", "specs": {"methods": ["UT", "RT", "MT", "PT", "ET", "AE"]}},
                {"code": "API 580", "specs": {"methodology": "RBI via IMS Suite"}},
                {"code": "API 581", "specs": {"service": "Quantitative RBI"}},
                {"code": "API 510", "specs": {"service": "Mechanical Integrity Management"}},
                {"code": "ISO 17025", "specs": {"scope": "Global Laboratory Network"}},
                {"code": "ISO 55001", "specs": {"software": ["SGS MIMS", "SGS QiiQ", "IMS Suite"]}}
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
                
                # Use UPSERT via POST with header
                cap_data = {
                    "listing_id": item['id'],
                    "standard_id": std_id,
                    "specifications": cap['specs'],
                    "verified": True
                }
                requests.post(url, headers=headers, json=cap_data)
                print(f"    ✅ {std_code}")

    # 5. Multi-category associations
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
                # Check if exists first to avoid pkey violation (since we didn't use upsert for this M:N)
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
