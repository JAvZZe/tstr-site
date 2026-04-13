#!/usr/bin/env python3
"""
Add Renewable Energy (Wind, Solar, BESS) specialized listings and standards.
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
    print("🚀 Adding Renewable Energy Testing Specialization...\n")

    # 1. Create Renewable Category
    print("📁 Syncing Renewable Energy categories...")
    renew_parent_id = get_id("categories", "slug", "renewables-environment")
    
    renew_test_id = get_id("categories", "slug", "renewable-energy-testing")
    if not renew_test_id:
        resp = requests.post(f"{SUPABASE_URL}/rest/v1/categories", headers=headers, json={
            "name": "Renewable Energy Testing & Certification",
            "slug": "renewable-energy-testing",
            "parent_id": renew_parent_id,
            "description": "Specialized testing, certification, and technical advisory for Wind, Solar, and Energy Storage systems."
        })
        renew_test_id = resp.json()[0]['id']
        print(f"  ✅ Created Renewable sub-category: {renew_test_id}")

    # 2. Add Renewable Standards
    print("\n📜 Adding Renewable Standards...")
    new_standards = [
        {"code": "IEC 61400-1", "name": "Wind turbines - Design requirements", "standard_type": "compliance", "category_id": renew_test_id},
        {"code": "IEC 61400-12-1", "name": "Power performance measurements of electricity producing wind turbines", "standard_type": "test_method", "category_id": renew_test_id},
        {"code": "IEC 61215", "name": "Terrestrial photovoltaic (PV) modules - Design qualification and type approval", "standard_type": "certification", "category_id": renew_test_id},
        {"code": "UL 9540A", "name": "Test Method for Evaluating Thermal Runaway Fire Propagation in Battery Energy Storage Systems", "standard_type": "test_method", "category_id": renew_test_id},
        {"code": "VDE-AR-N 4105", "name": "Generators connected to the low-voltage distribution network", "standard_type": "compliance", "category_id": renew_test_id}
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
    print("\n🏷️  Adding Renewable Service Tags...")
    service_tags = [
        {"code": "WIND-ENERGY", "name": "Wind Energy Services", "standard_type": "certification"},
        {"code": "SOLAR-PV", "name": "Solar PV Testing", "standard_type": "certification"},
        {"code": "BESS-SAFETY", "name": "Battery Storage Safety", "standard_type": "certification"},
        {"code": "GRID-CONFORMITY", "name": "Grid Connection Testing", "standard_type": "certification"}
    ]
    for st in service_tags:
        sid = get_id("standards", "code", st['code'])
        if not sid:
            resp = requests.post(f"{SUPABASE_URL}/rest/v1/standards", headers=headers, json=st)
            sid = resp.json()[0]['id']
            print(f"  ✅ Added Tag: {st['name']}")
        standards_map[st['code']] = sid

    # 4. Define Listings
    print("\n🏢 Syncing Renewable Listings...")
    global_loc_id = get_id("locations", "slug", "global")
    
    listings_data = [
        {
            "business_name": "UL Solutions",
            "slug": "ul-solutions",
            "website": "https://www.ul.com",
            "description": "UL Solutions is a global leader in renewable energy testing and certification. Their ecosystem includes the industry-standard HOMER® software for microgrid optimization, Windographer for resource analysis, and Openwind for farm design. UL provides comprehensive type certification for wind turbines and safety testing for PV modules. They are the primary authority for Battery Energy Storage System (BESS) safety, developing the UL 9540 and UL 9540A standards for thermal runaway fire propagation.",
            "caps": ["IEC 61400-1", "IEC 61215", "UL 9540A", "WIND-ENERGY", "SOLAR-PV", "BESS-SAFETY"]
        },
        {
            "business_name": "TÜV Rheinland",
            "slug": "tuv-rheinland",
            "website": "https://www.tuv.com/",
            "description": "TÜV Rheinland is a leading international provider of technical services for the solar industry. With a global network of PV laboratories, they specialize in module reliability testing, energy yield assessment, and 'bankability' reporting for utility-scale projects. Their innovations include the Mobile Solar Lab for on-site electroluminescence imaging and specialized testing for high-efficiency bifacial and HJT modules. They provide technical due diligence and supply chain inspections to ensure quality from factory to field.",
            "caps": ["IEC 61215", "GRID-CONFORMITY", "SOLAR-PV", "BESS-SAFETY"]
        },
        {
            "business_name": "Fraunhofer ISE",
            "slug": "fraunhofer-ise",
            "website": "https://www.ise.fraunhofer.de/",
            "description": "The Fraunhofer Institute for Solar Energy Systems ISE is the largest solar research institute in Europe. Their commercial TestLab PV Modules and CalLab provide ultra-precise power calibration and stress testing for manufacturers worldwide. Fraunhofer ISE also operates a specialized TestLab for Power Electronics, capable of grid connection and stability testing for PV inverters and bidirectional converters up to the multi-megawatt range (10 MVA).",
            "caps": ["IEC 61215", "VDE-AR-N 4105", "GRID-CONFORMITY", "SOLAR-PV"]
        },
        {
            "business_name": "Fraunhofer IWES",
            "slug": "fraunhofer-iwes",
            "website": "https://www.iwes.fraunhofer.de/",
            "description": "Fraunhofer IWES specialized in wind energy system validation. They operate some of the world's largest rotor blade test facilities, capable of handling blades exceeding 120 meters. Their services include uniaxial and biaxial fatigue testing, support structure validation at the TTH Hannover, and geotechnical foundation testing. As an IECRE-accepted laboratory, they provide critical data for wind turbine type certification and risk mitigation.",
            "caps": ["IEC 61400-1", "IEC 61400-12-1", "WIND-ENERGY"]
        },
        {
            "business_name": "VDE Renewables",
            "slug": "vde-renewables",
            "website": "https://www.vde.com/renewables",
            "description": "VDE Renewables provides 'bankability' assurance for the global solar and energy storage markets. Following the acquisition of the US-based RETC (Renewable Energy Test Center), they offer high-end reliability ranking and independent engineering reports. VDE is a primary authority for European grid conformity (VDE-AR-N series) and provides the 'VDE Quality Tested' mark for entire PV power plants, ensuring long-term asset performance and safety.",
            "caps": ["IEC 61215", "VDE-AR-N 4105", "GRID-CONFORMITY", "SOLAR-PV", "BESS-SAFETY"]
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
                "category_id": renew_test_id,
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
        else:
            # Update existing
            requests.patch(f"{SUPABASE_URL}/rest/v1/listings?id=eq.{lid}", headers=headers, json={
                "description": ld['description'],
                "category_id": renew_test_id,
                "plan_type": "premium",
                "billing_tier": "enterprise"
            })
            print(f"  ✅ Updated Listing: {ld['business_name']}")
        
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
        
        # Link Categories
        for cat_slug in ["renewables-environment", "renewable-energy-testing"]:
            cat_id = get_id("categories", "slug", cat_slug)
            if cat_id:
                # Check if exists
                check = requests.get(f"{SUPABASE_URL}/rest/v1/listing_categories?listing_id=eq.{lid}&category_id=eq.{cat_id}", headers=headers).json()
                if not check:
                    requests.post(f"{SUPABASE_URL}/rest/v1/listing_categories", headers=headers, json={
                        "listing_id": lid,
                        "category_id": cat_id,
                        "is_primary": (cat_slug == "renewable-energy-testing")
                    })

    print("\n✨ Renewable Energy integration complete!")

if __name__ == "__main__":
    main()
