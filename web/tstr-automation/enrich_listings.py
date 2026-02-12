
import os
import httpx
import time
import random
try:
    from duckduckgo_search import DDGS
except ImportError:
    print("Installing duckduckgo-search...")
    os.system("pip install duckduckgo-search")
    from duckduckgo_search import DDGS

# Configuration
SUPABASE_URL = "https://haimjeaetrsaauitrhfy.supabase.co"
# Service Key (from web/tstr-automation/.env)
SUPABASE_KEY = "sb_secret_[REDACTED]" 

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}

def fetch_table(table_name, select="*"):
    url = f"{SUPABASE_URL}/rest/v1/{table_name}?select={select}"
    try:
        response = httpx.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching {table_name}: {e}")
        return []

def search_ddg(query, num_results=3):
    try:
        results = []
        with DDGS() as ddgs:
            # DDGS text search
            for r in ddgs.text(query, max_results=num_results):
                results.append(r)
        return results
    except Exception as e:
        print(f"Search error for '{query}': {e}")
        return []

def enrich_listings():
    print("Fetching listings needing enrichment...")
    
    url = f"{SUPABASE_URL}/rest/v1/listings?select=id,business_name,address,website,listing_premium_data(id)"
    try:
        resp = httpx.get(url, headers=HEADERS)
        listings = resp.json()
    except Exception as e:
        print(f"Error fetching listings: {e}")
        return

    # Filter: processed if existing website OR existing premium data
    to_process = []
    for l in listings:
        has_premium = len(l.get('listing_premium_data', [])) > 0
        has_website = bool(l.get('website'))
        
        # We want to process if MISSING website OR MISSING premium (linkedin)
        if not has_website or not has_premium:
            to_process.append(l)

    print(f"Found {len(to_process)} listings to enrich.")
    
    # Process in small batches
    processed_count = 0
    
    for listing in to_process:
        lid = listing['id']
        name = listing['business_name']
        address = listing['address'] or ""
        
        print(f"Enriching: {name}...")
        
        # 1. Search for Official Website
        website = listing.get('website')
        if not website:
            query = f"{name} {address} official website"
            results = search_ddg(query, 3)
            if results:
                # Naive check: look for results that aren't social media/directories
                excluded_domains = [
                    "linkedin.com", "facebook.com", "zoominfo.com", 
                    "wikipedia.org", "zhihu.com", "instagram.com", 
                    "twitter.com", "youtube.com", "glassdoor.com",
                    "crunchbase.com", "bloomberg.com", "dnb.com"
                ]
                
                for res in results:
                    url = res['href']
                    if not any(d in url for d in excluded_domains):
                        website = url
                        print(f"  Found Website: {website}")
                        break
        
        # 2. Search for LinkedIn
        linkedin_url = None
        query_li = f"{name} linkedin company" # Simplified query
        results_li = search_ddg(query_li, 3)
        for res in results_li:
            if "linkedin.com/company" in res['href']:
                linkedin_url = res['href']
                print(f"  Found LinkedIn: {linkedin_url}")
                break
        
        # Update updates
        if website and website != listing.get('website'):
            try:
                httpx.patch(
                    f"{SUPABASE_URL}/rest/v1/listings?id=eq.{lid}",
                    headers=HEADERS,
                    json={"website": website}
                )
            except Exception as e:
                print(f"  Failed to update website: {e}")

        if linkedin_url:
            existing_prem = listing.get('listing_premium_data', [])
            if existing_prem:
                 pid = existing_prem[0]['id']
                 httpx.patch(
                    f"{SUPABASE_URL}/rest/v1/listing_premium_data?id=eq.{pid}",
                    headers=HEADERS,
                    json={"linkedin_url": linkedin_url}
                 )
            else:
                httpx.post(
                    f"{SUPABASE_URL}/rest/v1/listing_premium_data",
                    headers=HEADERS,
                    json={"listing_id": lid, "linkedin_url": linkedin_url}
                )

        processed_count += 1
        time.sleep(random.uniform(2, 4))
        
        if processed_count >= 10: 
            print("Processed 10 listings. Stopping for safety.")
            break

if __name__ == "__main__":
    enrich_listings()
