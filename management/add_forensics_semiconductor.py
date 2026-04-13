#!/usr/bin/env python3
"""
Add Forensic Engineering and Semiconductor/Materials Characterization specialized listings and standards.
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
    print("🚀 Adding Forensics & Semiconductor Testing Specializations...\n")

    # 1. Create Categories
    print("📁 Syncing Specialized categories...")
    # Forensics
    eng_parent_id = get_id("categories", "slug", "engineering-services")
    forensic_id = get_id("categories", "slug", "forensic-engineering-failure-analysis")
    if not forensic_id:
        resp = requests.post(f"{SUPABASE_URL}/rest/v1/categories", headers=headers, json={
            "name": "Forensic Engineering & Failure Analysis",
            "slug": "forensic-engineering-failure-analysis",
            "parent_id": eng_parent_id,
            "description": "Specialized labs for complex failure investigations, accident reconstruction, and fire protection engineering."
        })
        forensic_id = resp.json()[0]['id']
        print(f"  ✅ Created Forensics category: {forensic_id}")

    # Semiconductors
    mat_parent_id = get_id("categories", "slug", "materials-testing")
    semi_id = get_id("categories", "slug", "advanced-semiconductor-materials-characterization")
    if not semi_id:
        resp = requests.post(f"{SUPABASE_URL}/rest/v1/categories", headers=headers, json={
            "name": "Advanced Semiconductor & Materials Characterization",
            "slug": "advanced-semiconductor-materials-characterization",
            "parent_id": mat_parent_id,
            "description": "High-end surface analysis, trace elemental characterization, and semiconductor failure analysis."
        })
        semi_id = resp.json()[0]['id']
        print(f"  ✅ Created Semiconductor category: {semi_id}")

    # 2. Add Standards
    print("\n📜 Adding Specialized Standards...")
    new_standards = [
        {"code": "ASTM E2332", "name": "Standard Practice for Investigation and Analysis of Physical Component Failures", "standard_type": "test_method", "category_id": forensic_id},
        {"code": "NFPA 921", "name": "Guide for Fire and Explosion Investigations", "standard_type": "compliance", "category_id": forensic_id},
        {"code": "SEMI E54", "name": "Sensor/Actuator Network Standard", "standard_type": "compliance", "category_id": semi_id},
        {"code": "ISO 18115", "name": "Surface chemical analysis", "standard_type": "test_method", "category_id": semi_id},
        {"code": "JEDEC JESD22", "name": "Reliability Test Methods for Packaged Devices", "standard_type": "test_method", "category_id": semi_id}
    ]

    standards_map = {}
    for std in new_standards:
        std_id = get_id("standards", "code", std['code'])
        if not std_id:
            response = requests.post(f"{SUPABASE_URL}/rest/v1/standards", headers=headers, json=std)
            if response.status_code in [200, 201]:
                std_id = response.json()[0]['id']
                print(f"  ✅ Added Standard: {std['code']}")
            else:
                print(f"  ❌ Failed to add Standard: {std['code']}")
        else:
            print(f"  ⏭️ Standard {std['code']} exists.")
        standards_map[std['code']] = std_id

    # 3. Add Service Tags
    print("\n🏷️  Adding Specialized Service Tags...")
    service_tags = [
        {"code": "FAILURE-ANALYSIS", "name": "Complex Failure Analysis", "standard_type": "certification"},
        {"code": "FIRE-INVESTIGATION", "name": "Fire & Explosion Investigation", "standard_type": "certification"},
        {"code": "SURFACE-ANALYSIS", "name": "Surface Analysis (SIMS, XPS, Auger)", "standard_type": "certification"},
        {"code": "FIB-SEM", "name": "FIB-SEM Circuit Edit & Analysis", "standard_type": "certification"}
    ]
    for st in service_tags:
        sid = get_id("standards", "code", st['code'])
        if not sid:
            resp = requests.post(f"{SUPABASE_URL}/rest/v1/standards", headers=headers, json=st)
            if resp.status_code in [200, 201]:
                sid = resp.json()[0]['id']
                print(f"  ✅ Added Tag: {st['name']}")
        else:
            print(f"  ⏭️ Tag {st['name']} exists.")
        standards_map[st['code']] = sid

    # 4. Sync Listings
    print("\n🏢 Syncing Specialized Listings...")
    global_loc_id = get_id("locations", "slug", "global")
    if not global_loc_id:
        global_loc_id = get_id("locations", "name", "Global")
    
    listings_data = [
        {
            "business_name": "Exponent",
            "slug": "exponent",
            "website": "https://www.exponent.com/",
            "description": "Exponent is a premium multidisciplinary engineering and scientific consulting firm that brings together more than 90 technical disciplines. They are a world leader in complex failure analysis, accident reconstruction, and product recall investigations. Their specialized laboratories provide high-fidelity testing for batteries, consumer electronics, and civil infrastructure, ensuring unparalleled rigorous forensic engineering under critical litigation and regulatory scrutiny.",
            "category_id": forensic_id,
            "caps": ["ASTM E2332", "FAILURE-ANALYSIS"]
        },
        {
            "business_name": "Jensen Hughes",
            "slug": "jensen-hughes",
            "website": "https://www.jensenhughes.com/",
            "description": "Jensen Hughes is a global leader in safety, security, and risk-based engineering, specializing in fire protection engineering and forensic investigation. They provide high-level fire and explosion investigation (NFPA 921) alongside large-scale fire testing to validate complex building assemblies. Their proprietary modeling tools and world-class forensic experts evaluate catastrophic incidents across industrial, commercial, and nuclear environments.",
            "category_id": forensic_id,
            "caps": ["NFPA 921", "FAILURE-ANALYSIS", "FIRE-INVESTIGATION"]
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
            if sid:
                check = requests.get(f"{SUPABASE_URL}/rest/v1/listing_capabilities?listing_id=eq.{lid}&standard_id=eq.{sid}", headers=headers).json()
                if not check:
                    requests.post(f"{SUPABASE_URL}/rest/v1/listing_capabilities", headers=headers, json={
                        "listing_id": lid,
                        "standard_id": sid,
                        "verified": True
                    })
        
        # Multi-category
        target_cats = ["engineering-services"]
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

    # Update existing Eurofins EAG
    print("\n🔄 Updating existing EAG Laboratories profile...")
    eag_id = get_id("listings", "slug", "eag-laboratories")
    if eag_id:
        eag_update = {
            "description": "EAG Laboratories, a Eurofins company, is the global leader in materials characterization and semiconductor failure analysis. EAG offers an unparalleled suite of advanced analytical techniques, including Secondary Ion Mass Spectrometry (SIMS), X-ray Photoelectron Spectroscopy (XPS), and FIB-SEM for complex circuit edit and debug. They provide ultra-trace elemental analysis and physical characterization to support the semiconductor, aerospace, and medical device industries.",
            "category_id": semi_id,
            "plan_type": "premium",
            "billing_tier": "enterprise",
            "is_featured": True
        }
        requests.patch(f"{SUPABASE_URL}/rest/v1/listings?id=eq.{eag_id}", headers=headers, json=eag_update)
        print("  ✅ Updated EAG Laboratories with Semiconductor context and Premium tier")
        
        # Add Semiconductor Tags
        tags_to_add = ["SEMI E54", "ISO 18115", "JEDEC JESD22", "SURFACE-ANALYSIS", "FIB-SEM"]
        for tag_code in tags_to_add:
            sid = standards_map.get(tag_code)
            if sid:
                requests.post(f"{SUPABASE_URL}/rest/v1/listing_capabilities", headers=headers, json={
                    "listing_id": eag_id,
                    "standard_id": sid,
                    "verified": True
                })
        
        # Link to new category
        requests.post(f"{SUPABASE_URL}/rest/v1/listing_categories", headers=headers, json={
            "listing_id": eag_id,
            "category_id": semi_id,
            "is_primary": True
        })

    print("\n✨ Forensics & Semiconductor expansion complete!")

if __name__ == "__main__":
    main()
