#!/usr/bin/env python3
"""
Fix Intertek URL using Supabase REST API
"""

import json
import urllib.request
import urllib.parse


def fix_intertek_url():
    """Fix Intertek URL using Supabase REST API"""

    print("=" * 70)
    print("FIXING INTERTEK URL VIA SUPABASE REST API")
    print("=" * 70)

    # Supabase configuration
    supabase_url = "https://haimjeaetrsaauitrhfy.supabase.co"
    supabase_key = (
        "sb_secret_zRN1fTFOYnN7cEbEIfAP7A_YrEKBfI2"  # Service role key for updates
    )

    headers = {
        "apikey": supabase_key,
        "Authorization": f"Bearer {supabase_key}",
        "Content-Type": "application/json",
        "Prefer": "return=representation",
    }

    try:
        # First, find Intertek entries
        print("Searching for Intertek entries...")
        search_url = f"{supabase_url}/rest/v1/pending_research?business_name=ilike.*intertek*&select=id,business_name,website,validation_error,created_at"

        req = urllib.request.Request(search_url, headers=headers, method="GET")
        with urllib.request.urlopen(req) as response:
            search_results = json.loads(response.read().decode())

        if not search_results:
            print("❌ No Intertek entries found in pending_research table")
            return False

        print(f"Found {len(search_results)} Intertek entries:")
        for entry in search_results:
            print(f"  ID: {entry['id']}")
            print(f"  Business: {entry['business_name']}")
            print(f"  Current URL: {entry['website']}")
            print(f"  Error: {entry['validation_error']}")
            print("-" * 50)

        # Update each entry
        updated_count = 0
        for entry in search_results:
            if entry["website"] != "https://www.intertek.com/":
                update_url = (
                    f"{supabase_url}/rest/v1/pending_research?id=eq.{entry['id']}"
                )

                update_data = {"website": "https://www.intertek.com/"}

                req = urllib.request.Request(
                    update_url,
                    data=json.dumps(update_data).encode(),
                    headers=headers,
                    method="PATCH",
                )

                with urllib.request.urlopen(req) as response:
                    json.loads(response.read().decode())
                    print(f"✅ Updated ID {entry['id']} to https://www.intertek.com/")
                    updated_count += 1

        print(f"\n✅ Successfully updated {updated_count} Intertek entries!")

        # Verify the updates
        print("\nVerifying updates...")
        req = urllib.request.Request(search_url, headers=headers, method="GET")
        with urllib.request.urlopen(req) as response:
            final_results = json.loads(response.read().decode())

        print("Final state:")
        for entry in final_results:
            print(f"  {entry['business_name']}: {entry['website']}")

        return True

    except Exception as e:
        print(f"❌ Error: {e}")
        return False


if __name__ == "__main__":
    success = fix_intertek_url()
    if success:
        print("\n🎉 Intertek URL fix completed successfully!")
    else:
        print("\n❌ Failed to fix Intertek URL")
