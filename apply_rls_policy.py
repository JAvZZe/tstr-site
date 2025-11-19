#!/usr/bin/env python3
"""
Apply RLS policy for public form submissions
Directly executes SQL against Supabase database
"""

import os
import json
import base64
from pathlib import Path

# Supabase credentials
SUPABASE_URL = "https://haimjeaetrsaauitrhfy.supabase.co"
SERVICE_ROLE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhhaW1qZWFlbHJzYWF1aXRyaGZ5Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTcyNDQ5NjU5MiwiZXhwIjoxODgyMjYzMzkyLCJlbWFpbCI6IiIsInBob25lIjoiIiwiYXBwX21ldGFkYXRhIjp7InByb3ZpZGVyIjoic3VwYWJhc2UiLCJwcm92aWRlcnMiOlsic3VwYWJhc2UiXX0sInVzZXJfbWV0YWRhdGEiOnt9LCJzdWIiOiI4OWRlYzZiZC1iYjI0LTQ4ZjItYTc5Yi1lM2UxZGY5MjQ4NWMiLCJhdWQiOiJhdXRoZW50aWNhdGVkIiwiZXZlbnRfaWQiOiI2NzM1MWQyZi0zNTA1LTQ1NWMtOTY4Ni1lOGJiMWMyZDllMGUiLCJjaGFsbGVuZ2UiOiJlMmZkM2Q3MGEyNjc4MGE5Iiwic2Vzc2lvbl9pZCI6ImMwY2YwYTU2LWRkMzYtNGQ5NS04YzE2LTNkYzk1ZTQyM2YyZiIsImFhbCI6ImFhbDEiLCJhbXIiOlsiY2hlY2tpbmdfc2Vzc2lvbiIsInBhc3N3b3JkIl0sImF1dGhlbnRpY2F0aW9uX21ldGhvZCI6InBhc3N3b3JkIiwic2Vzc2lvbl9pZCI6ImMwY2YwYTU2LWRkMzYtNGQ5NS04YzE2LTNkYzk1ZTQyM2YyZiIsImlzX2Fub255bW91cyI6ZmFsc2V9.GQWD5xkRKvGiCsJqbfvyDAQHjy2t4ycXPRK0kZxPmqI"

# SQL to apply
RLS_POLICY_SQL = """
-- Drop any existing policies that might conflict
DROP POLICY IF EXISTS "Allow public submissions to pending listings" ON public.listings;
DROP POLICY IF EXISTS "Allow authenticated submissions to pending listings" ON public.listings;

-- Create policy for anonymous users to submit listings
CREATE POLICY "Allow public submissions to pending listings"
  ON public.listings
  FOR INSERT
  TO anon
  WITH CHECK (
    status = 'pending'
    AND verified = false
    AND claimed = false
  );

-- Create policy for authenticated users to submit listings
CREATE POLICY "Allow authenticated submissions to pending listings"
  ON public.listings
  FOR INSERT
  TO authenticated
  WITH CHECK (
    status = 'pending'
    AND verified = false
    AND claimed = false
  );

-- Ensure RLS is enabled on listings table
ALTER TABLE public.listings ENABLE ROW LEVEL SECURITY;

-- Ensure status column has correct default
ALTER TABLE public.listings
  ALTER COLUMN status SET DEFAULT 'pending';
"""

VERIFY_SQL = """
SELECT policyname, roles, cmd FROM pg_policies
WHERE tablename = 'listings' AND cmd = 'INSERT'
ORDER BY policyname;
"""


def apply_rls_policy():
    """Apply RLS policy using Supabase client library or direct SQL"""

    print("=" * 60)
    print("TSTR.site - Apply RLS Policy for Public Submissions")
    print("=" * 60)

    # Try using supabase-py client
    try:
        from supabase import create_client

        print("\n1. Initializing Supabase client...")
        supabase = create_client(SUPABASE_URL, SERVICE_ROLE_KEY)

        print("2. Executing RLS policy SQL...")
        # Use rpc call to execute raw SQL
        # This requires a SQL function in Supabase - check if it exists
        try:
            result = supabase.rpc('exec_sql', {'sql': RLS_POLICY_SQL}).execute()
            print("   ✓ RLS policy applied successfully")
        except Exception as e:
            print(f"   ✗ RPC exec_sql not available: {e}")
            print("\n   ALTERNATIVE: Use Supabase dashboard:")
            print("   - Go to SQL Editor")
            print("   - Paste the SQL from RLS_POLICY_SQL")
            print("   - Execute")
            return False

        print("\n3. Verifying policy creation...")
        verify_result = supabase.rpc('exec_sql', {'sql': VERIFY_SQL}).execute()
        print("   ✓ Policies verified:")
        print(f"   {verify_result}")

        print("\n" + "=" * 60)
        print("SUCCESS: RLS policy has been applied!")
        print("=" * 60)
        return True

    except ImportError:
        print("\n✗ supabase-py library not installed")
        print("\nFALLBACK: Manual application required")
        print("\nTo apply the RLS policy manually:")
        print("\n1. Option A - Using Supabase CLI:")
        print("   cd /path/to/project")
        print("   supabase db push --linked")
        print("\n2. Option B - Using Supabase Dashboard:")
        print("   - Go to https://app.supabase.io/")
        print("   - Select your project")
        print("   - Click 'SQL Editor'")
        print("   - Paste this SQL:")
        print("\n" + RLS_POLICY_SQL)
        print("\n   Then execute the verification query:")
        print("\n" + VERIFY_SQL)
        return False


if __name__ == "__main__":
    success = apply_rls_policy()
    exit(0 if success else 1)
