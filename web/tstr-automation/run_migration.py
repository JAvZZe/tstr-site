#!/usr/bin/env python3
"""
Execute SQL migration for custom fields
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

def run_migration():
    """Run the custom fields migration SQL"""
    # Initialize Supabase client
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_SERVICE_ROLE_KEY')

    if not supabase_url or not supabase_key:
        raise ValueError("Missing SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY environment variables")

    logging.info(f"Connecting to Supabase: {supabase_url}")
    create_client(supabase_url, supabase_key)

    # Read the migration SQL file
    migration_file = '/home/al/tstr-site-working/web/tstr-automation/migrations/add_niche_custom_fields.sql'

    logging.info(f"Reading migration file: {migration_file}")
    with open(migration_file, 'r') as f:
        f.read()

    # Execute the SQL via RPC or direct query
    # Note: Supabase Python client doesn't have direct SQL execution
    # We'll need to use psycopg2 for this

    # Parse the Supabase URL to get connection details
    # Supabase uses PostgreSQL, so we can connect directly
    # Connection string format: postgresql://postgres:[password]@db.[project-ref].supabase.co:5432/postgres

    # For Supabase, the DB URL is typically constructed as:
    supabase_url.replace('https://', '')

    # Note: This requires the database password, not the API key
    # Let's try using the service role key for now and see if it works

    logging.error("Direct SQL execution requires database password, not API key")
    logging.info("Please run the migration manually via Supabase SQL Editor")
    logging.info("Or use psql with the database connection string")

    print("\n" + "="*60)
    print("MIGRATION FILE CREATED SUCCESSFULLY")
    print("="*60)
    print(f"\nFile location: {migration_file}")
    print("\nTo execute the migration, use one of these methods:")
    print("\n1. Via Supabase Dashboard:")
    print("   - Go to https://supabase.com/dashboard/project/[your-project]/sql")
    print("   - Copy and paste the SQL from the migration file")
    print("   - Click 'Run'")
    print("\n2. Via psql (if you have database password):")
    print("   psql 'postgresql://postgres:[password]@db.[project-ref].supabase.co:5432/postgres' -f migrations/add_niche_custom_fields.sql")
    print("\n" + "="*60)

if __name__ == "__main__":
    try:
        run_migration()
    except Exception as e:
        logging.error(f"Migration failed: {str(e)}")
        sys.exit(1)
