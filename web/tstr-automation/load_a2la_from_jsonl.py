#!/usr/bin/env python3
"""
Load A2LA Materials Testing labs from pre-extracted JSONL data
This bypasses the scraping issues and uses already-collected data
"""

import json
import logging
import sys
import os
from supabase import create_client

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from location_parser import LocationParser

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Credentials
SUPABASE_URL = "https://haimjeaetrsaauitrhfy.supabase.co"
SUPABASE_SERVICE_ROLE_KEY = "sb_secret_zRN1fTFOYnN7cEbEIfAP7A_YrEKBfI2"

def load_a2la_labs(jsonl_file, limit=None):
    """
    Load A2LA labs from JSONL file and import to Supabase

    Args:
        jsonl_file: Path to JSONL file with extracted lab data
        limit: Max number of labs to load (for testing)
    """
    supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)
    location_parser = LocationParser(supabase)

    # Get materials-testing category
    result = supabase.from_('categories').select('id').eq('slug', 'materials-testing').execute()
    if not result.data:
        logger.error("materials-testing category not found!")
        return
    category_id = result.data[0]['id']
    logger.info(f"Category ID: {category_id}")

    # Load custom field definitions
    custom_fields_result = supabase.from_('custom_fields').select('*').eq('category_id', category_id).execute()
    custom_fields_map = {cf['field_name']: cf for cf in custom_fields_result.data}
    logger.info(f"Loaded {len(custom_fields_map)} custom field definitions")

    # Load JSONL data
    labs = []
    with open(jsonl_file, 'r') as f:
        for line in f:
            if line.strip():
                labs.append(json.loads(line))

    logger.info(f"Loaded {len(labs)} labs from {jsonl_file}")

    if limit:
        labs = labs[:limit]
        logger.info(f"Limiting to {limit} labs")

    stats = {
        'saved': 0,
        'failed': 0,
        'skipped': 0,
        'custom_fields': 0
    }

    for idx, lab in enumerate(labs, 1):
        logger.info(f"[{idx}/{len(labs)}] Processing: {lab.get('org', 'Unknown')}")

        try:
            # Build address
            address_parts = []
            if lab.get('city'):
                address_parts.append(lab['city'])
            if lab.get('state'):
                address_parts.append(lab['state'])
            if lab.get('country'):
                address_parts.append(lab['country'])

            address = ', '.join(address_parts)

            if not address:
                logger.warning("  ⚠ No address data, skipping")
                stats['skipped'] += 1
                continue

            # Parse location
            location_id = location_parser.parse_and_link(
                address=address,
                latitude=None,
                longitude=None,
                fallback_country='United States' if lab.get('country') == 'USA' else None
            )

            if not location_id:
                logger.warning(f"  ⚠ Failed to parse location: {address}")
                stats['failed'] += 1
                continue

            # Generate slug
            org_name = lab.get('org', 'Unknown Lab')
            slug = org_name.lower().replace(' ', '-').replace('/', '-')
            slug = ''.join(c for c in slug if c.isalnum() or c == '-')[:50]

            # Build description
            desc_parts = [
                "ISO/IEC 17025 accredited materials testing laboratory",
                f"(A2LA Cert: {lab.get('cert', 'N/A')})"
            ]
            if lab.get('scope'):
                desc_parts.append(f"Scope: {lab['scope']}")
            if lab.get('notes'):
                desc_parts.append(lab['notes'])

            description = '. '.join(desc_parts)

            # Check for duplicates
            dup_check = supabase.from_('listings').select('id').eq('slug', slug).eq('category_id', category_id).execute()
            if dup_check.data:
                logger.info(f"  ⚠ Duplicate slug '{slug}', skipping")
                stats['skipped'] += 1
                continue

            # Prepare listing data
            listing_data = {
                'business_name': org_name,
                'slug': slug,
                'description': description,
                'category_id': category_id,
                'location_id': location_id,
                'address': address,
                'phone': '',
                'email': '',
                'website': '',
                'status': 'active'
            }

            # Insert listing
            insert_result = supabase.from_('listings').insert(listing_data).execute()

            if not insert_result.data:
                logger.error("  ✗ Failed to insert listing")
                stats['failed'] += 1
                continue

            listing_id = insert_result.data[0]['id']
            logger.info(f"  ✓ Saved: {org_name} (ID: {listing_id[:8]}...)")
            stats['saved'] += 1

            # TODO: Extract and save custom fields based on scope/notes
            # For now, we'll skip custom fields since the JSONL doesn't have detailed data

        except Exception as e:
            logger.error(f"  ✗ Error processing {lab.get('org', 'Unknown')}: {e}")
            stats['failed'] += 1

    # Print summary
    print("\n" + "=" * 70)
    print("IMPORT COMPLETE")
    print("=" * 70)
    print(f"Total labs processed: {len(labs)}")
    print(f"Successfully saved: {stats['saved']}")
    print(f"Failed: {stats['failed']}")
    print(f"Skipped (duplicates/no address): {stats['skipped']}")
    print(f"Custom fields populated: {stats['custom_fields']}")
    print("=" * 70)


if __name__ == '__main__':
    jsonl_file = 'scrapers/a2la/a2la_claude_complete.jsonl'
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else None

    load_a2la_labs(jsonl_file, limit=limit)
