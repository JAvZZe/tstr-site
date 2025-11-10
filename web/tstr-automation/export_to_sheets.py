#!/usr/bin/env python3
"""
Export TSTR.site listings to Google Sheets or CSV
Supports both Google Sheets API and local CSV export
"""

import csv
import sys
from datetime import datetime
from supabase import create_client

# Credentials
SUPABASE_URL = "https://haimjeaetrsaauitrhfy.supabase.co"
SUPABASE_SERVICE_ROLE_KEY = "sb_secret_zRN1fTFOYnN7cEbEIfAP7A_YrEKBfI2"

def export_to_csv(category_slug=None, output_file=None):
    """
    Export listings to CSV file

    Args:
        category_slug: Filter by category (e.g., 'environmental-testing', 'materials-testing')
        output_file: Output CSV filename (default: listings_YYYYMMDD.csv)
    """
    supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)

    # Get category if specified
    category_id = None
    if category_slug:
        result = supabase.from_('categories').select('id, name').eq('slug', category_slug).execute()
        if result.data:
            category_id = result.data[0]['id']
            category_name = result.data[0]['name']
            print(f"Filtering by category: {category_name}")
        else:
            print(f"Category '{category_slug}' not found")
            return

    # Query listings
    query = supabase.from_('listings').select('''
        id,
        business_name,
        slug,
        description,
        address,
        phone,
        email,
        website,
        status,
        created_at
    ''')

    if category_id:
        query = query.eq('category_id', category_id)

    listings = query.execute()

    if not listings.data:
        print("No listings found")
        return

    print(f"Found {len(listings.data)} listings")

    # Get custom fields for all listings
    listing_ids = [l['id'] for l in listings.data]
    custom_fields_query = supabase.from_('listing_custom_fields').select('''
        listing_id,
        custom_field_id,
        value
    ''').in_('listing_id', listing_ids).execute()

    # Get custom field definitions
    custom_field_defs_query = supabase.from_('custom_fields').select('''
        id,
        field_name,
        field_type
    ''')

    if category_id:
        custom_field_defs_query = custom_field_defs_query.eq('category_id', category_id)

    custom_field_defs = custom_field_defs_query.execute()

    # Build custom field map
    field_map = {f['id']: f['field_name'] for f in custom_field_defs.data}

    # Build custom fields by listing
    custom_by_listing = {}
    for cf in custom_fields_query.data:
        listing_id = cf['listing_id']
        field_name = field_map.get(cf['custom_field_id'], 'unknown')

        if listing_id not in custom_by_listing:
            custom_by_listing[listing_id] = {}

        # Format value
        value = cf['value']
        if isinstance(value, list):
            value = ', '.join(str(v) for v in value)
        elif isinstance(value, bool):
            value = 'Yes' if value else 'No'
        else:
            value = str(value)

        custom_by_listing[listing_id][field_name] = value

    # Determine all custom field columns
    all_custom_fields = set()
    for fields in custom_by_listing.values():
        all_custom_fields.update(fields.keys())

    all_custom_fields = sorted(all_custom_fields)

    # Generate output filename
    if not output_file:
        timestamp = datetime.now().strftime('%Y%m%d')
        prefix = category_slug.replace('-', '_') if category_slug else 'all_listings'
        output_file = f"{prefix}_{timestamp}.csv"

    # Write CSV
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        # Define columns
        base_columns = [
            'Business Name',
            'Slug',
            'Description',
            'Address',
            'Phone',
            'Email',
            'Website',
            'Status',
            'Created At'
        ]

        custom_columns = [f.replace('_', ' ').title() for f in all_custom_fields]

        writer = csv.DictWriter(f, fieldnames=base_columns + custom_columns)
        writer.writeheader()

        for listing in listings.data:
            row = {
                'Business Name': listing.get('business_name', ''),
                'Slug': listing.get('slug', ''),
                'Description': listing.get('description', ''),
                'Address': listing.get('address', ''),
                'Phone': listing.get('phone', ''),
                'Email': listing.get('email', ''),
                'Website': listing.get('website', ''),
                'Status': listing.get('status', ''),
                'Created At': listing.get('created_at', '')[:10] if listing.get('created_at') else ''
            }

            # Add custom fields
            custom_fields = custom_by_listing.get(listing['id'], {})
            for field_name in all_custom_fields:
                col_name = field_name.replace('_', ' ').title()
                row[col_name] = custom_fields.get(field_name, '')

            writer.writerow(row)

    print(f"✓ Exported to {output_file}")
    print(f"  - {len(listings.data)} listings")
    print(f"  - {len(all_custom_fields)} custom fields")
    print(f"  - Base columns: {len(base_columns)}")
    print(f"  - Total columns: {len(base_columns) + len(all_custom_fields)}")


if __name__ == '__main__':
    category = None
    output = None

    if len(sys.argv) > 1:
        category = sys.argv[1]
    if len(sys.argv) > 2:
        output = sys.argv[2]

    print("=" * 70)
    print("TSTR.site Listings Export to CSV/Spreadsheet")
    print("=" * 70)

    export_to_csv(category_slug=category, output_file=output)

    print("\n" + "=" * 70)
    print("Export complete!")
    print("=" * 70)
    print("\nTo import to Google Sheets:")
    print("1. Open Google Sheets")
    print("2. File → Import → Upload")
    print("3. Select the CSV file")
    print("4. Choose 'Replace spreadsheet' or 'Insert new sheet'")
    print("\nOr use Google Sheets API (requires setup):")
    print("  pip install gspread oauth2client")
