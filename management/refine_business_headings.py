#!/usr/bin/env python3
"""
Refine business headings: Separate service descriptors into capabilities/tags.
"""
import os

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
    print("🚀 Refining Business Headings & Service Tags...\n")

    # 1. Create Service-based "Standards" to act as Tags
    services = [
        {"code": "AIM", "name": "Asset Integrity Management", "standard_type": "certification"},
        {"code": "H2-SAFETY", "name": "Hydrogen Safety Testing", "standard_type": "certification"},
        {"code": "H2-TANK", "name": "Hydrogen Tank Testing", "standard_type": "certification"},
        {"code": "EMBRITTLEMENT", "name": "Hydrogen Embrittlement Lab", "standard_type": "certification"},
        {"code": "NDT-SERVICE", "name": "Non-Destructive Testing Services", "standard_type": "certification"}
    ]

    service_map = {}
    for svc in services:
        sid = get_id("standards", "code", svc['code'])
        if not sid:
            resp = requests.post(f"{SUPABASE_URL}/rest/v1/standards", headers=headers, json=svc)
            sid = resp.json()[0]['id']
            print(f"✅ Created Service Tag: {svc['name']}")
        service_map[svc['code']] = sid

    # 2. Cleanup List
    targets = [
        {"slug": "tuv-sud---hydrogen-testing", "new_name": "TÜV SÜD", "tags": ["AIM", "H2-SAFETY"]},
        {"slug": "wha-international---h2-safety-lab", "new_name": "WHA International", "tags": ["H2-SAFETY"]},
        {"slug": "powertech-labs---h2-tank-testing", "new_name": "Powertech Labs", "tags": ["H2-TANK"]},
        {"slug": "kiwa-technology---h2-testing", "new_name": "Kiwa Technology", "tags": ["H2-SAFETY"]},
        {"slug": "element-materials---embrittlement-lab", "new_name": "Element Materials", "tags": ["EMBRITTLEMENT"]},
        {"slug": "npl---national-physical-laboratory", "new_name": "NPL", "tags": ["NDT-SERVICE"]}
    ]

    for t in targets:
        lid = get_id("listings", "slug", t['slug'])
        if lid:
            print(f"🏢 Updating {t['new_name']}...")
            # Update name
            requests.patch(f"{SUPABASE_URL}/rest/v1/listings?id=eq.{lid}", headers=headers, json={"business_name": t['new_name']})
            
            # Link tags as capabilities
            for tcode in t['tags']:
                sid = service_map[tcode]
                # Check if already linked
                check = requests.get(f"{SUPABASE_URL}/rest/v1/listing_capabilities?listing_id=eq.{lid}&standard_id=eq.{sid}", headers=headers).json()
                if not check:
                    requests.post(f"{SUPABASE_URL}/rest/v1/listing_capabilities", headers=headers, json={
                        "listing_id": lid,
                        "standard_id": sid,
                        "verified": True
                    })
                    print(f"  ✅ Linked {tcode}")
        else:
            print(f"  ⚠️ Listing {t['slug']} not found.")

    print("\n✨ Refinement complete!")

if __name__ == "__main__":
    main()
