#!/usr/bin/env python3
"""
Link new hydrogen standards to existing Oil & Gas labs
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
    """Fetch data from Supabase"""
    url = f"{SUPABASE_URL}/rest/v1/{table}"
    params = {"select": "*"}
    if filters:
        params.update(filters)
    
    response = requests.get(url, headers=headers, params=params)
    return response.json() if response.status_code == 200 else None

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
    print("🔗 Linking new hydrogen standards to existing labs...\n")
    
    # Get Oil & Gas category
    categories = get_data("categories", {"slug": "eq.oil-gas-testing"})
    if not categories:
        print("❌ Category not found")
        return
    
    
    # Get new hydrogen standards
    new_standards = get_data("standards", {
        "code": "in.(ISO 19880-5,ISO 11114-4,UN ECE R134,SAE J2579,CSA HGV 4.3)"
    })
    
    if not new_standards:
        print("❌ No new standards found")
        return
    
    print(f"📋 Found {len(new_standards)} new hydrogen standards:")
    for std in new_standards:
        print(f"  • {std['code']}")
    print()
    
    # Get existing Oil & Gas labs with hydrogen capabilities
    existing_caps = get_data("listing_capabilities", {"limit": "1000"})
    
    # Find labs that already have ISO 19880-3
    h2_lab_ids = set()
    for cap in existing_caps or []:
        listing_id = cap['listing_id']
        std = get_data("standards", {"id": f"eq.{cap['standard_id']}"})
        if std and std[0]['code'] in ['ISO 19880-3', 'SAE J2601', 'ISO 14687']:
            h2_lab_ids.add(listing_id)
    
    print(f"🔬 Found {len(h2_lab_ids)} existing H2 labs\n")
    
    if len(h2_lab_ids) == 0:
        print("⚠️  No existing hydrogen labs found")
        return
    
    # Add new standards to these labs
    total_added = 0
    
    for listing_id in list(h2_lab_ids)[:10]:  # Limit to 10 labs
        # Get listing info
        listings = get_data("listings", {"id": f"eq.{listing_id}"})
        if not listings:
            continue
        
        listing = listings[0]
        print(f"🏢 {listing['business_name']}")
        
        for std in new_standards:
            # Create enhanced specs for new standards
            specs = {
                "test_capabilities": ["advanced_h2_testing"],
                "temperature_range_c": [-253, 100]
            }
            
            if 'ISO 19880-5' in std['code']:  # Hoses
                specs.update({
                    "hose_testing": True,
                    "permeation_testing": True,
                    "max_pressure_bar": 700
                })
            elif 'ISO 11114-4' in std['code']:  # Embrittlement
                specs.update({
                    "embrittlement_testing": True,
                    "materials_qualification": True,
                    "metallurgical_analysis": True
                })
            elif 'UN ECE R134' in std['code']:  # Vehicle safety
                specs.update({
                    "vehicle_certification": True,
                    "tank_testing": True,
                    "crash_testing": False
                })
            elif 'SAE J2579' in std['code']:  # Fuel systems
                specs.update({
                    "fuel_system_testing": True,
                    "component_validation": True
                })
            elif 'CSA HGV 4.3' in std['code']:  # Fueling parameters
                specs.update({
                    "fueling_parameter_testing": True,
                    "station_validation": True
                })
            
            if add_capability(listing_id, std['id'], specs):
                print(f"  ✅ {std['code']}")
                total_added += 1
            else:
                print(f"  ⚠️  {std['code']} (already exists or failed)")
        
        print()
    
    print("\n📊 Summary:")
    print(f"  • New capabilities added: {total_added}")
    print(f"  • Labs enhanced: {min(len(h2_lab_ids), 10)}")
    print("\n✅ Hydrogen standards linked!\n")

if __name__ == "__main__":
    main()
