from supabase import create_client, Client

# Initialize Supabase client
SUPABASE_URL = "https://haimjeaetrsaauitrhfy.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhhaW1qZWFldHJzYWF1aXRyaGZ5Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTcyOTQ0ODQzNywiZXhwIjoyMDQ1MDI0NDM3fQ.sb_secret_zRN1fTFOYnN7cEbEIfAP7A_YrEKBfI2"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Query biotech/pharma listings
response = supabase.table('listings').select(
    'id, business_name, city, state, country, website, status, verified, categories(name)'
).execute()

# Filter for biotech/pharma
biotech_listings = []
for listing in response.data:
    category_name = listing.get('categories', {}).get('name', '') if listing.get('categories') else ''
    if 'biotech' in category_name.lower() or 'pharma' in category_name.lower():
        biotech_listings.append(listing)

print(f"\n=== BIOTECH/PHARMA LISTINGS ({len(biotech_listings)} total) ===\n")

for listing in sorted(biotech_listings, key=lambda x: x['business_name']):
    print(f"ID: {listing['id']}")
    print(f"Name: {listing['business_name']}")
    location_parts = [listing.get('city'), listing.get('state'), listing.get('country')]
    location = ', '.join(filter(None, location_parts))
    print(f"Location: {location}")
    print(f"Website: {listing.get('website', 'N/A')}")
    category_name = listing.get('categories', {}).get('name', 'N/A') if listing.get('categories') else 'N/A'
    print(f"Category: {category_name}")
    print(f"Status: {listing.get('status', 'N/A')} | Verified: {listing.get('verified', False)}")
    print("-" * 80)

# Now get their capabilities
print("\n=== QUERYING CAPABILITIES ===\n")

for listing in biotech_listings[:5]:  # Sample first 5
    cap_response = supabase.table('listing_capabilities').select(
        'standards(standard_code, standard_name, category)'
    ).eq('listing_id', listing['id']).execute()
    
    if cap_response.data:
        print(f"\n{listing['business_name']}:")
        for cap in cap_response.data:
            if cap.get('standards'):
                std = cap['standards']
                print(f"  - {std.get('standard_code', 'N/A')}: {std.get('standard_name', 'N/A')}")
    else:
        print(f"\n{listing['business_name']}: No capabilities recorded")

