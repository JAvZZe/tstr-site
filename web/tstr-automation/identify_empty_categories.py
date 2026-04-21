import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

SUPABASE_URL = "https://haimjeaetrsaauitrhfy.supabase.co"
SUPABASE_KEY = os.environ.get("PUBLIC_SUPABASE_ANON_KEY")

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

def check_categories():
    print("🔍 Scanning for categories with zero active listings...")
    
    # 1. Fetch all categories
    try:
        resp = requests.get(f"{SUPABASE_URL}/rest/v1/categories?select=id,name,slug", headers=headers)
        resp.raise_for_status()
        categories = resp.json()
    except Exception as e:
        print(f"Error fetching categories: {e}")
        return

    # 2. Fetch all active listings
    try:
        resp = requests.get(f"{SUPABASE_URL}/rest/v1/listings?select=category_id&status=eq.active", headers=headers)
        resp.raise_for_status()
        listings = resp.json()
    except Exception as e:
        print(f"Error fetching listings: {e}")
        return

    # Map category_id to actual active listing count
    listing_counts = {}
    for listing in listings:
        cid = listing.get('category_id')
        if cid:
            listing_counts[cid] = listing_counts.get(cid, 0) + 1

    print(f"\nFound {len(categories)} total categories and {len(listings)} active listings.")
    
    empty_categories = []
    populated_categories = []
    
    for cat in categories:
        count = listing_counts.get(cat['id'], 0)
        if count == 0:
            empty_categories.append(cat)
        else:
            populated_categories.append((cat, count))

    print(f"\n✅ {len(populated_categories)} categories have active listings.")
    print(f"❌ {len(empty_categories)} categories have 0 active listings.")

    if empty_categories:
        print("\n--- EMPTY CATEGORIES ---")
        for cat in sorted(empty_categories, key=lambda x: x['name']):
            print(f"  - {cat['name']} (slug: {cat['slug']})")
            print(f"    URL: https://tstr.directory/browse?category={cat['slug']}")
    
    # Specific check for Aerospace NDT Services
    aerospace_cat = next((c for c in categories if c['slug'] == 'aerospace-ndt-services'), None)
    if aerospace_cat:
        count = listing_counts.get(aerospace_cat['id'], 0)
        print("\nTarget Check: Aerospace NDT Services (slug: aerospace-ndt-services)")
        print(f"Count: {count}")
        if count == 0:
            print("Status: ❌ EMPTY (Matches User report)")
        else:
            print("Status: ✅ POPULATED (Possibly fixed or different environment)")
    
    # Check if homepage pillars are showing empty categories
    PILLARS_CONFIG_SLUGS = [
        'hydrogen-infrastructure-testing',
        'materials-testing',
        'environmental-testing',
        'pharmaceutical-testing',
        'oil-gas-testing',
        'biotech-testing',
        'aerospace-testing',
        'ev-battery-testing',
        'railway-testing',
        'cybersecurity-testing',
        'telecom-5g-testing',
        'nuclear-testing',
        'building-construction-testing',
        'mining-geochemistry-testing',
        'defense-ballistics-testing',
        'acoustics-vibration-testing',
        'product-safety-emc-testing',
        'calibration-metrology-services'
    ]
    
    print("\n--- HOMEPAGE PILLAR AUDIT ---")
    for slug in PILLARS_CONFIG_SLUGS:
        cat = next((c for c in categories if c['slug'] == slug), None)
        if cat:
            count = listing_counts.get(cat['id'], 0)
            status = "✅ OK" if count > 0 else "⚠️ EMPTY (HIDDEN)"
            print(f"  - {cat['name']:<40} | Count: {count:<4} | {status}")
        else:
            print(f"  - {slug:<40} | Count: N/A  | ❌ NOT FOUND IN DB")

if __name__ == "__main__":
    check_categories()
