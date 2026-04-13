#!/usr/bin/env python3
"""
Add Subsea Integrity and Acoustics/Vibration specialized listings and standards.
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
    print("🚀 Adding Subsea & Acoustics Testing Specializations...\n")

    # 1. Create Categories
    print("📁 Syncing Specialized categories...")
    # Subsea Integrity (Extension of Subsea & Offshore)
    subsea_parent_id = get_id("categories", "slug", "subsea-offshore-testing")
    sub_int_id = get_id("categories", "slug", "subsea-pipeline-integrity")
    if not sub_int_id:
        resp = requests.post(f"{SUPABASE_URL}/rest/v1/categories", headers=headers, json={
            "name": "Subsea Pipeline & Asset Integrity",
            "slug": "subsea-pipeline-integrity",
            "parent_id": subsea_parent_id,
            "description": "Specialized deepwater NDT, through-coating pipeline inspection, and underwater structural health monitoring."
        })
        sub_int_id = resp.json()[0]['id']
        print(f"  ✅ Created Subsea Integrity category: {sub_int_id}")

    # Acoustics & Vibration
    acoustics_id = get_id("categories", "slug", "acoustics-vibration-testing")
    if not acoustics_id:
        resp = requests.post(f"{SUPABASE_URL}/rest/v1/categories", headers=headers, json={
            "name": "Acoustics, Vibration & Seismic Testing",
            "slug": "acoustics-vibration-testing",
            "description": "Specialized labs for high-fidelity NVH measurement, triaxial seismic simulation, and environmental qualification for safety-critical assets."
        })
        acoustics_id = resp.json()[0]['id']
        print(f"  ✅ Created Acoustics category: {acoustics_id}")

    # 2. Add Standards
    print("\n📜 Adding Specialized Standards...")
    new_standards = [
        {"code": "ISO 3744", "name": "Acoustics — Determination of sound power levels and sound energy levels of noise sources using sound pressure", "standard_type": "test_method", "category_id": acoustics_id},
        {"code": "IEC 60980", "name": "Recommended practices for seismic qualification of electrical equipment of the safety system for nuclear generating stations", "standard_type": "compliance", "category_id": acoustics_id},
        {"code": "DNV-RP-F116", "name": "Integrity management of submarine pipeline systems", "standard_type": "compliance", "category_id": sub_int_id},
        {"code": "IMCA D 006", "name": "Code of practice for the use of high pressure water jetting equipment by divers", "standard_type": "compliance", "category_id": sub_int_id},
        {"code": "ISO 16283", "name": "Acoustics — Field measurement of sound insulation in buildings and of building elements", "standard_type": "test_method", "category_id": acoustics_id}
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
        {"code": "SUBSEA-NDT", "name": "Subsea NDT & Inspection", "standard_type": "certification"},
        {"code": "THROUGH-COATING", "name": "Through-Coating Inspection (ART)", "standard_type": "certification"},
        {"code": "SEISMIC-QUAL", "name": "Seismic Qualification", "standard_type": "certification"},
        {"code": "NVH-ANALYSIS", "name": "Noise, Vibration & Harshness", "standard_type": "certification"},
        {"code": "MODAL-TESTING", "name": "Structural Modal Analysis", "standard_type": "certification"}
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
            "business_name": "DeepOcean",
            "slug": "deepocean",
            "website": "https://www.deepoceangroup.com/",
            "description": "DeepOcean is a leading subsea IMR (Inspection, Maintenance, and Repair) provider. Specializing in high-resolution pipeline and structural inspection, they utilize advanced ROV platforms and photogrammetry for 3D visualization of subsea assets. DeepOcean operates a state-of-the-art Remote Operations Center (ROC), enabling onshore control of deepwater NDT and integrity monitoring for global energy operators.",
            "category_id": sub_int_id,
            "caps": ["DNV-RP-F116", "SUBSEA-NDT", "MODAL-TESTING"]
        },
        {
            "business_name": "i-Tech 7",
            "slug": "itech7-subsea",
            "website": "https://www.subsea7.com/en/our-business/i-tech-7.html",
            "description": "i-Tech 7 (a Subsea7 company) provides world-class Life of Field services, specializing in unpiggable pipeline inspection and advanced NDT validation. They leverage breakthrough Acoustic Resonance Technology (ARTEMIS™) for precise through-coating wall thickness measurement and subsea phased array (SPA™) for defect characterization. Their digital-first approach provides real-time Topsides data feeds for complex asset integrity audits.",
            "category_id": sub_int_id,
            "caps": ["DNV-RP-F116", "IMCA D 006", "THROUGH-COATING", "SUBSEA-NDT"]
        },
        {
            "business_name": "HBK",
            "slug": "hbk-world",
            "website": "https://www.hbkworld.com/",
            "description": "HBK (Hottinger Brüel & Kjær) is the global gold standard for noise, vibration, and harshness (NVH) engineering. They provide comprehensive structural testing, modal analysis, and sound power determination (ISO 3744). HBK's Application Research Centres (ARC) support the aerospace, automotive, and defense sectors with high-precision sensors, digital data acquisition, and specialized consultancy for operational integrity.",
            "category_id": acoustics_id,
            "caps": ["ISO 3744", "ISO 16283", "NVH-ANALYSIS", "MODAL-TESTING"]
        },
        {
            "business_name": "Sopemea",
            "slug": "sopemea-apave",
            "website": "https://www.sopemea.com/",
            "description": "Sopemea (an Apave Group company) is Europe's leading specialist in seismic testing and environmental qualification. Operating world-class labs with triaxial seismic tables and high-capacity electrodynamic vibrators (up to 300 kN), Sopemea provides critical validation for nuclear, aerospace, and defense hardware. They offer digital twin simulation and combined vibration/climatic testing to ensure equipment reliability in extreme environments.",
            "category_id": acoustics_id,
            "caps": ["IEC 60980", "SEISMIC-QUAL", "NVH-ANALYSIS"]
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
        
        # Link Categories
        for cat_id in [ld['category_id'], get_id("categories", "slug", "ndt-testing-inspection"), get_id("categories", "slug", "engineering-services")]:
            if cat_id:
                check = requests.get(f"{SUPABASE_URL}/rest/v1/listing_categories?listing_id=eq.{lid}&category_id=eq.{cat_id}", headers=headers).json()
                if not check:
                    requests.post(f"{SUPABASE_URL}/rest/v1/listing_categories", headers=headers, json={
                        "listing_id": lid,
                        "category_id": cat_id,
                        "is_primary": (cat_id == ld['category_id'])
                    })

    # Update existing Oceaneering and Element
    print("\n🔄 Updating existing Oceaneering and Element with Subsea/Acoustic context...")
    # Oceaneering
    lid = get_id("listings", "slug", "oceaneering")
    if lid:
        requests.post(f"{SUPABASE_URL}/rest/v1/listing_categories", headers=headers, json={
            "listing_id": lid,
            "category_id": sub_int_id,
            "is_primary": False
        })
        requests.post(f"{SUPABASE_URL}/rest/v1/listing_capabilities", headers=headers, json={
            "listing_id": lid,
            "standard_id": standards_map["SUBSEA-NDT"],
            "verified": True
        })
        print("  ✅ Updated Oceaneering")
    
    # Element
    lid = get_id("listings", "slug", "element-materials---embrittlement-lab")
    if lid:
        requests.post(f"{SUPABASE_URL}/rest/v1/listing_categories", headers=headers, json={
            "listing_id": lid,
            "category_id": acoustics_id,
            "is_primary": False
        })
        requests.post(f"{SUPABASE_URL}/rest/v1/listing_capabilities", headers=headers, json={
            "listing_id": lid,
            "standard_id": standards_map["NVH-ANALYSIS"],
            "verified": True
        })
        print("  ✅ Updated Element")

    print("\n✨ Sector expansion complete!")

if __name__ == "__main__":
    main()
