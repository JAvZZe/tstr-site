#!/usr/bin/env python3
"""Verify custom fields are properly populated and displaying correctly"""

from supabase import create_client

# Direct credentials
SUPABASE_URL = "https://haimjeaetrsaauitrhfy.supabase.co"
SUPABASE_SERVICE_ROLE_KEY = "sb_secret_zRN1fTFOYnN7cEbEIfAP7A_YrEKBfI2"

supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)

# Get environmental testing category
result = supabase.from_('categories').select('id').eq('slug', 'environmental-testing').execute()
cat_id = result.data[0]['id']

# Get custom field definitions for this category
custom_field_defs = supabase.from_('custom_fields').select('id, field_name, field_type').eq('category_id', cat_id).execute()

print("=" * 70)
print("CUSTOM FIELD DEFINITIONS FOR ENVIRONMENTAL TESTING")
print("=" * 70)
print(f"Total custom fields defined: {len(custom_field_defs.data)}\n")

field_map = {}
for field in custom_field_defs.data:
    field_map[field['id']] = field
    print(f"- {field['field_name']}")
    print(f"  Type: {field['field_type']}")
    print(f"  ID: {field['id'][:8]}...\n")

# Get listings with their custom field values
listings = supabase.from_('listings').select('id, business_name').eq('category_id', cat_id).limit(3).execute()

print("=" * 70)
print("SAMPLE LISTINGS WITH CUSTOM FIELDS")
print("=" * 70)

for listing in listings.data:
    print(f"\n{listing['business_name']}")
    print("-" * 60)

    # Get custom field values for this listing
    values = supabase.from_('listing_custom_fields').select('custom_field_id, value').eq('listing_id', listing['id']).execute()

    print(f"Custom field values: {len(values.data)}")

    for val in values.data:
        field_def = field_map.get(val['custom_field_id'])
        if field_def:
            field_name = field_def['field_name']
            field_value = val['value']

            # Format value based on type
            if isinstance(field_value, list):
                field_value = ', '.join(field_value)
            elif isinstance(field_value, bool):
                field_value = '✓ Yes' if field_value else '✗ No'

            print(f"  • {field_name}: {field_value}")

print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)

# Get total custom field values
all_values = supabase.from_('listing_custom_fields').select('listing_id').execute()
print(f"Total custom field values in database: {len(all_values.data)}")

# Count by listing
values_by_listing = {}
for val in all_values.data:
    listing_id = val['listing_id']
    values_by_listing[listing_id] = values_by_listing.get(listing_id, 0) + 1

print(f"Average custom fields per listing: {len(all_values.data) / len(values_by_listing):.1f}")
print(f"Min fields per listing: {min(values_by_listing.values())}")
print(f"Max fields per listing: {max(values_by_listing.values())}")
