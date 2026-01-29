#!/usr/bin/env python3
"""Check existing environmental testing listings and custom fields"""

from supabase import create_client

# Direct credentials (from .env)
SUPABASE_URL = "https://haimjeaetrsaauitrhfy.supabase.co"
SUPABASE_SERVICE_ROLE_KEY = "sb_secret_zRN1fTFOYnN7cEbEIfAP7A_YrEKBfI2"

supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)

# Get environmental testing category
result = supabase.from_('categories').select('id').eq('slug', 'environmental-testing').execute()
if result.data:
    cat_id = result.data[0]['id']
    print(f'Category ID: {cat_id}')

    # Get existing listings
    listings = supabase.from_('listings').select('id, business_name, description').eq('category_id', cat_id).execute()
    print(f'\nTotal listings: {len(listings.data)}')

    if listings.data:
        print('\nFirst 3 listings:')
        for listing in listings.data[:3]:
            print(f'  - {listing["business_name"][:60]}')
            print(f'    ID: {listing["id"][:8]}...')
            desc = listing.get("description", "")[:100]
            print(f'    Desc: {desc}...\n')

        # Check custom fields
        listing_ids = [listing['id'] for listing in listings.data]
        custom_fields = supabase.from_('listing_custom_fields').select('*').in_('listing_id', listing_ids).execute()
        print(f'Custom field values in DB: {len(custom_fields.data)}')

        if custom_fields.data:
            print('\nSample custom fields:')
            for cf in custom_fields.data[:3]:
                print(f'  - Listing: {cf["listing_id"][:8]}...')
                print(f'    Field: {cf["custom_field_id"][:8]}...')
                print(f'    Value: {cf["value"]}')
else:
    print("Environmental testing category not found!")

