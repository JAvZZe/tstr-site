
import re
import httpx

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

def create_slug(text):
    if text is None:
        return ""
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"[\s-]+", "-", text)
    text = text.strip("-")
    return text

def parse_linkedin_data(file_path):
    companies = []
    current_company = {}
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return []
        
    i = 0
    while i < len(lines):
        line = lines[i]
        
        if line == "Following":
            i += 1
            continue
            
        if line.startswith("Logo for "):
            i += 1
            if i < len(lines):
                current_company['name'] = lines[i]
                i += 1
        elif 'name' not in current_company:
             if i + 1 < len(lines) and " · " in lines[i+1]:
                 current_company['name'] = lines[i]
                 i += 1
             elif i + 1 < len(lines) and " · " not in lines[i+1] and "Followed" not in lines[i+1] and lines[i+1] != "Following" and not lines[i+1].startswith("Logo for"):
                 pass

        if 'name' in current_company and i < len(lines):
            details_line = lines[i]
            if " · " in details_line:
                parts = details_line.split(" · ")
                if len(parts) >= 2:
                    current_company['industry'] = parts[0].strip()
                    current_company['location'] = " · ".join(parts[1:]).strip()
                else:
                    current_company['industry'] = details_line
                    current_company['location'] = "Unknown"
            else:
                 current_company['industry'] = details_line
                 current_company['location'] = "Unknown"
            
            i += 1
            
            if i < len(lines) and lines[i].startswith("Followed"):
                 companies.append(current_company)
                 current_company = {}
                 i += 1
            else:
                companies.append(current_company)
                current_company = {}
                
        else:
            i += 1
            
    return companies

def fetch_table(table_name, select="*"):
    url = f"{SUPABASE_URL}/rest/v1/{table_name}?select={select}"
    try:
        response = httpx.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching {table_name}: {e}")
        return []

def insert_listings(listings):
    url = f"{SUPABASE_URL}/rest/v1/listings"
    try:
        batch_size = 100
        total_inserted = 0
        
        for i in range(0, len(listings), batch_size):
            batch = listings[i:i+batch_size]
            response = httpx.post(url, headers=HEADERS, json=batch)
            if response.status_code == 201:
                logging_data = response.json() if response.content else []
                total_inserted += len(logging_data) if logging_data else len(batch)
                print(f"Inserted batch {i//batch_size + 1}/{len(listings)//batch_size + 1}")
            else:
                print(f"Error inserting batch: {response.status_code} - {response.text}")
                
        return total_inserted
    except Exception as e:
        print(f"Error inserting listings: {e}")
        return 0

def sync_companies():
    print("Fetching existing data...")
    categories_data = fetch_table("categories", "id,name,slug")
    locations_data = fetch_table("locations", "id,name,slug")
    listings_data = fetch_table("listings", "business_name,slug")

    if not categories_data:
        print("Warning: No categories found.")
    
    categories = {cat["name"].lower(): cat["id"] for cat in categories_data}
    category_slugs = {cat["slug"]: cat["id"] for cat in categories_data} 
    
    locations = {loc["name"].lower(): loc["id"] for loc in locations_data}
    location_slugs = {loc["slug"]: loc["id"] for loc in locations_data}
    
    # Fetch all listings with IDs to check for missing links
    listings_data = fetch_table("listings", "id,business_name,slug")
    existing_listings_map = {l["business_name"].lower(): l for l in listings_data}
    existing_slugs = {l["slug"] for l in listings_data}
    
    # Fetch existing category links to avoid duplicates
    links_data = fetch_table("listing_categories", "listing_id,category_id")
    linked_listing_ids = {l["listing_id"] for l in links_data}
    
    # Mappings
    category_mapping = {
        "oil and gas": "oil-gas-testing",
        "renewable energy": "environmental-testing",
        "biotechnology research": "biotech-testing",
        "pharmaceutical manufacturing": "pharmaceutical-testing",
        "environmental services": "environmental-testing",
        "machinery manufacturing": "materials-testing",
        "chemicals": "materials-testing",
        "utilities": "environmental-testing",
        "mining": "materials-testing",
        "construction": "materials-testing",
        "medical equipment manufacturing": "medical-device-testing",
        "research services": "biotech-testing", 
        "industrial automation": "materials-testing",
        "semiconductors": "electrical-testing",
        "automotive": "automotive-testing",
        "defense and space": "aerospace-testing",
        "aviation and aerospace component manufacturing": "aerospace-testing",
        "civil engineering": "materials-testing",
        "mechanical or industrial engineering": "materials-testing",
        "plastics manufacturing": "materials-testing",
        "food and beverage manufacturing": "food-safety-testing",
        "medical device": "medical-device-testing",
        "hospital & health care": "clinical-testing",
        "information technology and services": "software-testing", 
        "computer software": "software-testing",
        "biotechnology": "biotech-testing",
        "transportation, logistics, supply chain and storage": "materials-testing", 
        "wholesale import and export": "materials-testing", 
        "business consulting and services": "software-testing", 
        "it services and it consulting": "software-testing",
        "non-profit organizations": "environmental-testing", 
        "government administration": "environmental-testing", 
        "higher education": "biotech-testing",
    }
    
    # Location mapping
    location_mapping = {
        "global": "global",
        "worldwide": "global",
        "remote": "global",
        "united states": "north-america",
        "usa": "north-america",
        "uk": "europe",
        "united kingdom": "europe",
        "germany": "europe",
        "france": "europe",
        "china": "asia-pacific",
        "india": "asia-pacific",
        "japan": "asia-pacific",
        "australia": "asia-pacific",
        "canada": "north-america",
        "brazil": "south-america",
        "south africa": "africa",
    }

    parsed_companies = parse_linkedin_data("linkedin_raw.txt")
    
    listings_to_insert = []
    links_to_insert = []
    
    count_new = 0
    count_linked = 0
    count_created_cats = 0
    
    print(f"Processing {len(parsed_companies)} parsed companies...")

    for company in parsed_companies:
        name = company.get('name')
        industry = company.get('industry')
        location_raw = company.get('location')
        
        if not name: continue
        
        # 1. Determine Category ID (Get or Create)
        cat_id = None
        if industry:
            ind_lower = industry.lower()
            if ind_lower in categories:
                cat_id = categories[ind_lower]
            elif ind_lower in category_mapping:
                 slug = category_mapping[ind_lower]
                 cat_id = category_slugs.get(slug)
            
            # If still no match, CREATE NEW CATEGORY
            if not cat_id:
                new_slug = create_slug(industry)
                if new_slug in category_slugs:
                    cat_id = category_slugs[new_slug]
                else:
                    print(f"Creating new category: {industry} ({new_slug})")
                    try:
                        resp = httpx.post(
                            f"{SUPABASE_URL}/rest/v1/categories",
                            headers=HEADERS,
                            json={"name": industry, "slug": new_slug}
                        )
                        if resp.status_code == 201:
                            new_cat = resp.json()[0] # Prefer return=representation
                            cat_id = new_cat['id']
                            # Update local cache
                            categories[industry.lower()] = cat_id
                            category_slugs[new_slug] = cat_id
                            count_created_cats += 1
                        else:
                            print(f"Failed to create category {industry}: {resp.text}")
                    except Exception as e:
                        print(f"Error creating category {industry}: {e}")

        # 2. Determine Location
        loc_id = None
        if location_raw:
            loc_lower = location_raw.lower()
            if loc_lower in locations:
                loc_id = locations[loc_lower]
            else:
                 # Try mapping
                for k, v in location_mapping.items():
                    if k in loc_lower:
                        loc_id = location_slugs.get(v)
                        break
        
        if not loc_id:
             loc_id = location_slugs.get("global") or location_slugs.get("unknown")

        # 3. Handle Listing
        listing_id = None
        
        if name.lower() in existing_listings_map:
            # Listing Exists - Check if linked
            listing_obj = existing_listings_map[name.lower()]
            listing_id = listing_obj['id']
            
            if listing_id not in linked_listing_ids:
                if cat_id:
                    links_to_insert.append({
                        "listing_id": listing_id,
                        "category_id": cat_id,
                        "is_primary": True
                    })
                    linked_listing_ids.add(listing_id) # Prevent dupes
                    count_linked += 1
        else:
            # New Listing
            slug = create_slug(name)
            if slug in existing_slugs:
                # Slug conflict but name didn't match? Skip/Warn
                print(f"Skipping {name} due to slug conflict {slug}")
                continue
            
            # Prepare for insertion
            # We must insert listing first to get ID, then link.
            # Batch insertion makes getting IDs harder unless we fetch back.
            # For simplicity with valid links, let's insert one-by-one or small batches and fetch back?
            # Or insert all new listings, THEN fetch all listings again to map names to IDs for linking.
            # Strategy: Insert listings batch -> Fetch all -> Create links batch.
            
            listings_to_insert.append({
                "business_name": name,
                "description": f"{industry} company based in {location_raw}. Imported from LinkedIn.",
                "status": "pending", 
                "slug": slug,
                "category_id": cat_id,
                "location_id": loc_id,
                "source_script": "sync_linkedin.py",
                "website": "", 
                "email": "",
                "phone": "",
                "address": location_raw,
                "_temp_cat_id": cat_id # Store for later linking
            })
            count_new += 1
            existing_slugs.add(slug)

    print(f"Summary: Found {len(listings_to_insert)} new listings, {count_linked} existing needing links. Created {count_created_cats} categories.")

    # Insert New Listings
    if listings_to_insert:
        print("Inserting new listings...")
        # Remove _temp_cat_id before insert
        clean_listings = [{k:v for k,v in l.items() if k != '_temp_cat_id'} for l in listings_to_insert]
        
        # We need the IDs. PostgREST returns created rows with Prefer: return=representation.
        # But batch insert returns array. existing validation logic might fail if batch fails?
        # Let's simple loop insert if count is small? 45 is small. 
        # Actually batch is fine, we just need to re-fetch or use returned data.
        
        url = f"{SUPABASE_URL}/rest/v1/listings"
        try:
            resp = httpx.post(url, headers=HEADERS, json=clean_listings)
            if resp.status_code == 201:
                created_rows = resp.json()
                print(f"Successfully inserted {len(created_rows)} listings.")
                
                # Create links for these new rows
                # Map back: We need to know which cat_id corresponds to which new listing.
                # Since we insert in order, likely returns in order? Not guaranteed.
                # Better to map by slug since we generated it.
                
                created_map = {r['slug']: r['id'] for r in created_rows}
                
                for l in listings_to_insert:
                    lid = created_map.get(l['slug'])
                    cid = l.get('_temp_cat_id')
                    if lid and cid:
                         links_to_insert.append({
                            "listing_id": lid,
                            "category_id": cid,
                            "is_primary": True
                         })
            else:
                print(f"Error inserting listings: {resp.text}")
        except Exception as e:
             print(f"Exception inserting listings: {e}")

    # Insert Links
    if links_to_insert:
        print(f"Inserting {len(links_to_insert)} category links...")
        url_links = f"{SUPABASE_URL}/rest/v1/listing_categories"
        # Batch insert links
        batch_size = 100
        for i in range(0, len(links_to_insert), batch_size):
            batch = links_to_insert[i:i+batch_size]
            try:
                r = httpx.post(url_links, headers=HEADERS, json=batch)
                if r.status_code == 201:
                    print(f"Linked batch {i//batch_size + 1}")
                else:
                    print(f"Failed to link batch: {r.text}")
            except Exception as e:
                print(f"Error linking: {e}")

if __name__ == "__main__":
    sync_companies()
