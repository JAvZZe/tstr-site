#!/usr/bin/env python3
"""
Check current RLS policies on the listings table
"""

from supabase import create_client, Client

SUPABASE_URL = "https://haimjeaetrsaauitrhfy.supabase.co"
SUPABASE_KEY = "sb_secret_zRN1fTFOYnN7cEbEIfAP7A_YrEKBfI2"


def check_rls_policies():
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

    print("🔍 Checking RLS policies on listings table...")

    try:
        # Check if RLS is enabled
        supabase.table("listings").select("*").limit(1).execute()
        print("✅ RLS query successful - data accessible")

        # Try to check policies (this might not work with service role)
        print("\n📋 Attempting to list RLS policies...")

        # Try anonymous insert test
        print("\n🧪 Testing anonymous insert capability...")
        test_data = {
            "business_name": "RLS TEST LISTING - DELETE ME",
            "slug": "rls-test-listing-delete-me",
            "category_id": "3f99a311-9bd4-4366-b9bc-49860ad931d5",  # Materials Testers
            "location_id": "4a1482aa-6387-4f44-84ea-bbe11eb2f4f1",  # United States
            "website": "https://rlstest.com",
            "email": "test@rls.com",
            "address": "Test City, United States",
            "status": "pending",
            "verified": False,
            "claimed": False,
        }

        try:
            insert_result = supabase.table("listings").insert(test_data).execute()
            print("✅ Anonymous insert SUCCESSFUL")
            print(
                f"Inserted record ID: {insert_result.data[0]['id'] if insert_result.data else 'Unknown'}"
            )

            # Clean up
            if insert_result.data:
                record_id = insert_result.data[0]["id"]
                supabase.table("listings").delete().eq("id", record_id).execute()
                print("🧹 Test record cleaned up")

        except Exception as e:
            print(f"❌ Anonymous insert FAILED: {e}")
            if "violates row level security policy" in str(e):
                print("🚫 BLOCKED BY RLS POLICY - Anonymous inserts not allowed")
            elif "violates foreign key constraint" in str(e):
                print("🔗 FOREIGN KEY ISSUE - Invalid category/location ID")
            else:
                print(f"❓ OTHER ERROR: {e}")

    except Exception as e:
        print(f"❌ Error checking policies: {e}")


if __name__ == "__main__":
    check_rls_policies()
