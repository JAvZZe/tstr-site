#!/usr/bin/env python3
"""
Expand Intertek, Bureau Veritas, and TÜV SÜD listings with detailed NDT/Asset Integrity data.
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
    print("🚀 Expanding Intertek, Bureau Veritas, and TÜV SÜD NDT profiles...\n")

    ndt_cat_id = get_id("categories", "slug", "ndt-testing-inspection")
    
    # 1. Add/Sync Additional Standards
    new_standards = [
        {"code": "API 579", "name": "Fitness-For-Service", "standard_type": "compliance", "category_id": ndt_cat_id},
        {"code": "ASME Section XI", "name": "Rules for Inservice Inspection of Nuclear Power Plant Components", "standard_type": "compliance", "category_id": ndt_cat_id},
        {"code": "ISO 14001", "name": "Environmental management systems", "standard_type": "compliance", "category_id": ndt_cat_id},
        {"code": "ISO 45001", "name": "Occupational health and safety management systems", "standard_type": "compliance", "category_id": ndt_cat_id}
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
    for code in ["ASNT SNT-TC-1A", "ISO 9712", "API 510", "API 570", "API 653", "API 580", "ISO 55001", "ISO 17025"]:
        std_id = get_id("standards", "code", code)
        if std_id:
            standards_map[code] = std_id

    # 2. Update Intertek
    intertek_id = "59a9e7a2-64ad-407f-9d63-679e242646b1"
    print(f"🏢 Updating Intertek (ID: {intertek_id})...")
    intertek_data = {
        "description": "Intertek is a leading Total Quality Assurance provider to industries worldwide. Their Asset Integrity Management (AIM) services help owners and operators maximize asset life and optimize maintenance through data-driven insights. Intertek's proprietary Aware™ software suite provides a comprehensive platform for Asset Performance Management (APM), tracking inspection, repair, and Risk-Based Inspection (RBI) data. With deep expertise in Fitness-for-Service (FFS) according to API 579 and specialized NDT methods, Intertek supports the power, oil & gas, and renewable energy sectors in maintaining structural integrity and safety.",
        "plan_type": "premium",
        "billing_tier": "enterprise",
        "is_featured": True,
        "region": "global"
    }
    if update_listing(intertek_id, intertek_data):
        print("  ✅ Intertek profile updated.")

    # 3. Update Bureau Veritas
    bv_id = "56b84bef-27d4-44d4-a07c-73b2f7e1be87"
    print(f"🏢 Updating Bureau Veritas (ID: {bv_id})...")
    bv_data = {
        "description": "Bureau Veritas is a world leader in laboratory testing, inspection, and certification services. Their Asset Integrity Management solutions focus on the entire lifecycle of industrial, marine, and offshore assets. Bureau Veritas leverages the Veristar brand of digital tools, including Veristar AIM 3D, which creates advanced digital twins to visualize asset health and optimize Risk-Based Inspection (RBI). By integrating smart data with Condition-Based Maintenance (CBM), they help clients reduce operational risks and costs while ensuring compliance with global regulatory standards and structural integrity requirements.",
        "plan_type": "premium",
        "billing_tier": "enterprise",
        "is_featured": True,
        "region": "global"
    }
    if update_listing(bv_id, bv_data):
        print("  ✅ Bureau Veritas profile updated.")

    # 4. Update TÜV SÜD
    tuv_id = "a837f837-5b02-4c04-a0e8-546316067587"
    print(f"🏢 Updating TÜV SÜD (ID: {tuv_id})...")
    tuv_data = {
        "business_name": "TÜV SÜD - Asset Integrity & Testing",
        "description": "TÜV SÜD is a premium quality, safety, and sustainability solutions provider. Their Asset Integrity Management (AIM) strategy focuses on ensuring high plant availability and safety through digital-based predictive analytics. A key differentiator is T-REMS (TÜV SÜD Remote Engineering and Monitoring System), a proprietary digital platform that integrates advanced NDT data with real-time monitoring. TÜV SÜD provides end-to-end support for energy, chemical, and manufacturing infrastructure, combining conventional and advanced NDT methods with Risk-Based Inspection (RBI) to identify vulnerabilities before they lead to unscheduled outages.",
        "plan_type": "premium",
        "billing_tier": "enterprise",
        "is_featured": True,
        "region": "global"
    }
    if update_listing(tuv_id, tuv_data):
        print("  ✅ TÜV SÜD profile updated.")

    # 5. Link Capabilities
    listings = [
        {
            "id": intertek_id, 
            "name": "Intertek",
            "caps": [
                {"code": "ASNT SNT-TC-1A", "specs": {"methods": ["UT", "RT", "MT", "PT", "ET"]}},
                {"code": "API 579", "specs": {"service": "Fitness-For-Service (FFS) Evaluations"}},
                {"code": "API 580", "specs": {"methodology": "RBI via Aware™ APM"}},
                {"code": "ISO 55001", "specs": {"software": ["Aware™", "PipeAware™", "WindAware"]}},
                {"code": "API 510", "specs": {"service": "Pressure Vessel Inspection"}}
            ]
        },
        {
            "id": bv_id,
            "name": "Bureau Veritas",
            "caps": [
                {"code": "ASNT SNT-TC-1A", "specs": {"methods": ["UT", "RT", "MT", "PT", "Drone"]}},
                {"code": "API 580", "specs": {"service": "Risk-Based Inspection (RBI)"}},
                {"code": "ISO 55001", "specs": {"software": ["Veristar AIM 3D", "Veristar Hull", "UTM Data Platform"]}},
                {"code": "ISO 9712", "specs": {"certification": "NDT Personnel Qualification"}},
                {"code": "API 653", "specs": {"service": "Storage Tank Integrity"}}
            ]
        },
        {
            "id": tuv_id,
            "name": "TÜV SÜD",
            "caps": [
                {"code": "ASNT SNT-TC-1A", "specs": {"methods": ["UT", "RT", "MT", "PT", "AE", "ET"]}},
                {"code": "API 580", "specs": {"service": "Risk-Based Inspection (RBI)"}},
                {"code": "ISO 55001", "specs": {"software": ["T-REMS"]}},
                {"code": "ASME Section XI", "specs": {"sector": "Nuclear Power Plant Inspection"}},
                {"code": "API 510", "specs": {"service": "Pressure Vessel Integrity"}}
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
