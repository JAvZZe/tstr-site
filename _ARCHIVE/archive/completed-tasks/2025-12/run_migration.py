#!/usr/bin/env python3
"""
Execute source tracking migration
"""

from supabase import create_client

# Load environment
from dotenv import load_dotenv

load_dotenv(
    "/media/al/AI_SSD/AI_PROJECTS_SPACE/ACTIVE_PROJECTS/TSTR-site/tstr-site-working/web/tstr-frontend/.env"
)

supabase_url = "https://haimjeaetrsaauitrhfy.supabase.co"
supabase_key = "sb_publishable_EFSlg4kPRIvAYExPmyUJyA_7_BiJnHO"

supabase = create_client(supabase_url, supabase_key)

# Read migration SQL
migration_file = "/media/al/AI_SSD/AI_PROJECTS_SPACE/ACTIVE_PROJECTS/TSTR-site/tstr-site-working/supabase/migrations/20251202000001_add_source_tracking_to_listings.sql"

with open(migration_file, "r") as f:
    sql = f.read()

print("Executing migration...")
print(sql)

try:
    # Execute the SQL using RPC
    result = supabase.rpc("exec_sql", {"sql": sql}).execute()
    print("Migration executed successfully!")
    print(result)
except Exception as e:
    print(f"Migration failed: {e}")
    # Try alternative method
    try:
        result = supabase.table("listings").select("id").limit(1).execute()
        print(
            "Database connection works, but RPC failed. Please execute manually in Supabase dashboard."
        )
    except Exception as e2:
        print(f"Database connection failed: {e2}")
