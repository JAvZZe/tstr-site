#!/usr/bin/env python3
"""
Check Supabase project status and basic health
"""

import os
import requests
from supabase import create_client, Client

def main():
    supabase_url = os.getenv('PUBLIC_SUPABASE_URL', 'https://haimjeaetrsaauitrhfy.supabase.co')
    anon_key = os.getenv('PUBLIC_SUPABASE_ANON_KEY', 'sb_publishable_EFSlg4kPRIvAYExPmyUJyA_7_BiJnHO')
    
    print("🔍 Checking Supabase Status...")
    print(f"URL: {supabase_url}")
    print("Project: haimjeaetrsaauitrhfy")
    print("-" * 40)
    
    # Test basic API connectivity
    try:
        response = requests.get(f"{supabase_url}/rest/v1/listings?select=count", 
                              headers={'apikey': anon_key})
        if response.status_code == 200:
            data = response.json()
            count = data[0]['count'] if data else 0
            print(f"✅ API Connection: {count} listings")
        else:
            print(f"❌ API Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Connection failed: {e}")
    
    # Test Supabase client
    try:
        supabase: Client = create_client(supabase_url, anon_key)
        result = supabase.table('listings').select('count', count='exact').limit(1).execute()
        print(f"✅ Client Connection: {result.count} listings")
    except Exception as e:
        print(f"❌ Client connection failed: {e}")
    
    # Check if service role key is set
    service_key = os.getenv('SUPABASE_SERVICE_ROLE_KEY')
    if service_key and service_key != 'your_service_role_key_here':
        print("✅ Service role key: Configured")
    else:
        print("❌ Service role key: NOT SET (needed for diagnostics)")
    
    print("\n📋 Manual Checks Needed:")
    print("1. Visit: https://supabase.com/dashboard/project/haimjeaetrsaauitrhfy")
    print("2. Check 'Issues' tab for 61 problems (15 security + 46 performance)")
    print("3. Get service_role key from Settings → API")
    print("4. Run: ./update_service_key.sh <your_key>")
    print("5. Run: python3 run_supabase_diagnostics.py")

if __name__ == "__main__":
    main()
