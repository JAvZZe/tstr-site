#!/usr/bin/env python3
"""
Add Calibration/Metrology and Hydraulic/Pneumatic specialized listings and standards.
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

def main():
    print("🚀 Adding Calibration & Hydraulic Testing Specializations...\n")

    # 1. Create Categories
    print("📁 Syncing Specialized categories...")
    # Calibration
    cal_id = get_id("categories", "slug", "calibration-metrology-services")
    if not cal_id:
        resp = requests.post(f"{SUPABASE_URL}/rest/v1/categories", headers=headers, json={
            "name": "Calibration & Metrology Services",
            "slug": "calibration-metrology-services",
            "description": "Accredited laboratories for high-precision calibration, dimensional metrology, and instrument asset management."
        })
        cal_id = resp.json()[0]['id']
        print(f"  ✅ Created Calibration category: {cal_id}")

    # Hydraulic
    eng_parent_id = get_id("categories", "slug", "engineering-services")
    hyd_id = get_id("categories", "slug", "hydraulic-pneumatic-testing")
    if not hyd_id:
        resp = requests.post(f"{SUPABASE_URL}/rest/v1/categories", headers=headers, json={
            "name": "Hydraulic & Pneumatic Testing",
            "slug": "hydraulic-pneumatic-testing",
            "parent_id": eng_parent_id,
            "description": "Specialized validation for fluid power systems, high-pressure valves, fittings, and filtration components."
        })
        hyd_id = resp.json()[0]['id']
        print(f"  ✅ Created Hydraulic category: {hyd_id}")

    # 2. Add Standards
    print("\n📜 Adding Specialized Standards...")
    # ISO 17025 already handled in previous phases
    new_standards = [
        {"code": "ISO 9001", "name": "Quality management systems — Requirements", "standard_type": "compliance", "category_id": cal_id},
        {"code": "ANSI/ASHRAE 199", "name": "Method of Testing the Performance of Industrial Pulse-Cleaned Dust Collectors", "standard_type": "test_method", "category_id": hyd_id},
        {"code": "ISO 15001", "name": "Anaesthetic and respiratory equipment — Compatibility with oxygen", "standard_type": "compliance", "category_id": hyd_id},
        {"code": "AAMA 501.1", "name": "Standard Test Method for Water Penetration of Windows, Curtain Walls and Doors Using Dynamic Pressure", "standard_type": "test_method", "category_id": hyd_id},
        {"code": "NIST Traceable", "name": "Calibration Traceable to NIST Standards", "standard_type": "certification", "category_id": cal_id}
    ]

    standards_map = {}
    for std in new_standards:
        std_id = get_id("standards", "code", std['code'])
        if not std_id:
            response = requests.post(f"{SUPABASE_URL}/rest/v1/standards", headers=headers, json=std)
            std_id = response.json()[0]['id']
            print(f"  ✅ Added Standard: {std['code']}")
        standards_map[std['code']] = std_id

    # 3. Add Service Tags
    print("\n🏷️  Adding Specialized Service Tags...")
    service_tags = [
        {"code": "ACCREDITED-CALIBRATION", "name": "Accredited Calibration (ISO 17025)", "standard_type": "certification"},
        {"code": "DIMENSIONAL-METROLOGY", "name": "3D Dimensional Inspection", "standard_type": "certification"},
        {"code": "HYDROSTATIC-TEST", "name": "High-Pressure Hydrostatic Testing", "standard_type": "certification"},
        {"code": "FLOW-VALIDATION", "name": "Precision Flow Validation", "standard_type": "certification"},
        {"code": "CLEAN-ROOM-ASSEMBLY", "name": "Ultra-High Purity Cleanroom Assembly", "standard_type": "certification"}
    ]
    for st in service_tags:
        sid = get_id("standards", "code", st['code'])
        if not sid:
            resp = requests.post(f"{SUPABASE_URL}/rest/v1/standards", headers=headers, json=st)
            sid = resp.json()[0]['id']
            print(f"  ✅ Added Tag: {st['name']}")
        standards_map[st['code']] = sid

    # 4. Sync Listings
    print("\n🏢 Syncing Specialized Listings...")
    global_loc_id = get_id("locations", "slug", "global")
    
    listings_data = [
        {
            "business_name": "Trescal",
            "slug": "trescal-global",
            "website": "https://www.trescal.com/",
            "description": "Trescal is the global leader in independent calibration services. Operating over 150 accredited laboratories in 25 countries, Trescal provides a single-source solution for measurement, repair, and asset management across 28+ metrological domains. Their expertise serves the aerospace, automotive, and life sciences industries with over 1,100 national accreditations ensuring worldwide data consistency and regulatory compliance.",
            "category_id": cal_id,
            "caps": ["ISO 9001", "NIST Traceable", "ACCREDITED-CALIBRATION", "DIMENSIONAL-METROLOGY"]
        },
        {
            "business_name": "Transcat",
            "slug": "transcat-inc",
            "website": "https://www.transcat.com/",
            "description": "Transcat is a leading North American provider of ISO/IEC 17025 accredited calibration and specialized metrology software. Their proprietary C3 Asset Management platform enables real-time compliance tracking and audit readiness for highly regulated sectors. Transcat’s Centers of Excellence specialize in high-pressure (up to 72,500 PSI) and high-precision electrical calibration, supporting pharmaceutical, aerospace, and energy infrastructure.",
            "category_id": cal_id,
            "caps": ["NIST Traceable", "ACCREDITED-CALIBRATION", "DIMENSIONAL-METROLOGY"]
        },
        {
            "business_name": "Parker Hannifin",
            "slug": "parker-hannifin-testing",
            "website": "https://www.parker.com/",
            "description": "Parker Hannifin provides world-class specialized testing for hydraulic and pneumatic systems through its Aerospace and Filtration groups. Their facilities, including the Slater Industrial Filter Lab, handle performance validation to ANSI/ASHRAE 199 and specialized aerospace component certification. Parker offers comprehensive diagnostic services and a global 'Hose Doctor' network for on-site fluid power system troubleshooting and rapid prototype verification.",
            "category_id": hyd_id,
            "caps": ["ANSI/ASHRAE 199", "HYDROSTATIC-TEST", "FLOW-VALIDATION"]
        },
        {
            "business_name": "Swagelok",
            "slug": "swagelok-testing",
            "website": "https://www.swagelok.com/",
            "description": "Swagelok provides high-fidelity performance testing for valves, fittings, and fluid systems. Their dedicated Product Test Lab conducts extreme pressure (burst), thermal/burn, and mechanical stress evaluations to simulate the most demanding industrial and subsea environments. Swagelok field engineers provide specialized gas distribution audits and compressed gas leak detection using advanced thermal imaging, ensuring the integrity of mission-critical fluid systems.",
            "category_id": hyd_id,
            "caps": ["ISO 15001", "HYDROSTATIC-TEST", "CLEAN-ROOM-ASSEMBLY"]
        }
    ]

    for ld in listings_data:
        lid = get_id("listings", "slug", ld['slug'])
        if not lid:
            resp = requests.post(f"{SUPABASE_URL}/rest/v1/listings", headers=headers, json={
                "business_name": ld['business_name'],
                "slug": ld['slug'],
                "website": ld['website'],
                "description": ld['description'],
                "category_id": ld['category_id'],
                "location_id": global_loc_id,
                "status": "active",
                "verified": True,
                "is_featured": True,
                "plan_type": "premium",
                "billing_tier": "enterprise",
                "region": "global"
            })
            lid = resp.json()[0]['id']
            print(f"  ✅ Created Listing: {ld['business_name']}")
        
        # Link Caps
        for ccode in ld['caps']:
            sid = standards_map.get(ccode)
            if not sid:
                # Fallback check for ISO 17025 if needed
                if ccode == "ACCREDITED-CALIBRATION":
                    sid = get_id("standards", "code", "ISO/IEC 17025")
            
            if sid:
                check = requests.get(f"{SUPABASE_URL}/rest/v1/listing_capabilities?listing_id=eq.{lid}&standard_id=eq.{sid}", headers=headers).json()
                if not check:
                    requests.post(f"{SUPABASE_URL}/rest/v1/listing_capabilities", headers=headers, json={
                        "listing_id": lid,
                        "standard_id": sid,
                        "verified": True
                    })
        
        # Link Categories
        target_cats = [ld['category_id'], get_id("categories", "slug", "ndt-testing-inspection"), get_id("categories", "slug", "engineering-services")]
        for cat_id in target_cats:
            if cat_id:
                check = requests.get(f"{SUPABASE_URL}/rest/v1/listing_categories?listing_id=eq.{lid}&category_id=eq.{cat_id}", headers=headers).json()
                if not check:
                    requests.post(f"{SUPABASE_URL}/rest/v1/listing_categories", headers=headers, json={
                        "listing_id": lid,
                        "category_id": cat_id,
                        "is_primary": (cat_id == ld['category_id'])
                    })

    print("\n✨ Calibration & Hydraulic expansion complete!")

if __name__ == "__main__":
    main()
