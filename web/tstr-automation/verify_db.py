import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
supabase: Client = create_client(url, key)

# Get category ID
category = supabase.table('categories').select('id').eq('slug', 'environmental-testing').execute()
category_id = category.data[0]['id'] if category.data else None

print("=" * 70)
print("DATABASE VERIFICATION REPORT")
print("=" * 70)

# Count total listings
total = supabase.table('listings').select('id', count='exact').eq('category_id', category_id).execute()
print(f"\nTotal Environmental Testing Listings: {total.count}")

# Count listings by source
tni_count = supabase.table('listings').select('id', count='exact').eq('category_id', category_id).eq('source_name', 'TNI LAMS (NELAP)').execute()
print(f"TNI LAMS Source Listings: {tni_count.count}")

# Get sample listings with all fields
samples = supabase.table('listings').select('*').eq('category_id', category_id).eq('source_name', 'TNI LAMS (NELAP)').limit(5).execute()

print(f"\n{'=' * 70}")
print("SAMPLE LISTINGS (First 5 from TNI LAMS)")
print("=" * 70)

for i, listing in enumerate(samples.data, 1):
    print(f"\n[{i}] {listing.get('business_name')}")
    print(f"    ID: {listing.get('id')}")
    print(f"    Location ID: {listing.get('location_id')}")
    print(f"    Address: {listing.get('address')}")
    print(f"    Phone: {listing.get('phone', 'N/A')}")
    print(f"    Email: {listing.get('email', 'N/A')}")
    print(f"    Website: {listing.get('website', 'N/A')}")
    print(f"    Description: {listing.get('description', '')[:100]}...")

# Get custom fields count
print(f"\n{'=' * 70}")
print("CUSTOM FIELDS ANALYSIS")
print("=" * 70)

custom_fields = supabase.table('custom_fields').select('*').eq('category_id', category_id).execute()
print(f"\nTotal Custom Fields Defined: {len(custom_fields.data)}")

for field in custom_fields.data:
    print(f"  - {field['field_name']} ({field['field_type']})")

# Count custom field values
values_count = supabase.table('listing_custom_fields').select('id', count='exact').execute()
print(f"\nTotal Custom Field Values Stored: {values_count.count}")

# Get location statistics
print(f"\n{'=' * 70}")
print("LOCATION DISTRIBUTION")
print("=" * 70)

locations = supabase.table('locations').select('*').execute()
print(f"\nTotal Locations: {len(locations.data)}")

regions = [loc for loc in locations.data if loc['level'] == 'region']
cities = [loc for loc in locations.data if loc['level'] == 'city']

print(f"  - Regions (States): {len(regions)}")
print(f"  - Cities: {len(cities)}")

