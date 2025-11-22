#!/usr/bin/env python3
"""
Add remaining capabilities for Oil & Gas and Biotech categories
"""

import requests
from datetime import datetime

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

def insert_capability(listing_id, standard_id, specifications=None):
    """Insert a listing capability"""
    url = f"{SUPABASE_URL}/rest/v1/listing_capabilities"
    data = {
        "listing_id": listing_id,
        "standard_id": standard_id,
        "specifications": specifications or {},
        "verified": False
    }
    
    response = requests.post(url, headers=headers, json=data)
    return response.status_code in [200, 201]

def main():
    print("🔗 Adding remaining capabilities...\n")

    # Get categories
    categories = get_data("categories")
    cat_map = {cat['slug']: cat for cat in categories}
    
    # Get standards for Oil & Gas and Biotech
    oil_gas_cat_id = cat_map['oil-gas-testing']['id']
    biotech_cat_id = cat_map['biotech-testing']['id']
    
    oil_gas_standards = get_data("standards", {"category_id": f"eq.{oil_gas_cat_id}"})
    biotech_standards = get_data("standards", {"category_id": f"eq.{biotech_cat_id}"})
    general_standards = get_data("standards", {"category_id": "is.null", "code": "eq.ISO 17025"})
    
    print(f"📊 Oil & Gas standards: {len(oil_gas_standards)}")
    print(f"📊 Biotech standards: {len(biotech_standards)}")
    print(f"📊 General standards: {len(general_standards)}\n")
    
    # Get Oil & Gas listings
    listings = get_data("listings", {"status": "eq.active", "category_id": f"eq.{oil_gas_cat_id}", "limit": "5"})
    print(f"📋 Processing {len(listings)} Oil & Gas listings\n")
    
    total_added = 0
    
    for listing in listings[:3]:
        print(f"🔬 {listing['business_name']}")
        
        for std in oil_gas_standards:
            specs = {}
            if 'hydrogen' in std['name'].lower() or 'ISO 19' in std['code']:
                specs = {
                    "max_pressure_bar": 700,
                    "temperature_range_c": [-40, 85],
                    "test_capabilities": ["valve_testing", "material_compatibility"]
                }
            elif 'API' in std['code']:
                specs = {
                    "inspection_types": ["visual", "ultrasonic", "radiographic"],
                    "equipment_types": ["pressure_vessels", "piping", "storage_tanks"]
                }
            
            if insert_capability(listing['id'], std['id'], specs):
                print(f"  ✅ {std['code']}")
                total_added += 1
        
        # Add general standard
        if general_standards:
            specs = {"accredited": True, "scope": "Testing and Calibration"}
            if insert_capability(listing['id'], general_standards[0]['id'], specs):
                print(f"  ✅ ISO 17025 (general)")
                total_added += 1
    
    # Get Biotech listings
    listings = get_data("listings", {"status": "eq.active", "category_id": f"eq.{biotech_cat_id}", "limit": "10"})
    if listings and len(listings) > 0:
        print(f"\n📋 Processing {len(listings)} Biotech listings\n")
        
        for listing in listings[:3]:
            print(f"🔬 {listing['business_name']}")
            
            for std in biotech_standards:
                specs = {}
                if 'biobank' in std['name'].lower():
                    specs = {
                        "biosafety_level": "BSL-2",
                        "storage_temperature": "-80C to -196C",
                        "sample_tracking": True
                    }
                elif 'medical' in std['name'].lower():
                    specs = {
                        "device_types": ["diagnostic", "therapeutic"],
                        "quality_management": True
                    }
                
                if insert_capability(listing['id'], std['id'], specs):
                    print(f"  ✅ {std['code']}")
                    total_added += 1
            
            # Add general standard
            if general_standards:
                specs = {"accredited": True, "scope": "Biological Testing"}
                if insert_capability(listing['id'], general_standards[0]['id'], specs):
                    print(f"  ✅ ISO 17025 (general)")
                    total_added += 1
    
    print(f"\n\n📊 Summary:")
    print(f"  • Capabilities added: {total_added}")
    print("\n✅ Complete!\n")

if __name__ == "__main__":
    main()
