#!/usr/bin/env python3
"""
Add Battery Fire Safety and Product Safety/EMC specialized listings and standards.
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
    print("🚀 Adding Battery Fire & EMC Testing Specializations...\n")

    # 1. Create Categories
    print("📁 Syncing Specialized categories...")
    # Battery Fire
    bat_parent_id = get_id("categories", "slug", "renewable-energy-testing")
    bat_fire_id = get_id("categories", "slug", "battery-fire-safety-testing")
    if not bat_fire_id:
        resp = requests.post(f"{SUPABASE_URL}/rest/v1/categories", headers=headers, json={
            "name": "Battery Fire & Thermal Abuse Testing",
            "slug": "battery-fire-safety-testing",
            "parent_id": bat_parent_id,
            "description": "Specialized destructive testing for thermal runaway, fire propagation (UL 9540A), and large-scale BESS safety validation."
        })
        bat_fire_id = resp.json()[0]['id']
        print(f"  ✅ Created Battery Fire category: {bat_fire_id}")

    # EMC
    emc_id = get_id("categories", "slug", "product-safety-emc-testing")
    if not emc_id:
        resp = requests.post(f"{SUPABASE_URL}/rest/v1/categories", headers=headers, json={
            "name": "Product Safety, EMC & Wireless",
            "slug": "product-safety-emc-testing",
            "description": "Nationally Recognized Testing Laboratories (NRTL) for electrical safety, electromagnetic compatibility, and global wireless certification."
        })
        emc_id = resp.json()[0]['id']
        print(f"  ✅ Created EMC category: {emc_id}")

    # 2. Add Standards
    print("\n📜 Adding Specialized Standards...")
    new_standards = [
        {"code": "UL 9540A", "name": "Test Method for Evaluating Thermal Runaway Fire Propagation in Battery Energy Storage Systems", "standard_type": "test_method", "category_id": bat_fire_id},
        {"code": "UL 1973", "name": "Batteries for Use in Stationary, Vehicle Auxiliary Power and Light Electric Rail (LER) Applications", "standard_type": "compliance", "category_id": bat_fire_id},
        {"code": "IEEE 1547", "name": "Standard for Interconnection and Interoperability of Distributed Energy Resources with Associated Electric Power Systems Interfaces", "standard_type": "compliance", "category_id": bat_fire_id},
        {"code": "FCC Part 15", "name": "Radio Frequency Devices (EMC/RF)", "standard_type": "compliance", "category_id": emc_id},
        {"code": "CISPR 32", "name": "Electromagnetic compatibility of multimedia equipment - Emission requirements", "standard_type": "test_method", "category_id": emc_id},
        {"code": "IEC 60601-1-2", "name": "Medical electrical equipment - Part 1-2: General requirements for basic safety and essential performance - Collateral Standard: Electromagnetic disturbances", "standard_type": "compliance", "category_id": emc_id},
        {"code": "RTCA DO-160", "name": "Environmental Conditions and Test Procedures for Airborne Equipment (EMC Section)", "standard_type": "test_method", "category_id": emc_id}
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
        {"code": "THERMAL-RUNAWAY", "name": "Thermal Runaway Testing", "standard_type": "certification"},
        {"code": "ANECHOIC-CHAMBER", "name": "10m Anechoic Chamber", "standard_type": "certification"},
        {"code": "NRTL-LISTING", "name": "NRTL Safety Listing", "standard_type": "certification"},
        {"code": "SAR-TESTING", "name": "SAR & RF Exposure", "standard_type": "certification"}
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
            "business_name": "DNV BEST Test Center",
            "slug": "dnv-best-center",
            "website": "https://www.dnv.com/services/battery-test-center-1439/",
            "description": "The DNV BEST (Battery and Energy Storage Technology) Test Center is a premier facility for BESS fire safety. Specialized in large-scale destructive testing (UL 9540A), they evaluate thermal runaway propagation and gas flammability for utility-scale storage. Their data supports independent engineering reports and helps developers meet stringent AHJ requirements, such as FDNY, for urban energy storage installations.",
            "category_id": bat_fire_id,
            "caps": ["UL 9540A", "UL 1973", "THERMAL-RUNAWAY"]
        },
        {
            "business_name": "CSA Group",
            "slug": "csa-group-hq",
            "website": "https://www.csagroup.org/",
            "description": "CSA Group is a global leader in battery safety and grid interconnection testing. Their state-of-the-art DER (Distributed Energy Resource) Laboratory in Ohio provides megawatt-scale fire testing and comprehensive validation for EV infrastructure and microgrids. As an OSHA-recognized NRTL, CSA certifies energy storage systems to UL 9540 and IEEE 1547 standards, ensuring safe synchronization with the utility grid.",
            "category_id": bat_fire_id,
            "caps": ["UL 1973", "IEEE 1547", "NRTL-LISTING", "THERMAL-RUNAWAY"]
        },
        {
            "business_name": "Eurofins MET Labs",
            "slug": "eurofins-met-labs",
            "website": "https://www.metlabs.com/",
            "description": "Eurofins MET Labs was the first laboratory recognized as an NRTL in the United States. They operate a global network of specialized facilities equipped with 10-meter semi-anechoic chambers and high-intensity radiated immunity (HIRF) testing environments. MET Labs provides comprehensive product safety, EMC, and wireless certification for the military, medical, and industrial sectors, serving as an FCC Telecommunications Certification Body (TCB).",
            "category_id": emc_id,
            "caps": ["FCC Part 15", "CISPR 32", "RTCA DO-160", "NRTL-LISTING", "ANECHOIC-CHAMBER"]
        },
        {
            "business_name": "TÜV SÜD America",
            "slug": "tuv-sud-america",
            "website": "https://www.tuvsud.com/en-us",
            "description": "TÜV SÜD America provides comprehensive EMC and wireless testing through an extensive network of North American labs. Specializing in 5G, Wi-Fi 6E, and medical device EMC (IEC 60601-1-2), they offer a one-stop solution for global market access (GMA). Their specialized capabilities include SAR exposure assessment, wireless coexistence, and in-situ EMC testing for large industrial machinery.",
            "category_id": emc_id,
            "caps": ["IEC 60601-1-2", "FCC Part 15", "SAR-TESTING", "ANECHOIC-CHAMBER"]
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
        target_cats = [ld['category_id'], get_id("categories", "slug", "engineering-services")]
        if ld['category_id'] == bat_fire_id:
            target_cats.append(get_id("categories", "slug", "renewable-energy-testing"))
        
        for cat_id in target_cats:
            if cat_id:
                check = requests.get(f"{SUPABASE_URL}/rest/v1/listing_categories?listing_id=eq.{lid}&category_id=eq.{cat_id}", headers=headers).json()
                if not check:
                    requests.post(f"{SUPABASE_URL}/rest/v1/listing_categories", headers=headers, json={
                        "listing_id": lid,
                        "category_id": cat_id,
                        "is_primary": (cat_id == ld['category_id'])
                    })

    # Update existing UL Solutions and SGS
    print("\n🔄 Updating existing UL and SGS with Fire/EMC context...")
    for s in ["ul-solutions", "sgs"]:
        lid = get_id("listings", "slug", s)
        if lid:
            # Add fire/emc tags
            for tag_code in ["UL 9540A", "FCC Part 15", "NRTL-LISTING"]:
                sid = standards_map[tag_code]
                requests.post(f"{SUPABASE_URL}/rest/v1/listing_capabilities", headers=headers, json={
                    "listing_id": lid,
                    "standard_id": sid,
                    "verified": True
                })
            # Link to new categories
            for cat_id in [bat_fire_id, emc_id]:
                requests.post(f"{SUPABASE_URL}/rest/v1/listing_categories", headers=headers, json={
                    "listing_id": lid,
                    "category_id": cat_id,
                    "is_primary": False
                })
            print(f"  ✅ Updated {s}")

    print("\n✨ Sector expansion complete!")

if __name__ == "__main__":
    main()
