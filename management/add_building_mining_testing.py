#!/usr/bin/env python3
"""
Add Building/Construction and Mining/Geochemistry specialized listings and standards.
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

def main():
    print("🚀 Adding Building & Mining Testing Specializations...\n")

    # 1. Create Categories
    print("📁 Syncing Specialized categories...")
    # Building
    build_id = get_id("categories", "slug", "building-construction-testing")
    if not build_id:
        resp = requests.post(f"{SUPABASE_URL}/rest/v1/categories", headers=headers, json={
            "name": "Building & Construction Testing",
            "slug": "building-construction-testing",
            "description": "Specialized labs for fire safety, building envelope (facade) validation, structural integrity, and materials testing for the built environment."
        })
        build_id = resp.json()[0]['id']
        print(f"  ✅ Created Building category: {build_id}")

    # Mining
    mining_id = get_id("categories", "slug", "mining-geochemistry-testing")
    if not mining_id:
        resp = requests.post(f"{SUPABASE_URL}/rest/v1/categories", headers=headers, json={
            "name": "Mining & Geochemistry Testing",
            "slug": "mining-geochemistry-testing",
            "description": "Comprehensive analytical services for the mining lifecycle including geochemical assaying, metallurgy, mineralogy, and on-site lab operations."
        })
        mining_id = resp.json()[0]['id']
        print(f"  ✅ Created Mining category: {mining_id}")

    # 2. Add Standards
    print("\n📜 Adding Specialized Standards...")
    new_standards = [
        {"code": "NFPA 285", "name": "Standard Fire Test Method for Evaluation of Fire Propagation Characteristics of Exterior Non-Load-Bearing Wall Assemblies", "standard_type": "test_method", "category_id": build_id},
        {"code": "ASTM E331", "name": "Standard Test Method for Water Penetration of Exterior Windows, Skylights, Doors, and Curtain Walls", "standard_type": "test_method", "category_id": build_id},
        {"code": "UL 10C", "name": "Positive Pressure Fire Tests of Door Assemblies", "standard_type": "test_method", "category_id": build_id},
        {"code": "NI 43-101", "name": "Standards of Disclosure for Mineral Projects", "standard_type": "compliance", "category_id": mining_id},
        {"code": "JORC Code", "name": "Australasian Code for Reporting of Exploration Results, Mineral Resources and Ore Reserves", "standard_type": "compliance", "category_id": mining_id},
        {"code": "ISO 10378", "name": "Copper, lead and zinc sulfide concentrates — Determination of gold and silver contents", "standard_type": "test_method", "category_id": mining_id},
        {"code": "ASTM E1105", "name": "Standard Test Method for Field Determination of Water Penetration of Installed Exterior Windows, Skylights, Doors, and Curtain Walls", "standard_type": "test_method", "category_id": build_id}
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
        {"code": "FIRE-SAFETY", "name": "Fire Safety Testing", "standard_type": "certification"},
        {"code": "BUILDING-ENVELOPE", "name": "Building Envelope & Facade", "standard_type": "certification"},
        {"code": "GEOCHEMICAL-ASSAY", "name": "Geochemical Assaying", "standard_type": "certification"},
        {"code": "METALLURGY-TEST", "name": "Metallurgical Testing", "standard_type": "certification"},
        {"code": "MAPPING-AI", "name": "Geological AI & Mapping", "standard_type": "certification"}
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
            "business_name": "ALS Minerals",
            "slug": "als-minerals",
            "website": "https://www.alsglobal.com/minerals",
            "description": "ALS Minerals is the world's leading provider of geochemical, metallurgical, and mineralogical testing services. Their proprietary digital ecosystem, featuring Webtrieve™, CoreViewer™, and LithoLens AI, provides real-time data integration for global mining projects. ALS specializes in trace-level geochemical analysis, high-precision fire assay, and advanced geometallurgy, supporting the entire mining lifecycle from exploration to production.",
            "category_id": mining_id,
            "caps": ["NI 43-101", "JORC Code", "GEOCHEMICAL-ASSAY", "METALLURGY-TEST", "MAPPING-AI"]
        },
        {
            "business_name": "Element Building Science",
            "slug": "element-building-science",
            "website": "https://www.element.com/industries/construction",
            "description": "Element Building Science provides comprehensive facade and building envelope testing through its global Centers of Excellence. Specializing in high-fidelity mock-up testing, air/water penetration (ASTM E331/E1105), and large-scale fire performance (NFPA 285), Element ensures the durability and safety of modern architectural structures. Their labs are European Notified Bodies (NB 2812) and recognized across North America for fenestration and structural validation.",
            "category_id": build_id,
            "caps": ["NFPA 285", "ASTM E331", "BUILDING-ENVELOPE", "FIRE-SAFETY"]
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
            sid = standards_map[ccode]
            check = requests.get(f"{SUPABASE_URL}/rest/v1/listing_capabilities?listing_id=eq.{lid}&standard_id=eq.{sid}", headers=headers).json()
            if not check:
                requests.post(f"{SUPABASE_URL}/rest/v1/listing_capabilities", headers=headers, json={
                    "listing_id": lid,
                    "standard_id": sid,
                    "verified": True
                })
        
        # Multi-category
        target_cats = ["ndt-testing-inspection", "materials-testing"]
        for cat_slug in target_cats:
            cat_id = get_id("categories", "slug", cat_slug)
            if cat_id:
                check = requests.get(f"{SUPABASE_URL}/rest/v1/listing_categories?listing_id=eq.{lid}&category_id=eq.{cat_id}", headers=headers).json()
                if not check:
                    requests.post(f"{SUPABASE_URL}/rest/v1/listing_categories", headers=headers, json={
                        "listing_id": lid,
                        "category_id": cat_id,
                        "is_primary": False
                    })

    # Update existing UL, SGS, BV, and Intertek
    print("\n🔄 Updating existing UL, SGS, BV, and Intertek with Building/Mining context...")
    for s in ["ul-solutions", "sgs", "bureau-veritas", "intertek"]:
        lid = get_id("listings", "slug", s)
        if lid:
            # All these offer Building & Mining usually.
            # I'll add specific tags.
            tags_to_add = ["FIRE-SAFETY", "BUILDING-ENVELOPE", "GEOCHEMICAL-ASSAY"]
            for tag_code in tags_to_add:
                sid = standards_map[tag_code]
                requests.post(f"{SUPABASE_URL}/rest/v1/listing_capabilities", headers=headers, json={
                    "listing_id": lid,
                    "standard_id": sid,
                    "verified": True
                })
            # Link to new categories
            for cat_id in [build_id, mining_id]:
                requests.post(f"{SUPABASE_URL}/rest/v1/listing_categories", headers=headers, json={
                    "listing_id": lid,
                    "category_id": cat_id,
                    "is_primary": False
                })
            print(f"  ✅ Updated {s} with Building & Mining context")

    print("\n✨ Sector expansion complete!")

if __name__ == "__main__":
    main()
