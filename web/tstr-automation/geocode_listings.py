
import os
import time
import argparse
import requests
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

# Configuration
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
GMAPS_KEY = os.environ.get("GOOGLE_MAPS_API_KEY")
GEOCODE_URL = "https://maps.googleapis.com/maps/api/geocode/json"

if not all([SUPABASE_URL, SUPABASE_KEY, GMAPS_KEY]):
    print("Error: Missing environment variables. Check .env")
    exit(1)

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def geocode(address, city, state, country):
    """Call Google Geocoding API."""
    query_parts = [address, city, state, country]
    # Filter out None or empty strings
    query = ", ".join([p for p in query_parts if p])
    if not query:
        return None
        
    try:
        r = requests.get(GEOCODE_URL, params={"address": query, "key": GMAPS_KEY})
        data = r.json()
        if data["status"] == "OK":
            loc = data["results"][0]["geometry"]["location"]
            return loc["lat"], loc["lng"]
        else:
            print(f"  ⚠️ Geocode API error for '{query}': {data['status']}")
            return None
    except Exception as e:
        print(f"  ❌ Geocode request failed: {e}")
        return None

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="Don't write to DB")
    parser.add_argument("--limit", type=int, default=10, help="Max listings to process")
    args = parser.parse_args()

    # Fetch listings where lat/lng is NULL or 0
    query = supabase.table("listings").select(
        "id, business_name, address, region"
    ).or_("latitude.is.null,latitude.eq.0").limit(args.limit)
    
    response = query.execute()
    rows = response.data

    if not rows:
        print("No listings found needing geocoding.")
        return

    print(f"{'DRY RUN - ' if args.dry_run else ''}Processing {len(rows)} listings...")
    
    success_count = 0
    fail_count = 0

    for row in rows:
        name = row.get("business_name", "Unknown")
        address = row.get("address")
        state = row.get("region")
        
        # Skip geocoding for 'global' or 'remote' listings that lack a real address
        is_global = str(address).lower() in ['global', 'remote', 'none', 'null'] or str(state).lower() == 'global'
        
        if is_global and (not address or len(address) < 5):
            print(f"Skipping Global/Remote listing: {name}")
            # We mark as 'success' in the sense that we processed it and decided it shouldn't have coordinates
            # To prevent re-processing, we could set a tiny non-zero value or use a different flag.
            # For now, we'll just set it to 0.000001 to distinguish it from NULL/0
            if not args.dry_run:
                try:
                    supabase.table("listings").update(
                        {"latitude": 0.000001, "longitude": 0.000001, "updated_at": "now()"}
                    ).eq("id", row["id"]).execute()
                    print(f"  ✅ Marked as Global (0.000001)")
                except Exception as e:
                    print(f"  ❌ DB Update failed: {e}")
                    fail_count += 1
                    continue
            else:
                print(f"  ✅ [DRY RUN] Would mark as Global")
            success_count += 1
            continue

        print(f"Geocoding: {name} ({state})...")
        coords = geocode(address, None, state, None)
        
        if coords:
            lat, lng = coords
            if not args.dry_run:
                try:
                    supabase.table("listings").update(
                        {"latitude": lat, "longitude": lng, "updated_at": "now()"}
                    ).eq("id", row["id"]).execute()
                    print(f"  ✅ Updated: {lat}, {lng}")
                except Exception as e:
                    print(f"  ❌ DB Update failed: {e}")
                    fail_count += 1
                    continue
            else:
                print(f"  ✅ [DRY RUN] Would update: {lat}, {lng}")
            
            success_count += 1
        else:
            fail_count += 1
        
        # Respect rate limits and be gentle
        time.sleep(0.1)

    print(f"\nSummary: {success_count} processed/updated, {fail_count} failed geocoding.")

if __name__ == "__main__":
    main()
