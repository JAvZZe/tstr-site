import os
from supabase import create_client, Client
from dotenv import load_dotenv
import json

load_dotenv()

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
supabase: Client = create_client(url, key)

# Get category ID
category = supabase.table('categories').select('id').eq('slug', 'environmental-testing').execute()
category_id = category.data[0]['id'] if category.data else None

print("=" * 70)
print("TNI ENVIRONMENTAL SCRAPER - DATABASE VERIFICATION REPORT")
print("=" * 70)

# Count total listings
total = supabase.table('listings').select('id', count='exact').eq('category_id', category_id).execute()
print(f"\nTotal Environmental Testing Listings: {total.count}")

# Get sample listings with all fields
samples = supabase.table('listings').select('*').eq('category_id', category_id).limit(5).execute()

print(f"\n{'=' * 70}")
print("SAMPLE LISTINGS")
print("=" * 70)

for i, listing in enumerate(samples.data, 1):
    print(f"\n[{i}] {listing.get('business_name')}")
    print(f"    ID: {listing.get('id')}")
    print(f"    Location ID: {listing.get('location_id')}")
    print(f"    Address: {listing.get('address')}")
    print(f"    Source: {listing.get('source')}")
    print(f"    Description: {(listing.get('description') or '')[:150]}...")

# Get custom fields for this listing
    lcf = supabase.table('listing_custom_fields').select('*, custom_fields(field_name)').eq('listing_id', listing['id']).execute()
    if lcf.data:
        print(f"    Custom Fields:")
        for field in lcf.data:
            print(f"      - {field['custom_fields']['field_name']}: {field.get('field_value', 'N/A')}")

# Get custom fields count
print(f"\n{'=' * 70}")
print("CUSTOM FIELDS ANALYSIS")
print("=" * 70)

custom_fields = supabase.table('custom_fields').select('*').eq('category_id', category_id).execute()
print(f"\nTotal Custom Fields Defined: {len(custom_fields.data)}")

for field in custom_fields.data:
    print(f"  - {field['field_name']} ({field['field_type']})")

# Count custom field values  
values = supabase.table('listing_custom_fields').select('listing_id, custom_field_id, field_value').execute()
print(f"\nTotal Custom Field Values Stored: {len(values.data)}")

# Calculate custom field population rate
if total.count > 0 and len(custom_fields.data) > 0:
    max_possible = total.count * len(custom_fields.data)
    population_rate = (len(values.data) / max_possible) * 100
    print(f"Custom Field Population Rate: {population_rate:.1f}%")

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

print(f"\nRecently Created Locations:")
sorted_locs = sorted(locations.data, key=lambda x: x.get('created_at', ''), reverse=True)[:10]
for loc in sorted_locs:
    print(f"  - {loc['name']} ({loc['level']}) - Created: {loc.get('created_at', 'N/A')[:10]}")

