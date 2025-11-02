#!/usr/bin/env python3
"""
Run migration and verify results using Supabase client
Requires SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY environment variables
"""

import os
import sys
from supabase import create_client
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def verify_migration():
    """Verify that custom fields were added correctly"""

    # Initialize Supabase client
    supabase_url = os.getenv('SUPABASE_URL', 'https://haimjeaetrsaauitrhfy.supabase.co')
    supabase_key = os.getenv('SUPABASE_SERVICE_ROLE_KEY')

    if not supabase_key:
        logging.error("SUPABASE_SERVICE_ROLE_KEY environment variable not set")
        logging.info("Using anon key for read-only verification")
        supabase_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhhaW1qZWFldHJzYWF1aXRyaGZ5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mjg4NTA4NjEsImV4cCI6MjA0NDQyNjg2MX0.EFSlg4kPRIvAYExPmyUJyA_7_BiJnHO'

    logging.info(f"Connecting to Supabase: {supabase_url}")
    supabase = create_client(supabase_url, supabase_key)

    print("\n" + "="*80)
    print("CUSTOM FIELDS MIGRATION VERIFICATION")
    print("="*80)

    # Query 1: Count custom fields per category
    print("\n1. Custom Fields Count by Category:")
    print("-" * 80)

    try:
        categories = ['oil-gas-testing', 'pharmaceutical-testing', 'environmental-testing', 'materials-testing']

        for category_slug in categories:
            # Get category
            cat_result = supabase.from_('categories').select('id, name').eq('slug', category_slug).execute()

            if cat_result.data:
                category = cat_result.data[0]

                # Count custom fields
                cf_result = supabase.from_('custom_fields').select('*', count='exact').eq('category_id', category['id']).execute()

                count = cf_result.count if cf_result.count else 0
                print(f"  {category['name']}: {count} fields")

        print("\n  Expected: 7 fields per category")

    except Exception as e:
        logging.error(f"Error querying categories: {str(e)}")

    # Query 2: Sample field details for each category
    print("\n2. Sample Custom Fields Details:")
    print("-" * 80)

    try:
        for category_slug in categories:
            # Get category
            cat_result = supabase.from_('categories').select('id, name').eq('slug', category_slug).execute()

            if cat_result.data:
                category = cat_result.data[0]
                print(f"\n  {category['name']} ({category_slug}):")

                # Get custom fields
                cf_result = supabase.from_('custom_fields') \
                    .select('field_name, field_label, field_type, options') \
                    .eq('category_id', category['id']) \
                    .order('display_order') \
                    .execute()

                for field in cf_result.data:
                    options_str = ""
                    if field.get('options'):
                        options_str = f" → {field['options']}"
                    print(f"    • {field['field_name']} ({field['field_type']}){options_str}")

    except Exception as e:
        logging.error(f"Error querying custom fields: {str(e)}")

    # Query 3: Validate options JSON
    print("\n3. Validation Check:")
    print("-" * 80)

    try:
        issues = []

        for category_slug in categories:
            # Get category
            cat_result = supabase.from_('categories').select('id').eq('slug', category_slug).execute()

            if cat_result.data:
                category_id = cat_result.data[0]['id']

                # Get multi_select and select fields
                cf_result = supabase.from_('custom_fields') \
                    .select('field_name, field_type, options') \
                    .eq('category_id', category_id) \
                    .in_('field_type', ['multi_select', 'select']) \
                    .execute()

                for field in cf_result.data:
                    if not field.get('options'):
                        issues.append(f"{category_slug}.{field['field_name']}: Missing options")
                    elif len(field['options']) == 0:
                        issues.append(f"{category_slug}.{field['field_name']}: Empty options")

        if issues:
            print("  Issues found:")
            for issue in issues:
                print(f"    ⚠ {issue}")
        else:
            print("  ✓ All multi_select and select fields have valid options")

    except Exception as e:
        logging.error(f"Error validating options: {str(e)}")

    # Summary
    print("\n" + "="*80)
    print("VERIFICATION SUMMARY")
    print("="*80)

    try:
        # Total count
        total_result = supabase.from_('custom_fields') \
            .select('id', count='exact') \
            .execute()

        # Get all category IDs
        cat_ids_result = supabase.from_('categories') \
            .select('id') \
            .in_('slug', categories) \
            .execute()

        category_ids = [c['id'] for c in cat_ids_result.data]

        # Count for our 4 categories
        niche_result = supabase.from_('custom_fields') \
            .select('id', count='exact') \
            .in_('category_id', category_ids) \
            .execute()

        niche_count = niche_result.count if niche_result.count else 0

        print(f"\nTotal custom fields in database: {total_result.count}")
        print(f"Custom fields for 4 testing niches: {niche_count}")
        print(f"Expected for 4 niches: 28 (7 fields × 4 categories)")

        if niche_count == 28:
            print("\n✅ Migration successful! All custom fields added correctly.")
        else:
            print(f"\n⚠ Warning: Expected 28 fields but found {niche_count}")
            print("   Please review the migration and re-run if needed.")

    except Exception as e:
        logging.error(f"Error in summary: {str(e)}")

    print("\n" + "="*80)
    print("\nFor detailed verification, run the SQL queries in:")
    print(f"/home/al/tstr-site-working/web/tstr-automation/migrations/verify_custom_fields.sql")
    print("="*80 + "\n")

if __name__ == "__main__":
    try:
        verify_migration()
    except Exception as e:
        logging.error(f"Verification failed: {str(e)}")
        sys.exit(1)
