#!/usr/bin/env python3
"""
Add target "whale" hydrogen testing laboratories
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

def get_category_id(slug):
    """Get category ID by slug"""
    url = f"{SUPABASE_URL}/rest/v1/categories"
    params = {"select": "id", "slug": f"eq.{slug}"}
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    return data[0]['id'] if data else None

def get_standards_by_codes(codes):
    """Get standards by their codes"""
    url = f"{SUPABASE_URL}/rest/v1/standards"
    params = {"select": "id,code", "code": f"in.({','.join(codes)})"}
    response = requests.get(url, headers=headers, params=params)
    return response.json() if response.status_code == 200 else []

def add_listing(business_name, website, address, category_id, description):
    """Add a new listing"""
    url = f"{SUPABASE_URL}/rest/v1/listings"
    listing_id = str(uuid.uuid4())
    data = {
        "id": listing_id,
        "business_name": business_name,
        "website": website,
        "address": address,
        "category_id": category_id,
        "description": description,
        "status": "active",
        "verified": False
    }
    
    response = requests.post(url, headers=headers, json=data)
    return response.status_code in [200, 201], listing_id

def add_capability(listing_id, standard_id, specifications):
    """Add a capability"""
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
    print("🐋 Adding target hydrogen 'whale' laboratories...\n")
    
    cat_id = get_category_id("oil-gas-testing")
    if not cat_id:
        print("❌ Category not found")
        return
    
    # Target labs
    labs = [
        {
            "name": "TÜV SÜD",
            "website": "https://www.tuvsud.com/en-us/industries/mobility-and-automotive/automotive-and-oem/alternative-drives/hydrogen",
            "address": "Munich, Germany (Global Operations)",
            "description": "Leading global testing and certification body for hydrogen infrastructure. Full range of H2 testing from 350-1000+ bar, cryogenic LH2, and comprehensive embrittlement testing. ISO 19880 family expert.",
            "standards": ["ISO 19880-3", "ISO 19880-5", "ISO 11114-4", "SAE J2601", "ISO 14687", "UN ECE R134"],
            "specs": {
                "max_pressure_bar": 1000,
                "cryogenic_capable": True,
                "temperature_range_c": [-253, 100],
                "test_capabilities": ["valve_testing", "hose_testing", "embrittlement", "permeation", "leak_testing"],
                "facilities": ["blast_bunker", "cryogenic_chamber", "high_pressure_autoclave"],
                "accreditations": ["ISO 17025", "DAkkS", "UKAS"]
            }
        },
        {
            "name": "Kiwa Technology",
            "website": "https://www.kiwa.com/en/service/hydrogen-testing/",
            "address": "Apeldoorn, Netherlands / Cheltenham, UK",
            "description": "European leader in hydrogen appliances and mid-pressure testing. Strong in ISO 19880 series and materials compatibility. Extensive experience with European hydrogen standards.",
            "standards": ["ISO 19880-3", "ISO 19880-5", "ISO 11114-4", "ISO 14687"],
            "specs": {
                "max_pressure_bar": 700,
                "cryogenic_capable": False,
                "temperature_range_c": [-40, 85],
                "test_capabilities": ["valve_testing", "appliance_testing", "materials_compatibility"],
                "facilities": ["pressure_test_rigs", "materials_lab"],
                "accreditations": ["ISO 17025", "RvA"]
            }
        },
        {
            "name": "NPL - National Physical Laboratory",
            "website": "https://www.npl.co.uk/hydrogen",
            "address": "Teddington, United Kingdom",
            "description": "Gold standard for hydrogen purity testing (ISO 14687). UK's national metrology institute with primary standards for hydrogen measurement. Reference laboratory for trace contaminant analysis.",
            "standards": ["ISO 14687", "ISO 19880-3"],
            "specs": {
                "max_pressure_bar": 700,
                "purity_testing": True,
                "detection_limit_ppb": 0.001,
                "test_capabilities": ["purity_analysis", "trace_contaminants", "metrology"],
                "primary_standards": True,
                "accreditations": ["ISO 17025", "UKAS"]
            }
        },
        {
            "name": "Powertech Labs",
            "website": "https://www.powertechlabs.com/hydrogen-testing/",
            "address": "Surrey, British Columbia, Canada",
            "description": "World leader in high-pressure tank testing (Type IV). Specialists in UN ECE R134 compliance and 700+ bar testing. Extensive automotive OEM client base.",
            "standards": ["UN ECE R134", "SAE J2579", "ISO 19881", "SAE J2601"],
            "specs": {
                "max_pressure_bar": 1000,
                "tank_testing": True,
                "type_iv_specialist": True,
                "test_capabilities": ["tank_cycling", "burst_testing", "permeation", "drop_testing"],
                "facilities": ["high_pressure_autoclave", "drop_tower", "environmental_chamber"],
                "accreditations": ["ISO 17025", "SCC"]
            }
        },
        {
            "name": "WHA International",
            "website": "https://www.wha-international.com/hydrogen-safety",
            "address": "Bartlesville, Oklahoma, USA",
            "description": "Niche specialists in hydrogen fire safety and forensics. Experts in oxygen/hydrogen combustion testing and failure analysis. Unique capabilities in rapid decompression and ignition testing.",
            "standards": ["ISO 19880-3", "SAE J2579"],
            "specs": {
                "max_pressure_bar": 700,
                "fire_safety_specialist": True,
                "forensics": True,
                "test_capabilities": ["ignition_testing", "fire_resistance", "failure_analysis", "rapid_decompression"],
                "facilities": ["blast_bunker", "fire_test_chamber"],
                "accreditations": ["ISO 17025"]
            }
        },
        {
            "name": "Element Materials Technology",
            "website": "https://www.element.com/industries/oil-and-gas/hydrogen-energy",
            "address": "Global Network (USA, UK, Germany, Singapore)",
            "description": "Global leader in materials science and hydrogen embrittlement testing (ISO 11114-4). Extensive metallurgical lab network. Strong in failure analysis and materials qualification.",
            "standards": ["ISO 11114-4", "ISO 19880-3", "NACE MR0175"],
            "specs": {
                "max_pressure_bar": 700,
                "materials_science_leader": True,
                "embrittlement_specialist": True,
                "test_capabilities": ["embrittlement", "metallography", "fracture_mechanics", "materials_qualification"],
                "facilities": ["materials_lab", "SEM", "XRD", "tensile_rigs"],
                "accreditations": ["ISO 17025", "Nadcap", "UKAS", "A2LA"]
            }
        }
    ]
    
    # Get all hydrogen standards
    std_codes = list(set([std for lab in labs for std in lab['standards']]))
    standards_map = {s['code']: s['id'] for s in get_standards_by_codes(std_codes)}
    
    print(f"📊 Found {len(standards_map)} standards\n")
    
    added_labs = 0
    added_caps = 0
    
    for lab in labs:
        print(f"🏢 Adding {lab['name']}...")
        
        success, listing_id = add_listing(
            lab['name'],
            lab['website'],
            lab['address'],
            cat_id,
            lab['description']
        )
        
        if not success:
            print(f"  ❌ Failed to add listing")
            continue
        
        print(f"  ✅ Listing added")
        added_labs += 1
        
        # Add capabilities for each standard
        for std_code in lab['standards']:
            if std_code not in standards_map:
                print(f"  ⚠️  Standard {std_code} not found")
                continue
            
            std_id = standards_map[std_code]
            if add_capability(listing_id, std_id, lab['specs']):
                print(f"    ✅ {std_code}")
                added_caps += 1
            else:
                print(f"    ❌ {std_code} (failed)")
        
        print()
    
    print(f"\n📊 Summary:")
    print(f"  • Labs added: {added_labs}/{len(labs)}")
    print(f"  • Capabilities added: {added_caps}")
    print(f"  • Average capabilities per lab: {added_caps/added_labs if added_labs > 0 else 0:.1f}")
    print("\n🎯 Whale labs added successfully!\n")

if __name__ == "__main__":
    main()
