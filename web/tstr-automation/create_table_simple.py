"""
Simple table creation using Supabase client
"""

import os
from dotenv import load_dotenv

load_dotenv()

def create_table_simple():
    """Create table by trying to insert a dummy record"""
    from supabase import create_client
    
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    
    client = create_client(supabase_url, supabase_key)
    
    print("="*70)
    print("SIMPLE TABLE CREATION")
    print("="*70)
    
    # Since we can't execute DDL via the Python client directly,
    # let's open the SQL editor in browser for you
    print("\n📝 Opening Supabase SQL Editor...")
    print("Please paste this SQL and click RUN:\n")
    
    sql = """CREATE TABLE IF NOT EXISTS pending_research (
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
CREATE INDEX IF NOT EXISTS idx_pending_research_status ON pending_research(status);"""
    
    print(sql)
    print("\n" + "="*70)
    
    # Open URL in browser
    project_ref = supabase_url.replace('https://', '').replace('.supabase.co', '')
    sql_editor_url = f"https://supabase.com/dashboard/project/{project_ref}/sql/new"
    
    import webbrowser
    print(f"\n🌐 Opening: {sql_editor_url}")
    webbrowser.open(sql_editor_url)
    
    print("\n⏳ After running the SQL, press ENTER to continue...")
    input()
    
    # Verify table exists
    try:
        result = client.table("pending_research").select("id").limit(1).execute()
        print("✅ Table created successfully!")
        return True
    except Exception as e:
        print(f"⚠️  Could not verify table: {e}")
        print("Please make sure you ran the SQL in the browser.")
        return False

if __name__ == "__main__":
    create_table_simple()
