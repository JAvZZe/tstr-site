#!/usr/bin/env python3
"""
Fix Intertek URL in pending_research table
"""

import os
import sys
from supabase import create_client, Client

# Add the frontend directory to path to import supabase config
sys.path.append(os.path.join(os.path.dirname(__file__), "web", "tstr-frontend"))


def fix_intertek_url():
    """Update the incorrect Intertek URL to the correct one"""

    # Use environment variables or fallback
    supabase_url = os.getenv(
        "PUBLIC_SUPABASE_URL", "https://haimjeaetrsaauitrhfy.supabase.co"
    )
    supabase_key = os.getenv(
        "SUPABASE_SERVICE_ROLE_KEY", "sb_secret_zRN1fTFOYnN7cEbEIfAP7A_YrEKBfI2"
    )

    supabase: Client = create_client(supabase_url, supabase_key)

    try:
        # Find entries with Intertek business name
        result = (
            supabase.table("pending_research")
            .select("*")
            .ilike("business_name", "%intertek%")
            .execute()
        )

        if result.data:
            print(f"Found {len(result.data)} Intertek entries:")
            for entry in result.data:
                print(
                    f"  ID: {entry['id']}, Business: {entry['business_name']}, URL: {entry['website']}"
                )

                # Update to correct URL
                update_result = (
                    supabase.table("pending_research")
                    .update({"website": "https://www.intertek.com/"})
                    .eq("id", entry["id"])
                    .execute()
                )

                print(f"  Updated ID {entry['id']} to https://www.intertek.com/")
        else:
            print("No Intertek entries found in pending_research table")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    fix_intertek_url()
