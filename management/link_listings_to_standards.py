#!/usr/bin/env python3
"""
Link listings to appropriate standards based on their category
"""

import requests
import json
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
    if response.status_code == 200:
        return response.json()
    return None

def insert_capability(listing_id, standard_id, specifications=None, verified=False):
    """Insert a listing capability"""
    url = f"{SUPABASE_URL}/rest/v1/listing_capabilities"
    data = {
        "listing_id": listing_id,
        "standard_id": standard_id,
        "specifications": specifications or {},
        "verified": verified,
        "verified_at": datetime.utcnow().isoformat() if verified else None
    }
    
    response = requests.post(url, headers=headers, json=data)
    return response.status_code in [200, 201]

def main():
    print("🔗 Linking listings to standards...\n")

    # Get categories
    categories = get_data("categories")
    cat_map = {cat['id']: cat for cat in categories}
    cat_slug_to_id = {cat['slug']: cat['id'] for cat in categories}
    
    # Get all standards by category
    standards = get_data("standards", {"is_active": "eq.true"})
    std_by_category = {}
    general_standards = []
    
    for std in standards:
        if std['category_id']:
            cat_id = std['category_id']
            if cat_id not in std_by_category:
                std_by_category[cat_id] = []
            std_by_category[cat_id].append(std)
        else:
            general_standards.append(std)
    
    print(f"📊 Found {len(standards)} standards")
    print(f"   - {sum(len(v) for v in std_by_category.values())} category-specific")
    print(f"   - {len(general_standards)} general\n")
    
    # Get sample listings from each category
    listings = get_data("listings", {"status": "eq.active", "order": "business_name", "limit": "200"})
    
    # Group by category
    listings_by_cat = {}
    for listing in listings:
        cat_id = listing['category_id']
        if cat_id:
            if cat_id not in listings_by_cat:
                listings_by_cat[cat_id] = []
            listings_by_cat[cat_id].append(listing)
    
    # Link listings - start with 3 per category
    total_added = 0
    
    for cat_id, cat_listings in listings_by_cat.items():
        cat_name = cat_map[cat_id]['name']
        cat_standards = std_by_category.get(cat_id, [])
        
        if not cat_standards:
            print(f"⊘ {cat_name}: No category-specific standards")
            continue
        
        print(f"\n📋 {cat_name}:")
        print(f"   {len(cat_listings)} listings, {len(cat_standards)} standards")
        
        # Take first 3 listings from this category
        sample_listings = cat_listings[:3]
        
        for listing in sample_listings:
            print(f"\n  🔬 {listing['business_name']}")
            
            # Add each category standard to this listing
            for std in cat_standards:
                # Create specifications based on category
                specs = {}
                
                # Add category-specific example specs
                if cat_map[cat_id]['slug'] == 'oil-gas-testing':
                    if 'hydrogen' in std['name'].lower() or 'ISO 19' in std['code']:
                        specs = {
                            "max_pressure_bar": 700,
                            "temperature_range_c": [-40, 85]
                        }
                    elif 'API' in std['code'] or 'ASTM' in std['code']:
                        specs = {
                            "test_methods": ["visual_inspection", "pressure_testing"],
                            "materials_tested": ["steel", "alloys"]
                        }
                
                elif cat_map[cat_id]['slug'] == 'pharmaceutical-testing':
                    if 'USP' in std['code']:
                        specs = {
                            "gmp_certified": True,
                            "cleanroom_iso_class": "ISO 7",
                            "sterility_testing": True
                        }
                    elif 'FDA' in std['code']:
                        specs = {
                            "fda_registered": True,
                            "gmp_certified": True
                        }
                
                elif cat_map[cat_id]['slug'] == 'materials-testing':
                    if 'tensile' in std['name'].lower():
                        specs = {
                            "tensile_strength_max_mpa": 2000,
                            "temperature_range_c": [-196, 1000]
                        }
                    elif 'impact' in std['name'].lower():
                        specs = {
                            "test_temperature_c": -40,
                            "energy_range_j": [0, 300]
                        }
                
                elif cat_map[cat_id]['slug'] == 'environmental-testing':
                    if 'EPA' in std['code']:
                        specs = {
                            "detection_limit_ppm": 0.001,
                            "sample_types": ["water", "soil", "air"]
                        }
                
                elif cat_map[cat_id]['slug'] == 'biotech-testing':
                    if 'biobank' in std['name'].lower():
                        specs = {
                            "biosafety_level": "BSL-2",
                            "sample_storage": True,
                            "temperature_control": "-80C to -196C"
                        }
                
                # Insert capability
                if insert_capability(listing['id'], std['id'], specs, verified=False):
                    print(f"     ✅ {std['code']}")
                    total_added += 1
                else:
                    print(f"     ❌ {std['code']} (failed)")
            
            # Also add general standards (ISO 17025, ISO 17020)
            for gen_std in general_standards[:1]:  # Just add ISO 17025 for now
                specs = {
                    "accredited": True,
                    "scope": "Testing and Calibration"
                }
                if insert_capability(listing['id'], gen_std['id'], specs, verified=False):
                    print(f"     ✅ {gen_std['code']} (general)")
                    total_added += 1
    
    print(f"\n\n📊 Summary:")
    print(f"  • Total capabilities added: {total_added}")
    print(f"  • Listings updated: {sum(len(cat_listings[:3]) for cat_listings in listings_by_cat.values())}")
    print("\n✅ Linking complete!\n")

if __name__ == "__main__":
    main()
