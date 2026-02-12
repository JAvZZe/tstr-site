import os
import json
import urllib.request
import urllib.error
from collections import defaultdict
from dotenv import load_dotenv

# Load env vars
load_dotenv('/media/al/AI_DATA/AI_PROJECTS_SPACE/ACTIVE_PROJECTS/TSTR-site/tstr-site-working/web/tstr-frontend/.env')

SUPABASE_URL = os.getenv("PUBLIC_SUPABASE_URL")
SUPABASE_KEY = os.getenv("PUBLIC_SUPABASE_ANON_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    print("Error: Missing SUPABASE_URL or PUBLIC_SUPABASE_ANON_KEY")
    exit(1)

def fetch_all(table, select="*"):
    results = []
    limit = 1000
    offset = 0
    
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json"
    }
    
    while True:
        # Construct URL with query params
        # select=...&limit=...&offset=...
        # Using manual string manip for standard lib purity
        url = f"{SUPABASE_URL}/rest/v1/{table}?select={select}&limit={limit}&offset={offset}"
        req = urllib.request.Request(url, headers=headers)
        
        try:
            with urllib.request.urlopen(req) as response:
                if response.status != 200:
                    print(f"Error fetching {table}: {response.status}")
                    break
                
                data = json.loads(response.read().decode())
                if not data:
                    break
                    
                results.extend(data)
                
                if len(data) < limit:
                    break
                
                offset += limit
                
        except urllib.error.URLError as e:
            print(f"Network Error fetching {table}: {e}")
            break
            
    return results

def analyze_data():
    print(f"Connecting to {SUPABASE_URL} via REST API...")
    
    # 1. Fetch Listings
    print("Fetching listings...")
    # We need category name and location name. REST API supports joins if configured, but simpler to fetch separately and join in memory for analysis script
    listings = fetch_all("listings", "id,business_name,slug,category_id,location_id,status")
    
    # 2. Fetch Categories
    print("Fetching categories...")
    categories = fetch_all("categories", "id,name,slug")
    cat_map = {c['id']: c['name'] for c in categories}
    
    # 3. Fetch Locations
    print("Fetching locations...")
    locations = fetch_all("locations", "id,name,slug")
    loc_map = {listing['id']: listing['name'] for listing in locations}
    
    active_listings = [listing for listing in listings if listing.get('status') != 'deleted']
    print(f"Total Active Listings: {len(active_listings)}")
    
    # 4. Analyze Duplicates (exact name match)
    name_map = defaultdict(list)
    for listing in active_listings:
        norm_name = (listing.get('business_name') or "").lower().strip()
        name_map[norm_name].append(listing)
        
    duplicates = {k: v for k,v in name_map.items() if len(v) > 1}
    print(f"\nPotential Duplicates (Same Business Name): {len(duplicates)}")
    
    for name, instances in list(duplicates.items())[:10]:
        print(f"\nAnalysis for: {name}")
        cats = set()
        locs = set()
        
        for i in instances:
            c_name = cat_map.get(i.get('category_id'), "Unknown")
            l_name = loc_map.get(i.get('location_id'), "Unknown")
            cats.add(c_name)
            locs.add(l_name)
            
        print(f"  - Count: {len(instances)}")
        print(f"  - Categories: {', '.join(cats)}")
        print(f"  - Locations: {', '.join(locs)}")
        
        if len(cats) > 1:
            print("  -> CROSS-CATEGORY DUPLICATE DETECTED")
        if len(locs) > 1 and len(cats) == 1:
             print("  -> MULTI-LOCATION LISTING DETECTED")

    # 5. Category Distribution
    cat_counts = defaultdict(int)
    for listing in active_listings:
        c_name = cat_map.get(listing.get('category_id'), "Unknown")
        cat_counts[c_name] += 1
        
    print("\nTop Categories:")
    for cat, count in sorted(cat_counts.items(), key=lambda x: x[1], reverse=True)[:10]:
         print(f"  - {cat}: {count}")

if __name__ == "__main__":
    analyze_data()
