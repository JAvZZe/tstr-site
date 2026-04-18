import os
#!/usr/bin/env python3
"""
Add Subsea/Marine and EV/Battery specialized listings and standards.
"""

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
    print("🚀 Adding Subsea & EV Battery Specializations...\n")

    # 1. Create Categories
    print("📁 Syncing Specialized categories...")
    # Subsea
    eng_parent_id = get_id("categories", "slug", "engineering-services")
    subsea_id = get_id("categories", "slug", "subsea-offshore-testing")
    if not subsea_id:
        resp = requests.post(f"{SUPABASE_URL}/rest/v1/categories", headers=headers, json={
            "name": "Subsea & Offshore Testing",
            "slug": "subsea-offshore-testing",
            "parent_id": eng_parent_id,
            "description": "Specialized testing and inspection for subsea production systems, pipelines, and offshore structures."
        })
        subsea_id = resp.json()[0]['id']
        print(f"  ✅ Created Subsea sub-category: {subsea_id}")

    # EV/Battery
    ev_id = get_id("categories", "slug", "ev-battery-testing")
    if not ev_id:
        resp = requests.post(f"{SUPABASE_URL}/rest/v1/categories", headers=headers, json={
            "name": "EV & Battery Safety Testing",
            "slug": "ev-battery-testing",
            "description": "Specialized testing for electric vehicle batteries, propulsion systems, and energy storage safety."
        })
        ev_id = resp.json()[0]['id']
        print(f"  ✅ Created EV/Battery category: {ev_id}")

    # 2. Add Standards
    print("\n📜 Adding Specialized Standards...")
    new_standards = [
        {"code": "DNV-ST-F101", "name": "Submarine pipeline systems", "standard_type": "compliance", "category_id": subsea_id},
        {"code": "API 17D", "name": "Design and Operation of Subsea Production Systems—Subsea Wellhead and Tree Equipment", "standard_type": "compliance", "category_id": subsea_id},
        {"code": "UN 38.3", "name": "Recommendations on the Transport of Dangerous Goods - Lithium Batteries", "standard_type": "certification", "category_id": ev_id},
        {"code": "ECE R100", "name": "Uniform provisions concerning the approval of vehicles with regard to specific requirements for the electric power train", "standard_type": "compliance", "category_id": ev_id},
        {"code": "SAE J2464", "name": "Electric and Hybrid Electric Vehicle Rechargeable Energy Storage System (RESS) Safety and Abuse Testing", "standard_type": "test_method", "category_id": ev_id}
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
        {"code": "SUBSEA-INSPECTION", "name": "Subsea Inspection Services", "standard_type": "certification"},
        {"code": "BATTERY-ABUSE", "name": "Battery Abuse Testing", "standard_type": "certification"},
        {"code": "PROPULSION-TESTING", "name": "EV Propulsion Validation", "standard_type": "certification"}
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
            "business_name": "Oceaneering",
            "slug": "oceaneering",
            "website": "https://www.oceaneering.com/",
            "description": "Oceaneering is a global leader in subsea engineering and applied technology. They provide integrated asset integrity solutions for the offshore energy industry, utilizing advanced ROV-based NDT and specialized subsea inspection tools. Their expertise includes pipeline integrity, splash zone inspection, and structural health monitoring for offshore platforms and subsea production systems.",
            "category_id": subsea_id,
            "caps": ["DNV-ST-F101", "API 17D", "SUBSEA-INSPECTION"]
        },
        {
            "business_name": "FEV",
            "slug": "fev-group",
            "website": "https://www.fev.com/",
            "description": "FEV is a premier global engineering and testing provider for the automotive and energy sectors. Their Sandersdorf-Brehna eDLP facility is the world's largest independent battery development and test center. FEV specializes in complex battery safety testing, including thermal runaway propagation, electrical abuse, and multi-physics simulation-driven safety validation for EV and stationary storage systems.",
            "category_id": ev_id,
            "caps": ["UN 38.3", "ECE R100", "SAE J2464", "BATTERY-ABUSE"]
        },
        {
            "business_name": "UTAC Millbrook",
            "slug": "utac-millbrook",
            "website": "https://www.utac.com/",
            "description": "UTAC Millbrook operates world-class proving grounds and battery test facilities. Specializing in battery abuse testing and full-vehicle validation, they provide critical safety compliance services for the global EV market. Their capabilities include mechanical shock, fire resistance, and full-scale crash testing for electric and fuel cell vehicle prototypes.",
            "category_id": ev_id,
            "caps": ["UN 38.3", "ECE R100", "BATTERY-ABUSE", "PROPULSION-TESTING"]
        },
        {
            "business_name": "Ricardo",
            "slug": "ricardo-plc",
            "website": "https://www.ricardo.com/",
            "description": "Ricardo is a global strategic engineering and environmental consultancy specializing in electrification and propulsion testing. Their Electrified Propulsion Research Centre (EPRC) and Detroit Battery Systems Development Center provide turnkey validation for high-voltage battery packs. Ricardo is a leader in thermal management safety, immersion cooling testing, and ISO 26262 functional safety certification.",
            "category_id": ev_id,
            "caps": ["ECE R100", "BATTERY-ABUSE", "PROPULSION-TESTING"]
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
            # Check if exists
            check = requests.get(f"{SUPABASE_URL}/rest/v1/listing_capabilities?listing_id=eq.{lid}&standard_id=eq.{sid}", headers=headers).json()
            if not check:
                requests.post(f"{SUPABASE_URL}/rest/v1/listing_capabilities", headers=headers, json={
                    "listing_id": lid,
                    "standard_id": sid,
                    "verified": True
                })
        
        # Multi-category
        target_cats = ["ndt-testing-inspection", "engineering-services", "materials-testing"]
        if ld['category_id'] == ev_id:
            target_cats.append("renewable-energy-testing")
        
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

    # Update existing AVL and HORIBA
    print("\n🔄 Updating existing AVL and HORIBA profiles...")
    # AVL
    avl_id = get_id("listings", "slug", "avl")
    if avl_id:
        requests.post(f"{SUPABASE_URL}/rest/v1/listing_capabilities", headers=headers, json={
            "listing_id": avl_id,
            "standard_id": standards_map["PROPULSION-TESTING"],
            "verified": True
        })
        print("  ✅ Updated AVL with Propulsion Tag")
    
    # HORIBA
    horiba_id = get_id("listings", "slug", "horiba-uk-ltd")
    if horiba_id:
        requests.post(f"{SUPABASE_URL}/rest/v1/listing_capabilities", headers=headers, json={
            "listing_id": horiba_id,
            "standard_id": standards_map["BATTERY-ABUSE"],
            "verified": True
        })
        print("  ✅ Updated HORIBA with Battery Abuse Tag")

    print("\n✨ Specialized expansion complete!")

if __name__ == "__main__":
    main()
