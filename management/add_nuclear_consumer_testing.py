#!/usr/bin/env python3
"""
Add Nuclear Energy and Consumer Goods/Textile specialized listings and standards.
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
    print("🚀 Adding Nuclear & Consumer Goods Testing Specializations...\n")

    # 1. Create Categories
    print("📁 Syncing Specialized categories...")
    # Nuclear
    nuclear_id = get_id("categories", "slug", "nuclear-testing")
    if not nuclear_id:
        resp = requests.post(f"{SUPABASE_URL}/rest/v1/categories", headers=headers, json={
            "name": "Nuclear Energy Testing & Inspection",
            "slug": "nuclear-testing",
            "description": "Specialized labs for nuclear fuel validation, component qualification, and inservice inspection (ISI) for power plants."
        })
        nuclear_id = resp.json()[0]['id']
        print(f"  ✅ Created Nuclear category: {nuclear_id}")

    # Consumer Goods
    consumer_id = get_id("categories", "slug", "consumer-goods-testing")
    if not consumer_id:
        resp = requests.post(f"{SUPABASE_URL}/rest/v1/categories", headers=headers, json={
            "name": "Consumer Goods & Textile Testing",
            "slug": "consumer-goods-testing",
            "description": "Global quality assurance for apparel, footwear, hardlines, and electronics including chemical and physical safety testing."
        })
        consumer_id = resp.json()[0]['id']
        print(f"  ✅ Created Consumer category: {consumer_id}")

    # 2. Add Standards
    print("\n📜 Adding Specialized Standards...")
    new_standards = [
        {"code": "ASME Section III", "name": "Rules for Construction of Nuclear Facility Components", "standard_type": "compliance", "category_id": nuclear_id},
        {"code": "RSE-M", "name": "In-service Inspection Rules for Mechanical Components of PWR Nuclear Islands", "standard_type": "compliance", "category_id": nuclear_id},
        {"code": "10 CFR Part 50", "name": "Domestic Licensing of Production and Utilization Facilities (Appendix B QA)", "standard_type": "compliance", "category_id": nuclear_id},
        {"code": "AATCC TM61", "name": "Colorfastness to Laundering: Accelerated", "standard_type": "test_method", "category_id": consumer_id},
        {"code": "ISO 14184", "name": "Textiles — Determination of formaldehyde", "standard_type": "test_method", "category_id": consumer_id},
        {"code": "ASTM F963", "name": "Standard Consumer Safety Specification for Toy Safety", "standard_type": "compliance", "category_id": consumer_id},
        {"code": "OEKO-TEX Standard 100", "name": "Testing for harmful substances in textiles", "standard_type": "certification", "category_id": consumer_id}
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
        {"code": "NUCLEAR-ISI", "name": "In-Service Inspection (ISI)", "standard_type": "certification"},
        {"code": "FUEL-VALIDATION", "name": "Nuclear Fuel Validation", "standard_type": "certification"},
        {"code": "ETHICAL-AUDIT", "name": "Social & Ethical Audits", "standard_type": "certification"},
        {"code": "SOFTLINES-TESTING", "name": "Textile & Apparel Testing", "standard_type": "certification"},
        {"code": "HARDLINES-TESTING", "name": "Hardlines & Toy Safety", "standard_type": "certification"}
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
            "business_name": "Westinghouse Electric Company",
            "slug": "westinghouse-nuclear",
            "website": "https://www.westinghousenuclear.com/",
            "description": "Westinghouse is a global leader in nuclear energy technology and testing. They provide comprehensive fuel data management (TracWorks®), core monitoring (BEACON™), and safety-related component qualification. Their specialized labs perform mechanical, materials, and non-destructive examination (NDE) to ensure the integrity of PWR and BWR units worldwide.",
            "category_id": nuclear_id,
            "caps": ["ASME Section III", "10 CFR Part 50", "NUCLEAR-ISI", "FUEL-VALIDATION"]
        },
        {
            "business_name": "Framatome",
            "slug": "framatome",
            "website": "https://www.framatome.com/",
            "description": "Framatome is an international leader in nuclear energy, specializing in the design, maintenance, and testing of nuclear steam supply systems. Their Technical Centers perform over 2,800 qualification tests annually, including thermal-hydraulic and environmental validation. Framatome provides advanced ISI services using breakthrough ultrasonic technologies for core barrel welds and RPV inspections.",
            "category_id": nuclear_id,
            "caps": ["RSE-M", "ASME Section III", "NUCLEAR-ISI"]
        },
        {
            "business_name": "Orano",
            "slug": "orano-group",
            "website": "https://www.orano.group/",
            "description": "Orano provides specialized nuclear testing and materials characterization across the entire fuel cycle. Their CIME facility specializes in hydrometallurgy and environmental monitoring, while Orano NPS validates nuclear packaging and transport casks through rigorous mechanical and thermal testing. Orano Med extracts high-purity radioisotopes for medical applications, supported by advanced radiochemical analysis.",
            "category_id": nuclear_id,
            "caps": ["ISO 17025", "NUCLEAR-ISI"]
        },
        {
            "business_name": "QIMA",
            "slug": "qima",
            "website": "https://www.qima.com/",
            "description": "QIMA is a leading global quality control and compliance service provider. Their digital platforms, myQIMA and QIMAone, enable brands to manage product inspections, supplier audits, and lab testing in real-time. QIMA specializes in consumer goods safety (REACH, CPSIA) and ethical audits, providing high-visibility supply chain mapping and AI-powered quality risk management.",
            "category_id": consumer_id,
            "caps": ["AATCC TM61", "OEKO-TEX Standard 100", "ETHICAL-AUDIT", "SOFTLINES-TESTING"]
        }
    ]

    # Get existing ISO 17025 for linking
    iso_17025_id = get_id("standards", "code", "ISO/IEC 17025")
    if not iso_17025_id:
        resp = requests.post(f"{SUPABASE_URL}/rest/v1/standards", headers=headers, json={
            "code": "ISO/IEC 17025",
            "name": "General requirements for the competence of testing and calibration laboratories",
            "standard_type": "certification"
        })
        iso_17025_id = resp.json()[0]['id']
    
    standards_map["ISO 17025"] = iso_17025_id

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
        target_cats = ["ndt-testing-inspection", "engineering-services"]
        if ld['category_id'] == nuclear_id:
            target_cats.append("power-generation-testing") # Fallback or add
        
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

    # Update existing Bureau Veritas and Intertek with Consumer context
    print("\n🔄 Updating existing BV and Intertek with Consumer Goods context...")
    for s in ["bureau-veritas", "intertek"]:
        lid = get_id("listings", "slug", s)
        if lid:
            # Add consumer tags
            for tag_code in ["SOFTLINES-TESTING", "HARDLINES-TESTING", "ETHICAL-AUDIT"]:
                sid = standards_map[tag_code]
                requests.post(f"{SUPABASE_URL}/rest/v1/listing_capabilities", headers=headers, json={
                    "listing_id": lid,
                    "standard_id": sid,
                    "verified": True
                })
            requests.post(f"{SUPABASE_URL}/rest/v1/listing_categories", headers=headers, json={
                "listing_id": lid,
                "category_id": consumer_id,
                "is_primary": False
            })
            print(f"  ✅ Updated {s} with Consumer Goods context")

    print("\n✨ Nuclear & Consumer expansion complete!")

if __name__ == "__main__":
    main()
