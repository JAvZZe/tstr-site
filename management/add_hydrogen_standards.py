#!/usr/bin/env python3
"""
Add critical hydrogen testing standards that are missing
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

def add_standard(code, name, description, issuing_body, category_id, standard_type, url_ref=None):
    """Add a new standard"""
    api_url = f"{SUPABASE_URL}/rest/v1/standards"
    data = {
        "id": str(uuid.uuid4()),
        "code": code,
        "name": name,
        "description": description,
        "issuing_body": issuing_body,
        "category_id": category_id,
        "standard_type": standard_type,
        "url": url_ref,
        "is_active": True
    }
    
    response = requests.post(api_url, headers=headers, json=data)
    return response.status_code in [200, 201], data['id']

def main():
    print("🔬 Adding critical hydrogen testing standards...\n")
    
    # Get Oil & Gas category ID
    cat_id = get_category_id("oil-gas-testing")
    if not cat_id:
        print("❌ Oil & Gas category not found")
        return
    
    print(f"✅ Found Oil & Gas category: {cat_id}\n")
    
    # Critical hydrogen standards to add
    standards = [
        {
            "code": "ISO 19880-5",
            "name": "Hydrogen Fuelling Stations - Part 5: Hoses",
            "description": "Specifies requirements for hoses used in hydrogen fuelling stations. Critical for high-pressure hydrogen transfer with minimal permeation and maximum safety.",
            "issuing_body": "ISO",
            "standard_type": "test_method",
            "url": "https://www.iso.org/standard/71942.html"
        },
        {
            "code": "ISO 11114-4",
            "name": "Gas Cylinders - Compatibility of Materials - Part 4: Test Methods for Hydrogen Embrittlement",
            "description": "Test methods for selecting metallic materials resistant to hydrogen embrittlement. Essential for component design and material qualification.",
            "issuing_body": "ISO",
            "standard_type": "test_method",
            "url": "https://www.iso.org/standard/50507.html"
        },
        {
            "code": "UN ECE R134",
            "name": "Hydrogen and Fuel Cell Vehicles - Safety Requirements",
            "description": "Uniform provisions concerning the approval of motor vehicles with regard to safety-related performance of hydrogen systems. Mandatory for EU market access.",
            "issuing_body": "UN ECE",
            "standard_type": "certification",
            "url": "https://unece.org/transport/standards/transport/vehicle-regulations-wp29/global-technical-regulations-gtrs"
        },
        {
            "code": "SAE J2579",
            "name": "Fuel Systems in Fuel Cell and Other Hydrogen Vehicles",
            "description": "Technical information report for fuel systems in hydrogen vehicles. Covers safety requirements for design, materials, and testing.",
            "issuing_body": "SAE",
            "standard_type": "certification",
            "url": "https://www.sae.org/standards/content/j2579_202009/"
        },
        {
            "code": "CSA HGV 4.3",
            "name": "Test Methods for Hydrogen Fueling Parameter Evaluation",
            "description": "Canadian standard for testing hydrogen fueling parameters. Widely used in North America for station validation.",
            "issuing_body": "CSA",
            "standard_type": "test_method",
            "url": "https://www.csagroup.org/"
        }
    ]
    
    added = 0
    failed = 0
    
    for std in standards:
        success, std_id = add_standard(
            std['code'],
            std['name'],
            std['description'],
            std['issuing_body'],
            cat_id,
            std['standard_type'],
            std.get('url')
        )
        
        if success:
            print(f"  ✅ {std['code']}")
            print(f"     {std['name']}")
            added += 1
        else:
            print(f"  ❌ {std['code']} (failed)")
            failed += 1
    
    print(f"\n📊 Summary:")
    print(f"  • Added: {added}")
    print(f"  • Failed: {failed}")
    print(f"  • Total hydrogen standards: {added + 5}")  # 5 existing
    print("\n✅ Hydrogen standards enhanced!\n")

if __name__ == "__main__":
    main()
