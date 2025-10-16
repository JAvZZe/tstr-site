"""
Execute SQL directly via Supabase using psycopg2
"""

import os
from dotenv import load_dotenv

load_dotenv()

def execute_sql():
    """Execute SQL to create pending_research table"""
    
    print("="*70)
    print("CREATING PENDING_RESEARCH TABLE")
    print("="*70)
    
    # Install psycopg2 if needed
    try:
        import psycopg2
    except ImportError:
        print("Installing psycopg2...")
        import subprocess
        subprocess.check_call(['pip', 'install', 'psycopg2-binary'])
        import psycopg2
    
    # Get credentials
    supabase_url = os.getenv("SUPABASE_URL")
    
    # Extract project ref from URL
    project_ref = supabase_url.replace('https://', '').replace('.supabase.co', '')
    
    # Connection string - using direct connection
    # Format: postgresql://postgres:{password}@db.{ref}.supabase.co:5432/postgres
    from urllib.parse import quote_plus
    
    db_password = "O6@R@qV2P5iD0p4"  # From your project
    encoded_password = quote_plus(db_password)
    
    conn_string = f"postgresql://postgres:{encoded_password}@db.{project_ref}.supabase.co:5432/postgres"
    
    sql = """
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
    
    ALTER TABLE pending_research ENABLE ROW LEVEL SECURITY;
    
    DROP POLICY IF EXISTS "Enable read access for all users" ON pending_research;
    CREATE POLICY "Enable read access for all users" ON pending_research
        FOR SELECT USING (true);
    
    DROP POLICY IF EXISTS "Enable insert for authenticated users" ON pending_research;
    CREATE POLICY "Enable insert for authenticated users" ON pending_research
        FOR INSERT WITH CHECK (true);
    
    DROP POLICY IF EXISTS "Enable update for authenticated users" ON pending_research;
    CREATE POLICY "Enable update for authenticated users" ON pending_research
        FOR UPDATE USING (true);
    """
    
    try:
        print("Connecting to database...")
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor()
        
        print("Executing SQL...")
        cursor.execute(sql)
        conn.commit()
        
        print("✅ Successfully created pending_research table!")
        
        # Verify
        cursor.execute("SELECT COUNT(*) FROM pending_research;")
        count = cursor.fetchone()[0]
        print(f"✓ Table verified. Current rows: {count}")
        
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nConnection string format:")
        print(f"postgresql://postgres.{project_ref}:[password]@aws-0-us-west-1.pooler.supabase.com:6543/postgres")
        return False

if __name__ == "__main__":
    success = execute_sql()
    
    if success:
        print("\n✅ Setup complete! Running cleanup script...")
        print("="*70)
    else:
        print("\n❌ Setup failed. Please create table manually in Supabase SQL Editor.")
