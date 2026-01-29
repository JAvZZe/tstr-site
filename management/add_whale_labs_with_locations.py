#!/usr/bin/env python3
"""
Add whale labs with proper location records
"""

import requests
import uuid

SUPABASE_URL = "https://haimjeaetrsaauitrhfy.supabase.co"
SERVICE_ROLE_KEY = "sb_secret_zRN1fTFOYnN7cEbEIfAP7A_YrEKBfI2"

headers = {
    "apikey": SERVICE_ROLE_KEY,
    "Authorization": f"Bearer {SERVICE_ROLE_KEY}",
    "Content-Type": "application/json"
}

def get_or_create_location(name, slug, level, parent_id=None):
    """Get existing location or create new one"""
    # Check if exists
    url = f"{SUPABASE_URL}/rest/v1/locations"
    params = {"select": "id", "slug": f"eq.{slug}"}
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    
    if data and len(data) > 0:
        return data[0]['id']
    
    # Create new location
    location_data = {
        "id": str(uuid.uuid4()),
        "name": name,
        "slug": slug,
        "level": level,
        "parent_id": parent_id
    }
    
    response = requests.post(url, headers=headers, json=location_data)
    if response.status_code in [200, 201]:
        return location_data["id"]
    return None

def get_category_id(slug):
    """Get category ID"""
    url = f"{SUPABASE_URL}/rest/v1/categories"
    params = {"select": "id", "slug": f"eq.{slug}"}
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    return data[0]['id'] if data else None

def get_standards_by_codes(codes):
    """Get standards"""
    url = f"{SUPABASE_URL}/rest/v1/standards"
    codes_list = "','".join(codes)
    params = {"select": "id,code", "code": f"in.({codes_list})"}
    response = requests.get(url, headers=headers, params=params)
    return response.json() if response.status_code == 200 else []

def add_listing(data):
    """Add listing"""
    url = f"{SUPABASE_URL}/rest/v1/listings"
    response = requests.post(url, headers=headers, json=data)
    if response.status_code in [200, 201]:
        return True, data["id"]
    print(f"    Error: {response.text[:200]}")
    return False, None

def add_capability(listing_id, standard_id, specifications):
    """Add capability"""
    url = f"{SUPABASE_URL}/rest/v1/listing_capabilities"
    data = {
        "listing_id": listing_id,
        "standard_id": standard_id,
        "specifications": specifications,
        "verified": False
    }
    response = requests.post(url, headers=headers, json=data)
    return response.status_code in [200, 201]

def main():
    print("🐋 Adding whale labs with proper locations...\n")
    
    cat_id = get_category_id("oil-gas-testing")
    print(f"✅ Category: {cat_id}\n")
    
    # Define labs with location info
    labs = [
        {
            "name": "TÜV SÜD - Hydrogen Testing",
            "country": "Germany",
            "city": "Munich",
            "address": "Westendstraße 199, Munich, Bavaria, Germany",
            "website": "https://www.tuvsud.com/en-us/industries/mobility-and-automotive/automotive-and-oem/alternative-drives/hydrogen",
            "email": "hydrogen@tuvsud.com",
            "description": "Global leader in hydrogen infrastructure testing. Full ISO 19880 series, 1000+ bar pressure, cryogenic LH2, complete embrittlement analysis. Serves major automotive OEMs, energy companies, component manufacturers.",
            "standards": ["ISO 19880-3", "ISO 19880-5", "ISO 11114-4", "SAE J2601", "ISO 14687", "UN ECE R134", "SAE J2579", "ISO 19881"],
            "specs": {
                "max_pressure_bar": 1000,
                "cryogenic_capable": True,
                "temperature_range_c": [-253, 150],
                "test_capabilities": ["valve_testing", "hose_testing", "embrittlement", "permeation", "fire_resistance", "materials_qualification"],
                "facilities": ["blast_bunker", "cryogenic_chamber", "high_pressure_autoclave", "materials_lab"],
                "accreditations": ["ISO 17025", "DAkkS", "UKAS"]
            }
        },
        {
            "name": "Kiwa Technology - H2 Testing",
            "country": "Netherlands",
            "city": "Apeldoorn",
            "address": "Sir William Siemensstraat 2, Apeldoorn, Netherlands",
            "website": "https://www.kiwa.com/en/service/hydrogen-testing/",
            "email": "hydrogen@kiwa.com",
            "description": "European leader in hydrogen appliances and infrastructure. ISO 19880 certification specialist. Primary testing partner for European H2 initiatives. Dual Netherlands/UK facilities.",
            "standards": ["ISO 19880-3", "ISO 19880-5", "ISO 11114-4", "ISO 14687", "SAE J2601"],
            "specs": {
                "max_pressure_bar": 700,
                "temperature_range_c": [-40, 85],
                "test_capabilities": ["valve_testing", "hose_testing", "appliance_testing", "materials_compatibility", "station_validation"],
                "accreditations": ["ISO 17025", "RvA"]
            }
        },
        {
            "name": "NPL - National Physical Laboratory",
            "country": "United Kingdom",
            "city": "London",
            "address": "Hampton Road, Teddington, Middlesex, UK",
            "website": "https://www.npl.co.uk/hydrogen",
            "email": "hydrogen@npl.co.uk",
            "description": "UK national metrology institute. Gold standard for hydrogen purity (ISO 14687). Primary reference standards for H2 measurement. World-leading trace contaminant analysis (ppb detection).",
            "standards": ["ISO 14687", "ISO 19880-3", "ISO 17025"],
            "specs": {
                "purity_testing": True,
                "detection_limit_ppb": 0.001,
                "test_capabilities": ["purity_analysis", "trace_contaminants", "metrology", "calibration_standards"],
                "primary_standards": True,
                "accreditations": ["ISO 17025", "UKAS"]
            }
        },
        {
            "name": "Powertech Labs - H2 Tank Testing",
            "country": "Canada",
            "city": "Surrey",
            "address": "12388 88 Avenue, Surrey, BC, Canada",
            "website": "https://www.powertechlabs.com/hydrogen-testing/",
            "email": "hydrogen@powertechlabs.com",
            "description": "World leader in high-pressure H2 tank testing (Type IV). UN ECE R134 specialist. 1000+ bar capability. Critical for automotive OEM certification (Toyota, Hyundai, BMW partnerships).",
            "standards": ["UN ECE R134", "SAE J2579", "ISO 19881", "SAE J2601", "ISO 11114-4"],
            "specs": {
                "max_pressure_bar": 1000,
                "tank_testing": True,
                "type_iv_specialist": True,
                "test_capabilities": ["tank_cycling", "burst_testing", "permeation", "drop_testing", "gun_fire", "bonfire"],
                "accreditations": ["ISO 17025", "SCC"]
            }
        },
        {
            "name": "WHA International - H2 Safety Lab",
            "country": "United States",
            "city": "Bartlesville",
            "address": "3103 SE 29th Street, Bartlesville, OK, USA",
            "website": "https://www.wha-international.com/hydrogen-safety",
            "email": "info@wha-international.com",
            "description": "Niche specialists in H2 fire safety and forensics. Unique rapid decompression and ignition testing. Expert witness for H2 incidents. Catastrophic failure analysis.",
            "standards": ["ISO 19880-3", "SAE J2579", "ISO 11114-4"],
            "specs": {
                "max_pressure_bar": 700,
                "fire_safety_specialist": True,
                "forensics": True,
                "test_capabilities": ["ignition_testing", "fire_resistance", "failure_analysis", "rapid_decompression", "expert_witness"],
                "accreditations": ["ISO 17025"]
            }
        },
        {
            "name": "Element Materials - Embrittlement Lab",
            "country": "United States",
            "city": "Global",
            "address": "Global Network - USA, UK, Germany, Singapore",
            "website": "https://www.element.com/industries/oil-and-gas/hydrogen-energy",
            "email": "hydrogen@element.com",
            "description": "Global leader in materials science and H2 embrittlement (ISO 11114-4). Extensive metallurgical labs with SEM, XRD. Specializes in materials qualification, fracture mechanics, SSRT.",
            "standards": ["ISO 11114-4", "ISO 19880-3", "NACE MR0175"],
            "specs": {
                "materials_science_leader": True,
                "embrittlement_specialist": True,
                "test_capabilities": ["embrittlement", "metallography", "fracture_mechanics", "materials_qualification", "SSRT", "SEM", "XRD"],
                "accreditations": ["ISO 17025", "Nadcap", "UKAS", "A2LA"]
            }
        }
    ]
    
    # Get all standards
    all_codes = list(set([s for lab in labs for s in lab['standards']]))
    standards_list = get_standards_by_codes(all_codes)
    standards_map = {s['code']: s['id'] for s in standards_list}
    print(f"📊 Found {len(standards_map)} standards\n")
    
    added_labs = 0
    added_caps = 0
    
    for lab in labs:
        print(f"🏢 {lab['name']}...")
        
        # Create or get country location
        country_slug = lab['country'].lower().replace(' ', '-')
        country_id = get_or_create_location(lab['country'], country_slug, 'country')
        
        # Create or get city location
        city_slug = f"{lab['city'].lower().replace(' ', '-')}-{country_slug}"
        city_id = get_or_create_location(lab['city'], city_slug, 'city', country_id)
        
        print(f"  📍 Location: {lab['city']}, {lab['country']}")
        
        # Create listing
        slug = lab["name"].lower().replace(' ', '-').replace('ü', 'u').replace('ö', 'o')
        slug = ''.join(c for c in slug if c.isalnum() or c == '-')
        
        listing_data = {
            "id": str(uuid.uuid4()),
            "business_name": lab["name"],
            "slug": slug,
            "website": lab["website"],
            "address": lab["address"],
            "email": lab.get("email", ""),
            "phone": "",
            "description": lab["description"],
            "category_id": cat_id,
            "location_id": city_id,
            "status": "active",
            "verified": False,
            "claimed": False,
            "featured": False,
            "is_featured": False,
            "views": 0,
            "priority_rank": 0
        }
        
        success, listing_id = add_listing(listing_data)
        if not success:
            continue
        
        print("  ✅ Listing added")
        added_labs += 1
        
        # Add capabilities
        for std_code in lab['standards']:
            if std_code in standards_map:
                if add_capability(listing_id, standards_map[std_code], lab['specs']):
                    print(f"    ✅ {std_code}")
                    added_caps += 1
        
        print()
    
    print("\n📊 Summary:")
    print(f"  • Labs added: {added_labs}/6")
    print(f"  • Capabilities: {added_caps}")
    print("\n🎯 Whale labs deployed!\n")

if __name__ == "__main__":
    main()
