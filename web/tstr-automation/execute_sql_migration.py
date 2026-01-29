#!/usr/bin/env python3
"""
Execute SQL migration using Supabase postgrest RPC
"""

import sys
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def execute_migration():
    """Execute the custom fields migration SQL"""

    migration_file = "/media/al/AI_SSD/AI_PROJECTS_SPACE/ACTIVE_PROJECTS/TSTR-site/tstr-site-working/supabase/migrations/20251202000001_add_source_tracking_to_listings.sql"

    # Read the SQL
    logging.info(f"Reading migration file: {migration_file}")
    with open(migration_file, "r") as f:
        sql_content = f.read()

    # Split the SQL into individual DO blocks
    # Each block is a separate transaction
    blocks = []
    current_block = []
    in_do_block = False

    for line in sql_content.split("\n"):
        if line.strip().startswith("DO $$"):
            in_do_block = True
            current_block = [line]
        elif line.strip().startswith("END $$;") and in_do_block:
            current_block.append(line)
            blocks.append("\n".join(current_block))
            current_block = []
            in_do_block = False
        elif in_do_block or (line.strip() and not line.strip().startswith("--")):
            current_block.append(line)

    if current_block:
        blocks.append("\n".join(current_block))

    logging.info(f"Split SQL into {len(blocks)} executable blocks")

    # For now, just provide instructions since direct SQL execution
    # via Supabase API requires database credentials
    print("\n" + "=" * 80)
    print("SQL MIGRATION FILE CREATED SUCCESSFULLY")
    print("=" * 80)
    print(f"\nFile location: {migration_file}")
    print(f"\nTotal SQL blocks to execute: {len(blocks)}")
    print("\n" + "-" * 80)
    print("TO EXECUTE THE MIGRATION:")
    print("-" * 80)
    print("\nOption 1: Supabase Dashboard (RECOMMENDED)")
    print("-" * 40)
    print("1. Go to: https://supabase.com/dashboard/project/haimjeaetrsaauitrhfy/sql")
    print(f"2. Open the file: {migration_file}")
    print("3. Copy the entire SQL content")
    print("4. Paste into the SQL Editor")
    print("5. Click 'Run'")
    print("\nOption 2: Using psql command line")
    print("-" * 40)
    print("1. Get your database password from Supabase Dashboard > Settings > Database")
    print("2. Run:")
    print(
        "   psql 'postgresql://postgres.[PASSWORD]@db.haimjeaetrsaauitrhfy.supabase.co:5432/postgres' \\"
    )
    print(f"        -f {migration_file}")
    print("\n" + "=" * 80)
    print("\nAfter running, execute verify_custom_fields.sql to confirm success")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    try:
        execute_migration()
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        sys.exit(1)
