# ruff: noqa: E402

import os
from dotenv import load_dotenv
# Load environment variables from .env file in the same directory as this script
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

import random
import time
import httpx
from ddgs import DDGS

# Configuration
SUPABASE_URL = "https://haimjeaetrsaauitrhfy.supabase.co"
SUPABASE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY") 

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}

def search_ddg(query, num_results=3):
    """
    Search DuckDuckGo using the ddgs package.
    """
    try:
        ddgs = DDGS()
        results = list(ddgs.text(query, max_results=num_results))
        return results
    except Exception as e:
        print(f"Search error for '{query}': {e}")
        return []

def enrich_listings(limit=20):
    print("Fetching listings needing enrichment...")
    
    # Fetch listings and their premium data
    url = f"{SUPABASE_URL}/rest/v1/listings?select=id,business_name,address,website,listing_premium_data(id,linkedin_url)"
    try:
        resp = httpx.get(url, headers=HEADERS)
        resp.raise_for_status()
        listings = resp.json()
    except Exception as e:
        print(f"Error fetching listings: {e}")
        return

    # Filter: process if missing website OR missing linkedin_url
    to_process = []
    for item in listings:
        premium_data = item.get('listing_premium_data', [])
        has_linkedin = any(p.get('linkedin_url') for p in premium_data)
        has_website = bool(item.get('website'))
        
        if not has_website or not has_linkedin:
            to_process.append(item)

    print(f"Found {len(to_process)} listings potentially needing enrichment.")
    
    processed_count = 0
    updated_count = 0
    
    for listing in to_process:
        lid = listing['id']
        name = listing['business_name']
        address = listing['address'] or ""
        existing_website = listing.get('website')
        
        premium_records = listing.get('listing_premium_data', [])
        existing_linkedin = next((p.get('linkedin_url') for p in premium_records), None)
        premium_id = premium_records[0]['id'] if premium_records else None

        print(f"\n--- [{processed_count+1}/{limit}] Enriching: {name} ---")
        
        new_website = None
        new_linkedin = None

        # 1. Search for Official Website if missing
        if not existing_website:
            print("  Searching for website...")
            query = f"{name} {address} official website"
            results = search_ddg(query, 3)
            
            excluded_domains = [
                "linkedin.com", "facebook.com", "zoominfo.com", 
                "wikipedia.org", "zhihu.com", "instagram.com", 
                "twitter.com", "youtube.com", "glassdoor.com",
                "crunchbase.com", "bloomberg.com", "dnb.com", "yelp.com"
            ]
            
            for res in results:
                url_found = res['href']
                if not any(d in url_found.lower() for d in excluded_domains):
                    new_website = url_found
                    print(f"  [FOUND WEBSITE] {new_website}")
                    break
        else:
            print(f"  Website already present: {existing_website}")

        # 2. Search for LinkedIn if missing
        if not existing_linkedin:
            print("  Searching for LinkedIn...")
            query_li = f"{name} {address} linkedin company"
            results_li = search_ddg(query_li, 3)
            for res in results_li:
                if "linkedin.com/company" in res['href'].lower():
                    new_linkedin = res['href']
                    print(f"  [FOUND LINKEDIN] {new_linkedin}")
                    break
        else:
            print(f"  LinkedIn already present: {existing_linkedin}")

        # 3. Apply updates
        changes_made = False
        
        if new_website:
            try:
                patch_resp = httpx.patch(
                    f"{SUPABASE_URL}/rest/v1/listings?id=eq.{lid}",
                    headers=HEADERS,
                    json={"website": new_website}
                )
                patch_resp.raise_for_status()
                changes_made = True
                print("  Successfully updated website.")
            except Exception as e:
                print(f"  Failed to update website: {e}")

        if new_linkedin:
            try:
                if premium_id:
                    # Update existing record
                    patch_resp = httpx.patch(
                        f"{SUPABASE_URL}/rest/v1/listing_premium_data?id=eq.{premium_id}",
                        headers=HEADERS,
                        json={"linkedin_url": new_linkedin}
                    )
                else:
                    # Create new record
                    patch_resp = httpx.post(
                        f"{SUPABASE_URL}/rest/v1/listing_premium_data",
                        headers=HEADERS,
                        json={"listing_id": lid, "linkedin_url": new_linkedin}
                    )
                patch_resp.raise_for_status()
                changes_made = True
                print("  Successfully updated LinkedIn URL.")
            except Exception as e:
                print(f"  Failed to update LinkedIn: {e}")

        if changes_made:
            updated_count += 1
        else:
            print("  No new data found or updated.")

        processed_count += 1
        if processed_count >= limit:
            break
            
        # Rate limiting: polite delay
        time.sleep(random.uniform(2, 5))

    print("\nFinished batch processing.")
    print(f"Total processed: {processed_count}")
    print(f"Total updated: {updated_count}")

if __name__ == "__main__":
    enrich_listings(limit=20)
