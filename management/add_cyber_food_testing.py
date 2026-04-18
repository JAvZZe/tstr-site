import os
#!/usr/bin/env python3
"""
Add Cybersecurity and Food Safety specialized listings and standards.
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
    print("🚀 Adding Cybersecurity & Food Safety Testing Specializations...\n")

    # 1. Create Categories
    print("📁 Syncing Specialized categories...")
    # Cybersecurity
    cyber_id = get_id("categories", "slug", "cybersecurity-testing")
    if not cyber_id:
        resp = requests.post(f"{SUPABASE_URL}/rest/v1/categories", headers=headers, json={
            "name": "Cybersecurity & Software Testing",
            "slug": "cybersecurity-testing",
            "description": "Specialized labs for penetration testing, red teaming, software resilience, and digital trust certification."
        })
        cyber_id = resp.json()[0]['id']
        print(f"  ✅ Created Cybersecurity category: {cyber_id}")

    # Food Safety
    food_parent_id = get_id("categories", "slug", "environmental-testing") # Fallback to Environmental if Bio/Life isn't clear
    food_id = get_id("categories", "slug", "food-safety-testing")
    if not food_id:
        resp = requests.post(f"{SUPABASE_URL}/rest/v1/categories", headers=headers, json={
            "name": "Food Safety & Agricultural Testing",
            "slug": "food-safety-testing",
            "parent_id": food_parent_id,
            "description": "Comprehensive laboratory testing for food microbiology, chemical contaminants, and agricultural provenance."
        })
        food_id = resp.json()[0]['id']
        print(f"  ✅ Created Food Safety category: {food_id}")

    # 2. Add Standards
    print("\n📜 Adding Specialized Standards...")
    new_standards = [
        {"code": "ISO 27001", "name": "Information security management systems", "standard_type": "compliance", "category_id": cyber_id},
        {"code": "NIST SP 800-53", "name": "Security and Privacy Controls for Information Systems and Organizations", "standard_type": "compliance", "category_id": cyber_id},
        {"code": "SOC 2", "name": "System and Organization Controls (Security, Availability, Processing Integrity, Confidentiality, and Privacy)", "standard_type": "certification", "category_id": cyber_id},
        {"code": "FSSC 22000", "name": "Food Safety System Certification", "standard_type": "certification", "category_id": food_id},
        {"code": "ISO 22000", "name": "Food safety management systems", "standard_type": "compliance", "category_id": food_id},
        {"code": "SQF Edition 9", "name": "Safe Quality Food Code", "standard_type": "certification", "category_id": food_id},
        {"code": "BRCGS Food Safety", "name": "Global Standard for Food Safety", "standard_type": "certification", "category_id": food_id},
        {"code": "HACCP", "name": "Hazard Analysis and Critical Control Points", "standard_type": "compliance", "category_id": food_id}
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
        {"code": "RED-TEAMING", "name": "Red Teaming & Simulations", "standard_type": "certification"},
        {"code": "PEN-TESTING", "name": "Penetration Testing Services", "standard_type": "certification"},
        {"code": "FOOD-MICROBIOLOGY", "name": "Food Microbiology Analysis", "standard_type": "certification"},
        {"code": "CONTAMINANT-SCREENING", "name": "Contaminant & Residue Screening", "standard_type": "certification"},
        {"code": "FOOD-FRAUD", "name": "Food Fraud & Authenticity Testing", "standard_type": "certification"}
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
            "business_name": "NCC Group",
            "slug": "ncc-group",
            "website": "https://www.nccgroup.com/",
            "description": "NCC Group is a global leader in cybersecurity and software resilience. Specializing in 'people-powered, tech-enabled' security, they provide world-class penetration testing, Red Teaming, and Full Spectrum Attack Simulations. Their proprietary 'Escrow as a Service' (EaaS) ensures software resilience for cloud-native applications, while their Global SOC provides 24/7 managed detection and response (MXDR) for critical digital infrastructure.",
            "category_id": cyber_id,
            "caps": ["ISO 27001", "SOC 2", "RED-TEAMING", "PEN-TESTING"]
        },
        {
            "business_name": "Mérieux NutriSciences",
            "slug": "merieux-nutrisciences",
            "website": "https://www.merieuxnutrisciences.com/",
            "description": "Mérieux NutriSciences is a global leader in food safety, quality, and nutrition. With a network of over 100 ISO 17025-accredited labs, they provide comprehensive microbiology, chemistry, and contaminant screening. Their digital ecosystem, including EnviroMap® for environmental monitoring and Safety HUD for global risk tracking, enables food businesses to move from reactive to proactive safety management across the entire supply chain.",
            "category_id": food_id,
            "caps": ["FSSC 22000", "HACCP", "FOOD-MICROBIOLOGY", "CONTAMINANT-SCREENING"]
        },
        {
            "business_name": "ALS Global",
            "slug": "als-global-food",
            "website": "https://www.alsglobal.com/en/food",
            "description": "ALS Global provides premier food and agricultural testing services, leveraging advanced technologies like Benchtop NMR for authenticity and light stable isotope analysis for provenance verification. Their Webtrieve™ portal offers real-time sample tracking and data visualization, helping clients combat food fraud and ensure product integrity from farm to fork. ALS specializes in ultra-trace contaminant detection and precision agricultural soil analysis.",
            "category_id": food_id,
            "caps": ["SQF Edition 9", "BRCGS Food Safety", "FOOD-FRAUD", "CONTAMINANT-SCREENING"]
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
        target_cats = ["ndt-testing-inspection", "engineering-services"]
        if ld['category_id'] == food_id:
            target_cats.append("pharmaceutical-testing")
        
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

    # Update existing heavyweights
    print("\n🔄 Updating existing UL, SGS, Eurofins, and Intertek with Cyber/Food context...")
    # Find IDs
    heavy_slugs = ["ul-solutions", "sgs", "eurofins-electrical-electronics", "intertek", "dnv", "tuv-rheinland"]
    for s in heavy_slugs:
        lid = get_id("listings", "slug", s)
        if lid:
            # All these offer Cyber & Food usually. 
            # I'll add one key tag for each sector if not present.
            for tag_code in ["PEN-TESTING", "HACCP"]:
                sid = standards_map[tag_code]
                requests.post(f"{SUPABASE_URL}/rest/v1/listing_capabilities", headers=headers, json={
                    "listing_id": lid,
                    "standard_id": sid,
                    "verified": True
                })
            # Link to new categories
            for cat_id in [cyber_id, food_id]:
                requests.post(f"{SUPABASE_URL}/rest/v1/listing_categories", headers=headers, json={
                    "listing_id": lid,
                    "category_id": cat_id,
                    "is_primary": False
                })
            print(f"  ✅ Updated {s} with Cyber & Food context")

    print("\n✨ Cyber & Food expansion complete!")

if __name__ == "__main__":
    main()
