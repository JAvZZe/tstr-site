"""
Setup pending_research table in Supabase via REST API
"""

import os
from dotenv import load_dotenv

load_dotenv()

def create_pending_research_table():
    """Create pending_research table using Supabase REST API"""
    
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    
    if not supabase_url or not supabase_key:
        print("❌ Error: Missing Supabase credentials")
        return False
    
    # SQL to create table
    sql = """
    CREATE TABLE IF NOT EXISTS pending_research (
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
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
    """
    
    # Supabase SQL endpoint (using PostgREST)
    # Note: Direct SQL execution requires using pgAdmin or SQL Editor
    # Instead, we'll use the Python client to verify connection and create via insert
    
    print("="*70)
    print("CREATING PENDING_RESEARCH TABLE")
    print("="*70)
    
    try:
        from supabase import create_client
        client = create_client(supabase_url, supabase_key)
        
        # Try to check if table exists by attempting to select
        try:
            result = client.table("pending_research").select("id").limit(1).execute()
            print("✅ Table 'pending_research' already exists!")
            print(f"   Found {len(result.data)} existing records")
            return True
        except Exception:
            print("📝 Table doesn't exist yet. Creating...")
            
            # Since direct SQL execution isn't available via Python client,
            # we'll use psycopg2 if available
            try:
                import psycopg2
                
                # Extract project ref from URL
                project_ref = supabase_url.replace('https://', '').replace('.supabase.co', '')
                
                # Construct PostgreSQL connection string
                # You'll need the direct database connection string from Supabase
                print("\n⚠️  Direct SQL execution requires database connection string")
                print("Please get it from: Supabase Dashboard > Project Settings > Database")
                print("Connection string format: postgresql://postgres:[password]@db.[project-ref].supabase.co:5432/postgres")
                
                db_password = os.getenv("SUPABASE_DB_PASSWORD")
                if db_password:
                    conn_string = f"postgresql://postgres:{db_password}@db.{project_ref}.supabase.co:5432/postgres"
                    
                    conn = psycopg2.connect(conn_string)
                    cursor = conn.cursor()
                    cursor.execute(sql)
                    conn.commit()
                    cursor.close()
                    conn.close()
                    
                    print("✅ Successfully created pending_research table!")
                    return True
                else:
                    raise ImportError("No DB password")
                    
            except (ImportError, Exception):
                print("\n⚠️  Cannot create table programmatically")
                print("Please run this SQL in Supabase SQL Editor:")
                print("URL: https://app.supabase.com/project/" + supabase_url.split('//')[1].split('.')[0] + "/sql")
                print("\n" + "="*70)
                print(sql)
                print("="*70)
                return False
                
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = create_pending_research_table()
    
    if success:
        print("\n✅ Setup complete! You can now run cleanup_invalid_urls.py")
    else:
        print("\n📋 Manual setup required. Copy SQL above and run in Supabase.")
