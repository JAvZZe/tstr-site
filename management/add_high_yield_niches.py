#!/usr/bin/env python3
"""
Add High-Yield niche testing providers for Under-served categories.
Aligned with PSEO 2.0 architecture and URL matrix.
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
    if isinstance(data, dict) and "error" in data:
        print(f"Error fetching {table}: {data['error']}")
        return None
    return data[0]['id'] if data else None

def create_if_not_exists(table, field, value, data):
    existing_id = get_id(table, field, value)
    if existing_id:
        return existing_id
    
    response = requests.post(f"{SUPABASE_URL}/rest/v1/{table}", headers=headers, json=data)
    res_data = response.json()
    if isinstance(res_data, list) and len(res_data) > 0:
        return res_data[0]['id']
    else:
        print(f"Failed to create {table} {value}: {res_data}")
        return None

def main():
    print("🚀 Starting High-Yield Listing Ingestion...\n")

    # Define Categories mapping to existing slugs
    categories_data = {
        "battery-fire-safety-testing": {"name": "Battery Fire & Thermal Abuse Testing", "slug": "battery-fire-safety-testing"},
        "subsea-pipeline-integrity": {"name": "Subsea Pipeline & Asset Integrity", "slug": "subsea-pipeline-integrity"},
        "cybersecurity-testing": {"name": "Cybersecurity & Software Testing", "slug": "cybersecurity-testing"},
        "aerospace-ndt-services": {"name": "Aerospace NDT & Lab Services", "slug": "aerospace-ndt-services"},
        "nuclear-testing": {"name": "Nuclear Energy Testing & Inspection", "slug": "nuclear-testing"}
    }

    # Ensure categories exist and get IDs
    cat_ids = {}
    for slug, data in categories_data.items():
        cat_ids[slug] = create_if_not_exists("categories", "slug", slug, data)

    # Define Listings Data
    listings = [
        {
            "company_name": "UL Solutions",
            "slug": "ul-solutions",
            "url": "https://www.ul.com",
            "location_slug": "global",
            "region": "global",
            "category_slug": "battery-fire-safety-testing",
            "industry": "automotive",
            "standards": ["UL 2580", "UN 38.3", "GB 38031"],
            "description": "UL Solutions offers a comprehensive range of electric vehicle (EV) battery testing services, including abuse and fire exposure/thermal propagation and performance testing services at the cell, module and pack levels. High regulatory demand for EV safety ensures zero tolerance for catastrophic failure."
        },
        {
            "company_name": "Element Materials Technology",
            "slug": "element-materials-technology",
            "url": "https://www.element.com",
            "location_slug": "north-america",
            "region": "north-america",
            "category_slug": "battery-fire-safety-testing",
            "industry": "aerospace-automotive",
            "standards": ["ISO 17025", "UN 38.3"],
            "description": "Element provides comprehensive battery safety and abuse testing including internal short circuit evaluation, overcharge testing, crush and impact assessment, nail penetration simulation, and thermal runaway propagation analysis. North America's largest network of purpose-built battery testing facilities."
        },
        {
            "company_name": "DEKRA",
            "slug": "dekra",
            "url": "https://www.dekra.com",
            "location_slug": "germany",
            "region": "europe",
            "category_slug": "battery-fire-safety-testing",
            "industry": "automotive",
            "standards": ["ISO 17025", "UN 38.3"],
            "description": "DEKRA offers all battery abuse tests under one roof with reproducible and safe test conditions. State-of-the-art Battery Test Center includes the largest fire chamber of its kind (360 sq meters), capable of accommodating entire vehicles."
        },
        {
            "company_name": "SERMA Energy",
            "slug": "serma-energy",
            "url": "https://www.serma-energy.com",
            "location_slug": "europe",
            "region": "europe",
            "category_slug": "battery-fire-safety-testing",
            "industry": "automotive",
            "standards": ["ECE R100", "UN 38.3", "UL 1642", "IEC 62133"],
            "description": "SERMA Energy enables the study of battery behavior and reactions beyond specifications, including certification support (ECE R100). Specialized in high-capacity packs up to 150 kWh."
        },
        {
            "company_name": "Stress Engineering Services",
            "slug": "stress-engineering-services",
            "url": "https://www.stress.com",
            "location_slug": "texas",
            "region": "north-america",
            "category_slug": "battery-fire-safety-testing",
            "industry": "aerospace-defense",
            "standards": ["RTCA DO-227a", "UN 38.3", "UL 9540"],
            "description": "SES offers battery safety and performance testing, digging deep into complex electrochemical/thermal systems to improve safety during operation and transportation. Expertise in ITAR testing and standards development."
        },
        {
            "company_name": "Balmoral Subsea Test Centre",
            "slug": "balmoral-subsea-test-centre",
            "url": "https://www.balmoraloffshore.com",
            "location_slug": "europe",
            "region": "europe",
            "category_slug": "subsea-pipeline-integrity",
            "industry": "oil-gas-renewables",
            "standards": ["API 17L1"],
            "description": "The industry's most comprehensive hyperbaric and mechanical testing center. Equipped with 23 vessels for testing to pressures of 700bar, catering to subsea, renewables, and defense sectors."
        },
        {
            "company_name": "MACAW Engineering",
            "slug": "macaw-engineering",
            "url": "https://www.macawengineering.com",
            "location_slug": "europe",
            "region": "europe",
            "category_slug": "subsea-pipeline-integrity",
            "industry": "oil-gas",
            "standards": ["ISO 17025"],
            "description": "Independent engineering consultancy for asset integrity management. Specializing in risk-based inspection (RBI), corrosion management, and fitness-for-purpose assessments for subsea pipelines and offshore structures."
        },
        {
            "company_name": "SINTEF Marine Structures Laboratory",
            "slug": "sintef-marine-structures",
            "url": "https://www.sintef.no",
            "location_slug": "europe",
            "region": "europe",
            "category_slug": "subsea-pipeline-integrity",
            "industry": "oil-gas-renewables",
            "standards": ["API 17J", "API 17B", "ISO 9001"],
            "description": "Focus on testing marine structures, including flexibles, umbilicals, and subsea cables. World-leading laboratory for full-scale fatigue, ultimate strength, and collapse testing."
        },
        {
            "company_name": "IKERLAN",
            "slug": "ikerlan",
            "url": "https://www.ikerlan.es",
            "location_slug": "europe",
            "region": "europe",
            "category_slug": "cybersecurity-testing",
            "industry": "industrial-automation",
            "standards": ["IEC 62443-4-2"],
            "description": "First industrial cybersecurity laboratory in Spain accredited by ENAC to UNE-EN IEC 62443-4-2. Specializing in verification of security requirements for components in industrial automation and control systems (IACS)."
        },
        {
            "company_name": "Fraunhofer SIT",
            "slug": "fraunhofer-sit",
            "url": "https://www.sit.fraunhofer.de",
            "location_slug": "europe",
            "region": "europe",
            "category_slug": "cybersecurity-testing",
            "industry": "iot-embedded",
            "standards": ["IEC 62443"],
            "description": "Cybersecurity assessments for embedded systems and IoT devices. Expertise in hardware-related cryptography, side-channel analysis, and industrial security validation."
        },
        {
            "company_name": "PCA Cyber Security",
            "slug": "pca-cyber-security",
            "url": "https://www.pcacybersecurity.com",
            "location_slug": "global",
            "region": "global",
            "category_slug": "cybersecurity-testing",
            "industry": "automotive-industrial",
            "standards": ["ISO 21434", "IEC 62443"],
            "description": "Comprehensive security assessments and forensic analysis for embedded systems and IoT. Advanced Hardware Laboratory specializes in detecting hardware vulnerabilities before mass production."
        },
        {
            "company_name": "MISTRAS Group",
            "slug": "mistras-group",
            "url": "https://www.mistrasgroup.com",
            "location_slug": "global",
            "region": "global",
            "category_slug": "aerospace-ndt-services",
            "industry": "aerospace-defense",
            "standards": ["AMS 2644", "ASTM E1417", "NAS 410"],
            "description": "Global leader in NDT solutions. Mandated verification for aerospace flight-worthiness using ultrasonic, radiographic, and penetrant testing. NADCAP accredited and FAA certified."
        },
        {
            "company_name": "Applus+ Laboratories (Aerospace)",
            "slug": "applus-laboratories-aerospace",
            "url": "https://www.appluslaboratories.com",
            "location_slug": "europe",
            "region": "europe",
            "category_slug": "aerospace-ndt-services",
            "industry": "aerospace-defense",
            "standards": ["ISO 17025", "NADCAP"],
            "description": "Specialized large-scale structural testing and non-destructive evaluation for advanced aerospace composites. Tier-1 partner for major airframe manufacturers."
        },
        {
            "company_name": "Framatome",
            "slug": "framatome",
            "url": "https://www.framatome.com",
            "location_slug": "europe",
            "region": "europe",
            "category_slug": "nuclear-testing",
            "industry": "nuclear-power",
            "standards": ["ASME NQA-1", "ISO 19443", "RCC-M"],
            "description": "World leader in nuclear energy components. Validation for extreme radiation and thermal environments. Operates specialized radiological testing facilities."
        },
        {
            "company_name": "Kinectrics",
            "slug": "kinectrics",
            "url": "https://www.kinectrics.com",
            "location_slug": "north-america",
            "region": "north-america",
            "category_slug": "nuclear-testing",
            "industry": "nuclear-power",
            "standards": ["CSA N285", "ASME Section III"],
            "description": "Specializing in nuclear life-extension and material degradation testing. Licensed radioactive materials laboratories for commercial grade dedication (CGD)."
        },
        {
            "company_name": "Studsvik",
            "slug": "studsvik",
            "url": "https://www.studsvik.com",
            "location_slug": "europe",
            "region": "europe",
            "category_slug": "nuclear-testing",
            "industry": "nuclear-power",
            "standards": ["ISO 17025", "IAEA Safety Standards"],
            "description": "Advanced fuel and materials testing for nuclear reactors. One of the few commercial entities globally licensed to handle irradiated nuclear fuel for qualification."
        },
        {
            "company_name": "SGS Aerospace",
            "slug": "sgs-aerospace",
            "url": "https://www.sgs.com",
            "location_slug": "global",
            "region": "global",
            "category_slug": "aerospace-ndt-services",
            "industry": "aerospace-defense",
            "standards": ["ISO 17025", "AS9100", "NADCAP"],
            "description": "Localized, trusted verification of aerospace raw materials and forged components. Global footprint for supply chain risk mitigation."
        }
    ]

    for item in listings:
        print(f"🏢 Processing {item['company_name']}...")
        
        # 1. Location
        loc_id = get_id("locations", "slug", item['location_slug'])
        if not loc_id:
            # Fallback to global if not found
            loc_id = get_id("locations", "slug", "global")

        # 2. Category
        primary_cat_id = cat_ids.get(item['category_slug'])
        if not primary_cat_id:
            print(f"  ⚠️ Category {item['category_slug']} not found, skipping...")
            continue

        # 3. Listing
        listing_payload = {
            "business_name": item['company_name'],
            "slug": item['slug'],
            "website": item['url'],
            "description": item['description'],
            "category_id": primary_cat_id,
            "location_id": loc_id,
            "status": "active",
            "verified": True,
            "is_featured": True,
            "plan_type": "premium",
            "billing_tier": "enterprise",
            "region": item['region']
        }
        
        listing_id = create_if_not_exists("listings", "slug", item['slug'], listing_payload)
        if not listing_id:
            continue
        print(f"  ✅ Listing ready: {listing_id}")

        # 4. Standards (Capabilities)
        for std_code in item['standards']:
            std_id = get_id("standards", "code", std_code)
            if not std_id:
                std_id = requests.post(f"{SUPABASE_URL}/rest/v1/standards", headers=headers, json={
                    "code": std_code,
                    "name": std_code,
                    "standard_type": "certification",
                    "is_active": True
                }).json()[0]['id']
                print(f"  ✅ Created Standard: {std_code}")
            
            # Link to listing
            check_cap = requests.get(f"{SUPABASE_URL}/rest/v1/listing_capabilities?listing_id=eq.{listing_id}&standard_id=eq.{std_id}", headers=headers).json()
            if not check_cap:
                requests.post(f"{SUPABASE_URL}/rest/v1/listing_capabilities", headers=headers, json={
                    "listing_id": listing_id,
                    "standard_id": std_id,
                    "verified": True
                })

        # 5. Secondary Category Linking
        # Add NDT as secondary for Aerospace NDT
        if item['category_slug'] == "aerospace-ndt-services":
            ndt_cat_id = get_id("categories", "slug", "ndt-testing-inspection")
            if ndt_cat_id:
                check_link = requests.get(f"{SUPABASE_URL}/rest/v1/listing_categories?listing_id=eq.{listing_id}&category_id=eq.{ndt_cat_id}", headers=headers).json()
                if not check_link:
                    requests.post(f"{SUPABASE_URL}/rest/v1/listing_categories", headers=headers, json={
                        "listing_id": listing_id,
                        "category_id": ndt_cat_id,
                        "is_primary": False
                    })

    print("\n✨ High-yield niche ingestion complete!")

if __name__ == "__main__":
    main()
