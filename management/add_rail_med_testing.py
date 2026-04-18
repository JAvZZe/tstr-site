import os
#!/usr/bin/env python3
"""
Add Railway and Medical Device specialized listings and standards.
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
    print("🚀 Adding Railway & Medical Device Testing Specializations...\n")

    # 1. Create Categories
    print("📁 Syncing Specialized categories...")
    # Railway
    rail_id = get_id("categories", "slug", "railway-testing")
    if not rail_id:
        resp = requests.post(f"{SUPABASE_URL}/rest/v1/categories", headers=headers, json={
            "name": "Railway & Rolling Stock Testing",
            "slug": "railway-testing",
            "description": "Comprehensive testing and certification for rolling stock, signaling systems, and railway infrastructure."
        })
        rail_id = resp.json()[0]['id']
        print(f"  ✅ Created Railway category: {rail_id}")

    # Medical
    med_parent_id = get_id("categories", "slug", "pharmaceutical-testing")
    med_id = get_id("categories", "slug", "medical-device-testing")
    if not med_id:
        resp = requests.post(f"{SUPABASE_URL}/rest/v1/categories", headers=headers, json={
            "name": "Medical Device & Healthcare Testing",
            "slug": "medical-device-testing",
            "parent_id": med_parent_id,
            "description": "Specialized laboratory testing for medical devices, including biocompatibility, sterilization, and chemical characterization."
        })
        med_id = resp.json()[0]['id']
        print(f"  ✅ Created Medical category: {med_id}")

    # 2. Add Standards
    print("\n📜 Adding Specialized Standards...")
    new_standards = [
        {"code": "EN 50126", "name": "Railway applications - RAMS (Reliability, Availability, Maintainability and Safety)", "standard_type": "compliance", "category_id": rail_id},
        {"code": "EN 45545", "name": "Railway applications - Fire protection on railway vehicles", "standard_type": "compliance", "category_id": rail_id},
        {"code": "ISO 22163", "name": "Railway applications - Quality management system (IRIS)", "standard_type": "compliance", "category_id": rail_id},
        {"code": "ISO 13485", "name": "Medical devices — Quality management systems", "standard_type": "compliance", "category_id": med_id},
        {"code": "ISO 10993", "name": "Biological evaluation of medical devices (Biocompatibility)", "standard_type": "test_method", "category_id": med_id},
        {"code": "IEC 60601", "name": "Medical electrical equipment - General requirements for basic safety and essential performance", "standard_type": "compliance", "category_id": med_id},
        {"code": "ISO 11135", "name": "Sterilization of health-care products — Ethylene oxide", "standard_type": "test_method", "category_id": med_id},
        {"code": "ISO 11137", "name": "Sterilization of health-care products — Radiation", "standard_type": "test_method", "category_id": med_id}
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
        {"code": "ROLLING-STOCK-CERT", "name": "Rolling Stock Certification", "standard_type": "certification"},
        {"code": "SIGNALING-TESTING", "name": "Signaling & Telecoms Validation", "standard_type": "certification"},
        {"code": "BIOCOMPATIBILITY", "name": "Biocompatibility Testing", "standard_type": "certification"},
        {"code": "STERILIZATION-VAL", "name": "Sterilization Validation", "standard_type": "certification"}
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
            "business_name": "TÜV SÜD Rail",
            "slug": "tuv-sud-rail",
            "website": "https://www.tuvsud.com/rail",
            "description": "TÜV SÜD Rail is a global leader in railway testing, inspection, and certification. They provide comprehensive technical assurance for rolling stock, signaling systems (ERTMS/ETCS), and infrastructure. Their specialized labs handle dynamic behavior, braking systems, and fire safety (EN 45545) validation, ensuring the highest RAMS standards for modern rail networks.",
            "category_id": rail_id,
            "caps": ["EN 50126", "EN 45545", "ISO 22163", "ROLLING-STOCK-CERT", "SIGNALING-TESTING"]
        },
        {
            "business_name": "Ricardo Rail",
            "slug": "ricardo-rail",
            "website": "https://rail.ricardo.com/",
            "description": "Ricardo Rail provides expert consultancy and technical assurance services for the global rail industry. Specializing in rolling stock engineering, independent assurance (AsBO/NoBo/DeBo), and operational NDT, Ricardo ensures the safety and performance of complex rail systems. Their expertise includes electrification, propulsion, and structural integrity monitoring for high-speed and freight networks.",
            "category_id": rail_id,
            "caps": ["EN 50126", "ISO 22163", "ROLLING-STOCK-CERT", "SIGNALING-TESTING"]
        },
        {
            "business_name": "Nelson Labs",
            "slug": "nelson-labs",
            "website": "https://www.nelsonlabs.com/",
            "description": "Nelson Labs (a Sotera Health company) is a global leader in medical device testing. They specialize in biocompatibility (ISO 10993) and sterilization validation (EO, Radiation, VHP) to ensure regulatory compliance for global markets. Their services include extractables/leachables studies, chemical characterization, and microbiological analysis for surgical and implantable devices.",
            "category_id": med_id,
            "caps": ["ISO 10993", "ISO 11135", "ISO 11137", "BIOCOMPATIBILITY", "STERILIZATION-VAL"]
        },
        {
            "business_name": "Charles River Laboratories",
            "slug": "charles-river-labs",
            "website": "https://www.criver.com/",
            "description": "Charles River provides essential products and services to help pharmaceutical and biotechnology companies, government agencies, and leading academic institutions accelerate their research and drug development efforts. Their specialized medical device division offers comprehensive biological safety testing, toxicology, and sterilization validation according to GLP and ISO standards.",
            "category_id": med_id,
            "caps": ["ISO 10993", "BIOCOMPATIBILITY", "STERILIZATION-VAL"]
        },
        {
            "business_name": "NAMSA",
            "slug": "namsa-medical",
            "website": "https://namsa.com/",
            "description": "NAMSA is the world's only Medical Research Organization (MRO) that speeds product development through integrated laboratory, clinical, and regulatory services. Driven by global regulatory expertise and therapeutic depth, NAMSA provides comprehensive biocompatibility testing, chemical characterization, and clinical trial support for high-risk medical devices.",
            "category_id": med_id,
            "caps": ["ISO 10993", "ISO 13485", "BIOCOMPATIBILITY", "STERILIZATION-VAL"]
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
            # Check if exists
            check = requests.get(f"{SUPABASE_URL}/rest/v1/listing_capabilities?listing_id=eq.{lid}&standard_id=eq.{sid}", headers=headers).json()
            if not check:
                requests.post(f"{SUPABASE_URL}/rest/v1/listing_capabilities", headers=headers, json={
                    "listing_id": lid,
                    "standard_id": sid,
                    "verified": True
                })
        
        # Multi-category
        target_cats = ["ndt-testing-inspection", "engineering-services", "materials-testing"]
        if ld['category_id'] == med_id:
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

    # Update existing Eurofins
    print("\n🔄 Updating existing Eurofins profiles...")
    # Find all eurofins
    resp = requests.get(f"{SUPABASE_URL}/rest/v1/listings?business_name=ilike.*Eurofins*", headers=headers).json()
    for e in resp:
        requests.post(f"{SUPABASE_URL}/rest/v1/listing_capabilities", headers=headers, json={
            "listing_id": e['id'],
            "standard_id": standards_map["BIOCOMPATIBILITY"],
            "verified": True
        })
        requests.post(f"{SUPABASE_URL}/rest/v1/listing_categories", headers=headers, json={
            "listing_id": e['id'],
            "category_id": med_id,
            "is_primary": False
        })
    print(f"  ✅ Updated {len(resp)} Eurofins entries with Medical Device context")

    print("\n✨ Rail & Medical expansion complete!")

if __name__ == "__main__":
    main()
