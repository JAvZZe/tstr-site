import os
import requests
from collections import Counter
from dotenv import load_dotenv

# Load environment variables
ENV_PATH = '/media/al/AI_DATA/AI_PROJECTS_SPACE/ACTIVE_PROJECTS/tstr-site-working/web/tstr-automation/.env'
load_dotenv(dotenv_path=ENV_PATH)

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("PUBLIC_SUPABASE_ANON_KEY")

def query_postgrest(table, select="*", order=None, limit=None):
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}"
    }
    url = f"{SUPABASE_URL}/rest/v1/{table}?select={select}"
    if order:
        url += f"&order={order}"
    if limit:
        url += f"&limit={limit}"
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return []
    return response.json()

def get_pseo_stats():
    print("--- TSTR PSEO Health Check ---")
    
    # 1. Fetch Listings with Category and Location Slugs
    # We'll use the relationships if they are defined in Postgrest
    # select=business_name,slug,categories(name,slug),locations(name,slug)
    data = query_postgrest("listings", select="business_name,slug,categories(name,slug),locations(name,slug),website,updated_at")
    
    if not data:
        print("Failed to fetch listings or relationship join failed.")
        # Fallback to simple select
        data = query_postgrest("listings", select="business_name,slug,website,updated_at")
    
    # 2. Get Enrichment counts
    total = len(data)
    with_web = sum(1 for x in data if x.get('website'))
    
    # We can't easily check premium_data via anon key because of RLS
    # but we can check recently updated listings
    sorted_data = sorted(data, key=lambda x: x.get('updated_at', ''), reverse=True)
    
    print("\n[SUMMARY]")
    print(f"  Total Listings: {total}")
    print(f"  With Website: {with_web} ({round(with_web/total*100, 1) if total > 0 else 0}%)")
    
    # 3. Top Categories (simulated from slugs if needed)
    categories = [x.get('categories', {}).get('name') for x in data if x.get('categories')]
    top_cats = Counter(categories).most_common(5)
    print("\n[TOP CATEGORIES]")
    for cat, count in top_cats:
        print(f"  {cat}: {count} listings")

    # 4. Target URLs for Verification
    print("\n[AUDIT TARGETS]")
    
    # Sample Top Category Page
    if data and any(x.get('categories') for x in data):
        top_cat_slug = next(x['categories']['slug'] for x in data if x.get('categories'))
        print(f"  Category Page: https://tstr.directory/{top_cat_slug}")
    
    # Sample Recently Updated Listing
    if sorted_data:
        sample = sorted_data[0]
        print(f"  Recent Listing: https://tstr.directory/listing/{sample['slug']} (Updated: {sample['updated_at']})")

    # Sample Standard Page (hardcoded common ones)
    print("  Standard Page: https://tstr.directory/standards/iso-17025")

if __name__ == "__main__":
    get_pseo_stats()
