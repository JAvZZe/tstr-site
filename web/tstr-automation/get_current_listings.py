import requests

SUPABASE_URL = "https://haimjeaetrsaauitrhfy.supabase.co"
SUPABASE_KEY = "sb_secret_zRN1fTFOYnN7cEbEIfAP7A_YrEKBfI2"

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

def get_data():
    # Fetch Categories
    try:
        resp_cat = requests.get(f"{SUPABASE_URL}/rest/v1/categories?select=id,name", headers=headers)
        resp_cat.raise_for_status()
        categories = resp_cat.json()
        cat_map = {c['id']: c['name'] for c in categories}
    except Exception as e:
        print(f"Error fetching categories: {e}")
        cat_map = {}

    # Fetch Listings
    try:
        # Note: status=eq.active
        resp_list = requests.get(f"{SUPABASE_URL}/rest/v1/listings?select=business_name,slug,category_id,status&status=eq.active", headers=headers)
        resp_list.raise_for_status()
        listings = resp_list.json()
    except Exception as e:
        print(f"Error fetching listings: {e}")
        return

    print(f"Total Active Listings: {len(listings)}")
    print("-" * 40)
    for listing in listings:
        c_name = cat_map.get(listing['category_id'], "Unknown")
        print(f"{listing['business_name']} | {c_name} | {listing['slug']}")

if __name__ == "__main__":
    get_data()
