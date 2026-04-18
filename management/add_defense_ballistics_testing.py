import os
#!/usr/bin/env python3
"""
Add Defense and Ballistics specialized listings and standards.
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
    print("🚀 Adding Defense & Ballistics Testing Specializations...\n")

    # 1. Create Category
    print("📁 Syncing Specialized categories...")
    def_id = get_id("categories", "slug", "defense-ballistics-testing")
    if not def_id:
        resp = requests.post(f"{SUPABASE_URL}/rest/v1/categories", headers=headers, json={
            "name": "Defense & Ballistics Testing",
            "slug": "defense-ballistics-testing",
            "description": "High-security labs for ballistic resistance, ordnance testing, MIL-STD environmental stress screening, and heavyweight shock validation."
        })
        def_id = resp.json()[0]['id']
        print(f"  ✅ Created Defense category: {def_id}")

    # 2. Add Standards
    print("\n📜 Adding Specialized Standards...")
    new_standards = [
        {"code": "MIL-STD-810H", "name": "Environmental Engineering Considerations and Laboratory Tests", "standard_type": "compliance", "category_id": def_id},
        {"code": "MIL-STD-461G", "name": "Requirements for the Control of Electromagnetic Interference Characteristics of Subsystems and Equipment", "standard_type": "compliance", "category_id": def_id},
        {"code": "MIL-DTL-901E", "name": "Shock Tests, H.I. (High-Impact) Shipboard Machinery, Equipment, and Systems", "standard_type": "test_method", "category_id": def_id},
        {"code": "NIJ 0101.06", "name": "Ballistic Resistance of Body Armor", "standard_type": "test_method", "category_id": def_id},
        {"code": "STANAG 4569", "name": "Protection Levels for Occupants of Armoured Vehicles", "standard_type": "compliance", "category_id": def_id},
        {"code": "AAMA 501", "name": "Methods of Test for Exterior Walls", "standard_type": "test_method", "category_id": def_id}
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
        {"code": "BALLISTICS-ORDNANCE", "name": "Ballistics & Ordnance Testing", "standard_type": "certification"},
        {"code": "HEAVYWEIGHT-SHOCK", "name": "Heavyweight Shock (MIL-DTL-901E)", "standard_type": "certification"},
        {"code": "MIL-SPEC-EMC", "name": "MIL-SPEC EMC/EMI Testing", "standard_type": "certification"},
        {"code": "ARMOR-VALIDATION", "name": "Armor & Helmet Validation", "standard_type": "certification"}
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
            "business_name": "Element U.S. Space & Defense",
            "slug": "element-defense",
            "website": "https://www.elementdefense.com/",
            "description": "Element U.S. Space & Defense (incorporating the mission-critical core of NTS) is the premier provider of high-level military and ordnance testing. Operating 6 specialized labs, they provide world-class ballistics, heavyweight shock (MIL-DTL-901E), and high-intensity vibration testing for missiles and space launch systems. Their facilities include a 36-acre quarry for explosive testing and large-scale environmental simulation for extreme mission profiles.",
            "category_id": def_id,
            "caps": ["MIL-STD-810H", "MIL-DTL-901E", "BALLISTICS-ORDNANCE", "MIL-SPEC-EMC"]
        },
        {
            "business_name": "QinetiQ",
            "slug": "qinetiq",
            "website": "https://www.qinetiq.com/",
            "description": "QinetiQ is a world-leading integrated defense and security technology company. They provide extensive Test & Evaluation (T&E) services for weapons, sensors, and aerospace platforms. QinetiQ operates the UK's Long Range Weapons Range and specialized labs for signatures, stealth, and communications validation, ensuring technical superiority and operational readiness for global defense customers.",
            "category_id": def_id,
            "caps": ["MIL-STD-810H", "STANAG 4569", "BALLISTICS-ORDNANCE"]
        },
        {
            "business_name": "Dayton T. Brown",
            "slug": "dayton-t-brown",
            "website": "https://www.dtb.com/",
            "description": "Dayton T. Brown (DTB) provides a comprehensive suite of engineering and testing services for the aerospace, defense, and commercial sectors. Their world-class facilities handle full-spectrum environmental simulation, dynamics, and EMI/EMC testing according to MIL-STD-810 and MIL-STD-461. DTB is a leader in survival equipment validation and specialized technical documentation services for complex military hardware.",
            "category_id": def_id,
            "caps": ["MIL-STD-810H", "MIL-STD-461G", "MIL-SPEC-EMC"]
        },
        {
            "business_name": "Oregon Ballistic Laboratories",
            "slug": "oregon-ballistic-labs",
            "website": "https://www.oregonballisticlaboratories.com/",
            "description": "Oregon Ballistic Laboratories (OBL) is a premier independent ballistics testing facility. Specialized in NIJ certification for body armor and helmets, OBL provides high-fidelity assessment of ballistic resistance, V50 limit determination, and backface signature (BFS) analysis. They serve law enforcement, military, and civilian manufacturers with state-of-the-art range facilities and precision instrumentation.",
            "category_id": def_id,
            "caps": ["NIJ 0101.06", "BALLISTICS-ORDNANCE", "ARMOR-VALIDATION"]
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
        target_cats = ["ndt-testing-inspection", "engineering-services", "aerospace-testing"]
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

    # Update existing Element
    print("\n🔄 Updating existing Element Materials with Defense context...")
    lid = get_id("listings", "slug", "element-materials---embrittlement-lab")
    if lid:
        requests.post(f"{SUPABASE_URL}/rest/v1/listing_categories", headers=headers, json={
            "listing_id": lid,
            "category_id": def_id,
            "is_primary": False
        })
        print("  ✅ Updated Element with Defense category link")

    print("\n✨ Defense & Ballistics expansion complete!")

if __name__ == "__main__":
    main()
