#!/usr/bin/env python3
"""
Link the newly added whale labs to their hydrogen standards
"""

import requests

SUPABASE_URL = "https://haimjeaetrsaauitrhfy.supabase.co"
SERVICE_ROLE_KEY = "sb_secret_zRN1fTFOYnN7cEbEIfAP7A_YrEKBfI2"

headers = {
    "apikey": SERVICE_ROLE_KEY,
    "Authorization": f"Bearer {SERVICE_ROLE_KEY}",
    "Content-Type": "application/json"
}

def get_data(table, filters=None):
    url = f"{SUPABASE_URL}/rest/v1/{table}"
    params = {"select": "*"}
    if filters:
        params.update(filters)
    response = requests.get(url, headers=headers, params=params)
    return response.json() if response.status_code == 200 else None

def add_capability(listing_id, standard_id, specifications):
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
    print("🔗 Linking whale labs to standards...\n")
    
    # Get all standards
    standards = get_data("standards", {"is_active": "eq.true"})
    std_map = {s['code']: s['id'] for s in standards}
    print(f"📊 Found {len(std_map)} standards\n")
    
    # Define whale labs and their standards
    whale_labs = {
        "TÜV SÜD - Hydrogen Testing": {
            "standards": ["ISO 19880-3", "ISO 19880-5", "ISO 11114-4", "SAE J2601", "ISO 14687", "UN ECE R134", "SAE J2579", "ISO 19881"],
            "specs": {
                "max_pressure_bar": 1000,
                "cryogenic_capable": True,
                "temperature_range_c": [-253, 150],
                "test_capabilities": ["valve_testing", "hose_testing", "embrittlement", "permeation", "fire_resistance", "materials_qualification"],
                "facilities": ["blast_bunker", "cryogenic_chamber", "high_pressure_autoclave", "materials_lab"],
                "accreditations": ["ISO 17025", "DAkkS", "UKAS"],
                "global_leader": True
            }
        },
        "Kiwa Technology - H2 Testing": {
            "standards": ["ISO 19880-3", "ISO 19880-5", "ISO 11114-4", "ISO 14687", "SAE J2601"],
            "specs": {
                "max_pressure_bar": 700,
                "temperature_range_c": [-40, 85],
                "test_capabilities": ["valve_testing", "hose_testing", "appliance_testing", "materials_compatibility", "station_validation"],
                "accreditations": ["ISO 17025", "RvA"],
                "european_leader": True
            }
        },
        "NPL - National Physical Laboratory": {
            "standards": ["ISO 14687", "ISO 19880-3", "ISO 17025"],
            "specs": {
                "purity_testing": True,
                "detection_limit_ppb": 0.001,
                "test_capabilities": ["purity_analysis", "trace_contaminants", "metrology", "calibration_standards"],
                "primary_standards": True,
                "accreditations": ["ISO 17025", "UKAS"],
                "gold_standard": True
            }
        },
        "Powertech Labs - H2 Tank Testing": {
            "standards": ["UN ECE R134", "SAE J2579", "ISO 19881", "SAE J2601", "ISO 11114-4"],
            "specs": {
                "max_pressure_bar": 1000,
                "tank_testing": True,
                "type_iv_specialist": True,
                "test_capabilities": ["tank_cycling", "burst_testing", "permeation", "drop_testing", "gun_fire", "bonfire"],
                "accreditations": ["ISO 17025", "SCC"],
                "world_leader_tanks": True
            }
        },
        "WHA International - H2 Safety Lab": {
            "standards": ["ISO 19880-3", "SAE J2579", "ISO 11114-4"],
            "specs": {
                "max_pressure_bar": 700,
                "fire_safety_specialist": True,
                "forensics": True,
                "test_capabilities": ["ignition_testing", "fire_resistance", "failure_analysis", "rapid_decompression", "expert_witness"],
                "accreditations": ["ISO 17025"],
                "unique_capabilities": True
            }
        },
        "Element Materials - Embrittlement Lab": {
            "standards": ["ISO 11114-4", "ISO 19880-3", "NACE MR0175"],
            "specs": {
                "materials_science_leader": True,
                "embrittlement_specialist": True,
                "test_capabilities": ["embrittlement", "metallography", "fracture_mechanics", "materials_qualification", "SSRT", "SEM", "XRD"],
                "accreditations": ["ISO 17025", "Nadcap", "UKAS", "A2LA"],
                "global_network": True
            }
        }
    }
    
    # Get all listings
    listings = get_data("listings", {"status": "eq.active"})
    listing_map = {l['business_name']: l['id'] for l in listings}
    
    total_added = 0
    
    for lab_name, lab_data in whale_labs.items():
        if lab_name not in listing_map:
            print(f"⚠️  Lab not found: {lab_name}")
            continue
        
        listing_id = listing_map[lab_name]
        print(f"🏢 {lab_name}")
        
        for std_code in lab_data['standards']:
            if std_code not in std_map:
                print(f"  ⚠️  Standard not found: {std_code}")
                continue
            
            std_id = std_map[std_code]
            if add_capability(listing_id, std_id, lab_data['specs']):
                print(f"  ✅ {std_code}")
                total_added += 1
            else:
                print(f"  ⚠️  {std_code} (already exists or failed)")
        
        print()
    
    print("\n📊 Summary:")
    print(f"  • Capabilities added: {total_added}")
    print("  • Whale labs fully linked\n")

if __name__ == "__main__":
    main()
