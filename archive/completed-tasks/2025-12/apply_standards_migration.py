#!/usr/bin/env python3
"""
Apply standards and capabilities migration to Supabase
Uses service role key to execute SQL directly
"""

import requests
import sys

# Supabase project details
PROJECT_REF = "haimjeaetrsaauitrhfy"
SERVICE_ROLE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhhaW1qZWFldHJzYWF1aXRyaGZ5Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTcyOTc2OTI1NywiZXhwIjoyMDQ1MzQ1MjU3fQ.dR_zMUZlxkxZ-wrApS9XkV5maCBNdm-5HB5Mj0CnFRk"

# Read migration file
with open("supabase/migrations/20251120000001_add_standards_and_capabilities.sql", "r") as f:
    migration_sql = f.read()

print("🚀 Applying standards and capabilities migration...")
print(f"📊 Migration size: {len(migration_sql)} characters")

# Use Supabase's SQL execution endpoint
url = f"https://{PROJECT_REF}.supabase.co/rest/v1/rpc/exec_sql"

# Try direct query endpoint instead
url = f"https://{PROJECT_REF}.supabase.co/rest/v1/"

headers = {
    "apikey": SERVICE_ROLE_KEY,
    "Authorization": f"Bearer {SERVICE_ROLE_KEY}",
    "Content-Type": "application/json"
}

# Alternative: Use Supabase Management API
# This requires the service role key and uses the database endpoint

print("\n⚠️  Note: Supabase REST API doesn't support direct DDL execution.")
print("📋 Migration file ready at: supabase/migrations/20251120000001_add_standards_and_capabilities.sql")
print("\n✅ Recommended approach:")
print("   1. Go to: https://supabase.com/dashboard/project/haimjeaetrsaauitrhfy/sql")
print("   2. Copy contents from migration file")
print("   3. Paste into SQL Editor")
print("   4. Click 'Run' or press Ctrl+Enter")
print("\n📄 Migration creates:")
print("   - standards table (testing standards/certifications)")
print("   - listing_capabilities table (links listings to standards)")
print("   - Indexes for search performance")
print("   - RLS policies for security")
print("   - search_by_standard() helper function")

sys.exit(0)
