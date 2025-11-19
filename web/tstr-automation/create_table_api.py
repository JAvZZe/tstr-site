"""
Create table using Supabase Management API
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

def create_via_api():
    """Use Supabase Management API to execute SQL"""
    
    # Get project info
    supabase_url = os.getenv("SUPABASE_URL")
    project_ref = supabase_url.replace('https://', '').replace('.supabase.co', '')
    
    # Management API requires an access token
    # For now, let's use a workaround: create via REST API POST
    
    print("="*70)
    print("CREATING TABLE VIA MANAGEMENT API")
    print("="*70)
    
    # Alternative: Use supabase CLI or create manually
    # Since the Supabase Management API requires authentication that we don't have,
    # let's just create the SQL file and provide instructions
    
    sql_file = "pending_research_table.sql"
    
    sql = """-- Run this in Supabase SQL Editor
-- URL: https://supabase.com/dashboard/project/{}/sql

CREATE TABLE IF NOT EXISTS pending_research (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    business_name TEXT NOT NULL,
    website TEXT,
    validation_error TEXT,
    original_id UUID,
    category TEXT,
    location_id UUID,
    address TEXT,
    phone TEXT,
    email TEXT,
    description TEXT,
    status TEXT DEFAULT 'pending_research',
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    researched_at TIMESTAMP WITH TIME ZONE,
    researched_by TEXT
);

CREATE INDEX IF NOT EXISTS idx_pending_research_business_name ON pending_research(business_name);
CREATE INDEX IF NOT EXISTS idx_pending_research_status ON pending_research(status);
CREATE INDEX IF NOT EXISTS idx_pending_research_created_at ON pending_research(created_at);

-- Enable Row Level Security
ALTER TABLE pending_research ENABLE ROW LEVEL SECURITY;

-- Create policies
DROP POLICY IF EXISTS "Enable all for authenticated users" ON pending_research;
CREATE POLICY "Enable all for authenticated users" ON pending_research
    FOR ALL USING (true);
""".format(project_ref)
    
    with open(sql_file, 'w') as f:
        f.write(sql)
    
    print(f"✅ Created SQL file: {sql_file}")
    print("\n📋 COPY AND PASTE THIS SQL INTO SUPABASE:")
    print("="*70)
    print(sql)
    print("="*70)
    
    print(f"\n🌐 SQL Editor URL:")
    print(f"https://supabase.com/dashboard/project/{project_ref}/sql")
    
    print("\n🔧 Or use Supabase CLI:")
    print(f"supabase db push --db-url postgresql://postgres:[YOUR_PASSWORD]@db.{project_ref}.supabase.co:5432/postgres --file {sql_file}")
    
    return True

if __name__ == "__main__":
    create_via_api()
    
    print("\n" + "="*70)
    print("After running the SQL, you can proceed with:")
    print("python cleanup_invalid_urls.py 2")
    print("="*70)
