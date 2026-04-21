#!/usr/bin/env python3
"""
Add Environmental/Carbon Sequestration and Telecommunications/5G specialized listings and standards.
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
    print("🚀 Adding Carbon Sequestration & 5G Testing Specializations...\n")

    # 1. Create Categories
    print("📁 Syncing Specialized categories...")
    # Carbon
    env_parent_id = get_id("categories", "slug", "environmental-testing")
    carbon_id = get_id("categories", "slug", "carbon-sequestration-testing")
    if not carbon_id:
        resp = requests.post(f"{SUPABASE_URL}/rest/v1/categories", headers=headers, json={
            "name": "Carbon Sequestration & MRV",
            "slug": "carbon-sequestration-testing",
            "parent_id": env_parent_id,
            "description": "Specialized labs for carbon soil mapping, Monitoring, Reporting and Verification (MRV), and CCUS technology validation."
        })
        carbon_id = resp.json()[0]['id']
        print(f"  ✅ Created Carbon category: {carbon_id}")

    # Telecom
    telecom_id = get_id("categories", "slug", "telecom-5g-testing")
    if not telecom_id:
        resp = requests.post(f"{SUPABASE_URL}/rest/v1/categories", headers=headers, json={
            "name": "Telecommunications & 5G Testing",
            "slug": "telecom-5g-testing",
            "description": "Advanced network validation labs for 5G NR, O-RAN interoperability, and device conformance testing."
        })
        telecom_id = resp.json()[0]['id']
        print(f"  ✅ Created Telecom category: {telecom_id}")

    # 2. Add Standards
    print("\n📜 Adding Specialized Standards...")
    new_standards = [
        {"code": "ISO 14064-1", "name": "Greenhouse gases — Part 1: Specification with guidance at the organization level for quantification and reporting of greenhouse gas emissions and removals", "standard_type": "compliance", "category_id": carbon_id},
        {"code": "Verra VM0042", "name": "Methodology for Improved Agricultural Land Management", "standard_type": "test_method", "category_id": carbon_id},
        {"code": "DNV-RP-A203", "name": "Technology Qualification", "standard_type": "compliance", "category_id": carbon_id},
        {"code": "3GPP Rel-17", "name": "3rd Generation Partnership Project; Technical Specification Group Services and System Aspects; Release 17 Description", "standard_type": "compliance", "category_id": telecom_id},
        {"code": "O-RAN.WG4.IOT", "name": "O-RAN Alliance Working Group 4: Open Fronthaul Interoperability Test Specification", "standard_type": "test_method", "category_id": telecom_id},
        {"code": "IEEE 802.11be", "name": "IEEE Standard for Information technology--Telecommunications and information exchange between systems Local and metropolitan area networks--Specific requirements - Part 11: Wireless LAN Medium Access Control (MAC) and Physical Layer (PHY) Specifications", "standard_type": "compliance", "category_id": telecom_id}
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
        {"code": "SOIL-CARBON-MAPPING", "name": "Soil Carbon Mapping", "standard_type": "certification"},
        {"code": "CCUS-VALIDATION", "name": "CCUS Technology Validation", "standard_type": "certification"},
        {"code": "5G-CONFORMANCE", "name": "5G Device Conformance", "standard_type": "certification"},
        {"code": "ORAN-INTEROP", "name": "O-RAN Interoperability Testing", "standard_type": "certification"},
        {"code": "6G-RESEARCH", "name": "6G Early Research & Sub-THz", "standard_type": "certification"}
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
            "business_name": "Yard Stick PBC",
            "slug": "yard-stick-soil",
            "website": "https://www.useyardstick.com/",
            "description": "Yard Stick provides a scalable, low-cost solution for Monitoring, Reporting, and Verification (MRV) of soil carbon sequestration. Using proprietary in situ spectroscopy and a cloud-enabled spectral probe, Yard Stick reduces measurement costs by over 90% while providing instant soil organic carbon (SOC) levels. Their platform automates stratification and sampling plans, providing a single source of truth for carbon credit verification.",
            "category_id": carbon_id,
            "caps": ["Verra VM0042", "ISO 14064-1", "SOIL-CARBON-MAPPING"]
        },
        {
            "business_name": "Aker Carbon Capture",
            "slug": "aker-carbon-capture",
            "website": "https://akercarboncapture.com/",
            "description": "Aker Carbon Capture is a pure-play carbon capture company with solutions, services, and technologies serving a range of industries with carbon emissions. They operate advanced testing facilities including the Technology Centre Mongstad (TCM) and a Mobile Test Unit (MTU) for on-site validation. Their proprietary amine technology is DNV-qualified, ensuring reliable carbon capture performance for full-scale industrial facilities.",
            "category_id": carbon_id,
            "caps": ["DNV-RP-A203", "ISO 14064-1", "CCUS-VALIDATION"]
        },
        {
            "business_name": "Keysight Technologies",
            "slug": "keysight",
            "website": "https://www.keysight.com/",
            "description": "Keysight Technologies provides a comprehensive ecosystem of hardware, software, and service solutions for the global 5G and O-RAN market. Their KORA (Keysight Open RAN Architect) platform enables end-to-end validation from the radio unit to the core. Keysight specializes in 5G NR signaling, Massive MIMO beamforming analysis, and device conformance testing, accelerating time-to-market for mobile operators and manufacturers.",
            "category_id": telecom_id,
            "caps": ["3GPP Rel-17", "O-RAN.WG4.IOT", "5G-CONFORMANCE", "ORAN-INTEROP"]
        },
        {
            "business_name": "Rohde & Schwarz",
            "slug": "rohde-schwarz",
            "website": "https://www.rohde-schwarz.com/",
            "description": "Rohde & Schwarz is a global leader in wireless communication testing, providing high-precision solutions for 5G NR and early 6G research. Their portfolio includes vector signal generators, spectrum analyzers, and network scanners for site acceptance and optimization. They are pioneers in sub-THz testing and AI-native air interface validation, supporting the entire lifecycle from chipset R&D to live network monitoring.",
            "category_id": telecom_id,
            "caps": ["3GPP Rel-17", "IEEE 802.11be", "5G-CONFORMANCE", "6G-RESEARCH"]
        },
        {
            "business_name": "Spirent Communications",
            "slug": "spirent",
            "website": "https://www.spirent.com/",
            "description": "Spirent Communications provides automated test and assurance solutions for networks, cybersecurity, and positioning. Their Landslide platform is the industry standard for emulating 5G Core network functions and massive subscriber traffic. Spirent specializes in O-RAN interoperability, RIC validation, and cloud-native infrastructure resiliency testing, ensuring carrier-grade performance for disaggregated 5G networks.",
            "category_id": telecom_id,
            "caps": ["3GPP Rel-17", "O-RAN.WG4.IOT", "ORAN-INTEROP"]
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
        target_cats = ["engineering-services"]
        if ld['category_id'] == carbon_id:
            target_cats.append("renewables-environment")
        
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

    # Update existing DNV and SGS with Carbon context
    print("\n🔄 Updating existing DNV and SGS with Carbon context...")
    for s in ["dnv", "sgs"]:
        lid = get_id("listings", "slug", s)
        if lid:
            requests.post(f"{SUPABASE_URL}/rest/v1/listing_capabilities", headers=headers, json={
                "listing_id": lid,
                "standard_id": standards_map["CCUS-VALIDATION"],
                "verified": True
            })
            requests.post(f"{SUPABASE_URL}/rest/v1/listing_categories", headers=headers, json={
                "listing_id": lid,
                "category_id": carbon_id,
                "is_primary": False
            })
            print(f"  ✅ Updated {s} with Carbon Sequestration context")

    print("\n✨ Sector expansion complete!")

if __name__ == "__main__":
    main()
