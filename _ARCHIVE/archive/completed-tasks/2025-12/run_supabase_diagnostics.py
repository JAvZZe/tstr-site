#!/usr/bin/env python3
"""
Supabase Security & Performance Diagnostics
Run this after updating the service role key
"""

import os
import sys

from supabase import Client, create_client


def main():
    # Load environment variables
    supabase_url = os.getenv('PUBLIC_SUPABASE_URL')
    service_key = os.getenv('SUPABASE_SERVICE_ROLE_KEY')
    
    if not supabase_url or not service_key:
        print("❌ Missing environment variables")
        print("Set PUBLIC_SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY")
        sys.exit(1)
    
    try:
        # Create Supabase client with service role
        supabase: Client = create_client(supabase_url, service_key)
        
        print("🔍 Running Supabase Diagnostics...")
        print("=" * 50)
        
        # Test basic connectivity
        result = supabase.table('listings').select('count', count='exact').limit(1).execute()
        print(f"✅ Database connection: {result.count} listings found")
        
        # Check RLS policies (this would require direct SQL access)
        print("\n📋 Next Steps:")
        print("1. Run supabase_diagnostics.sql in Supabase SQL Editor")
        print("2. Check the Issues tab in Supabase Dashboard")
        print("3. Review the output for security and performance problems")
        
        # Test some basic queries that might be slow
        print("\n⏱️  Testing query performance...")
        
        # Test analytics functions
        try:
            result = supabase.rpc('get_top_clicked_listings', {'limit_count': 5}).execute()
            print(f"✅ get_top_clicked_listings: {len(result.data)} results")
        except Exception as e:
            print(f"❌ get_top_clicked_listings failed: {e}")
        
        try:
            result = supabase.rpc('get_click_stats', {'days_back': 7}).execute()
            print(f"✅ get_click_stats: {len(result.data)} results")
        except Exception as e:
            print(f"❌ get_click_stats failed: {e}")
        
        # Test listing queries with joins
        try:
            result = supabase.table('listings').select('*, category:category_id(name), location:location_id(name)').limit(5).execute()
            print(f"✅ Complex listing query: {len(result.data)} results")
        except Exception as e:
            print(f"❌ Complex listing query failed: {e}")
        
        print("\n✅ Diagnostics complete!")
        print("📊 Check Supabase dashboard for detailed issue breakdown")
        
    except Exception as e:
        print(f"❌ Diagnostic failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
