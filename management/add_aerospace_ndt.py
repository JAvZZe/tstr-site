#!/usr/bin/env python3
"""
Add Aerospace NDT specialized listings and standards.
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
    print("🚀 Adding Aerospace NDT Specialization...\n")

    # 1. Create Aerospace Categories
    print("📁 Creating Aerospace categories...")
    # Parent
    aero_id = get_id("categories", "slug", "aerospace-testing")
    if not aero_id:
        resp = requests.post(f"{SUPABASE_URL}/rest/v1/categories", headers=headers, json={
            "name": "Aerospace Testing",
            "slug": "aerospace-testing",
            "description": "Specialized testing, inspection, and certification services for the aerospace and defense industry."
        })
        aero_id = resp.json()[0]['id']
        print(f"  ✅ Created Aerospace Testing: {aero_id}")

    # Sub-category
    ndt_aero_id = get_id("categories", "slug", "aerospace-ndt-services")
    if not ndt_aero_id:
        resp = requests.post(f"{SUPABASE_URL}/rest/v1/categories", headers=headers, json={
            "name": "Aerospace NDT & Lab Services",
            "slug": "aerospace-ndt-services",
            "parent_id": aero_id,
            "description": "High-precision non-destructive testing (NDT) services specifically for aircraft components, engines, and structures."
        })
        ndt_aero_id = resp.json()[0]['id']
        print(f"  ✅ Created Aerospace NDT sub-category: {ndt_aero_id}")

    # 2. Add Aerospace Standards
    print("\n📜 Adding Aerospace Standards...")
    new_standards = [
        {"code": "AMS 2644", "name": "Inspection Material, Penetrant", "standard_type": "certification", "category_id": ndt_aero_id},
        {"code": "AMS 3041", "name": "Magnetic Particles, Wet Method, Oil Vehicle", "standard_type": "certification", "category_id": ndt_aero_id},
        {"code": "ASTM E3022", "name": "Standard Practice for Measurement of Emission Characteristics and Requirements for LED UV Lamps Used in Fluorescent PT/MT", "standard_type": "test_method", "category_id": ndt_aero_id},
        {"code": "NAS 410", "name": "NAS Certification & Qualification of Nondestructive Test Personnel", "standard_type": "certification", "category_id": ndt_aero_id}
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
    print("\n🏷️  Adding Service Tags...")
    service_tags = [
        {"code": "AERO-NDT", "name": "Aerospace NDT Services", "standard_type": "certification"},
        {"code": "COMPUTED-TOMOGRAPHY", "name": "Industrial CT Scanning", "standard_type": "certification"},
        {"code": "EDDY-CURRENT", "name": "Advanced Eddy Current Testing", "standard_type": "certification"}
    ]
    for st in service_tags:
        sid = get_id("standards", "code", st['code'])
        if not sid:
            resp = requests.post(f"{SUPABASE_URL}/rest/v1/standards", headers=headers, json=st)
            sid = resp.json()[0]['id']
            print(f"  ✅ Added Tag: {st['name']}")
        standards_map[st['code']] = sid

    # 4. Add Listings
    print("\n🏢 Adding Aerospace Listings...")
    global_loc_id = get_id("locations", "slug", "global")
    
    listings_data = [
        {
            "business_name": "Magnaflux",
            "slug": "magnaflux",
            "website": "https://www.magnaflux.com/",
            "description": "Magnaflux is a global leader in Liquid Penetrant Testing (PT) and Magnetic Particle Inspection (MT) for the aerospace industry. Providing a complete ecosystem of certified consumables (Zyglo, Magnaglo), equipment, and digital process control software, Magnaflux ensures compliance with rigorous standards such as AMS 2644 and ASTM E1444. Their solutions are critical for the inspection of aircraft engines, landing gear, and structural components worldwide.",
            "caps": ["AMS 2644", "AMS 3041", "ASTM E3022", "NAS 410", "AERO-NDT"]
        },
        {
            "business_name": "Waygate Technologies",
            "slug": "waygate-technologies",
            "website": "https://www.waygate-technologies.com/",
            "description": "Waygate Technologies (a Baker Hughes business) is a world leader in industrial radiography and computed tomography (CT). Specializing in advanced NDT for aerospace, automotive, and electronics, Waygate provides high-resolution imaging and precision metrology through their Phoenix V|tome|x and Speed|scan systems. Their proprietary Rhythm Insight software enables DICONDE-compliant digital workflows, ensuring maximum data integrity and inspection efficiency for complex high-value assets.",
            "caps": ["NAS 410", "AERO-NDT", "COMPUTED-TOMOGRAPHY"]
        },
        {
            "business_name": "Eddyfi Technologies",
            "slug": "eddyfi-technologies",
            "website": "https://www.eddyfi.com/",
            "description": "Eddyfi Technologies (incorporating Zetec) provides the highest-performance Non-Destructive Testing (NDT) inspection technologies in the world. Specializing in advanced Eddy Current (ECT) and Phased Array Ultrasonic Testing (PAUT), Eddyfi serves critical aerospace and power generation sectors. Their UltraVision software and specialized probes provide unparalleled defect characterization for aircraft structures, engine components, and heat exchanger tubing.",
            "caps": ["NAS 410", "AERO-NDT", "EDDY-CURRENT"]
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
                "category_id": ndt_aero_id,
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
            requests.post(f"{SUPABASE_URL}/rest/v1/listing_capabilities", headers=headers, json={
                "listing_id": lid,
                "standard_id": sid,
                "verified": True
            })
        
        # Link Categories
        for cat_slug in ["aerospace-testing", "ndt-testing-inspection"]:
            cat_id = get_id("categories", "slug", cat_slug)
            if cat_id:
                # Check if exists
                check = requests.get(f"{SUPABASE_URL}/rest/v1/listing_categories?listing_id=eq.{lid}&category_id=eq.{cat_id}", headers=headers).json()
                if not check:
                    requests.post(f"{SUPABASE_URL}/rest/v1/listing_categories", headers=headers, json={
                        "listing_id": lid,
                        "category_id": cat_id,
                        "is_primary": False
                    })

    print("\n✨ Aerospace integration complete!")

if __name__ == "__main__":
    main()
