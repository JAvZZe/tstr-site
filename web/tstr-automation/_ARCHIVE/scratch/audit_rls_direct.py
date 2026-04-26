import psycopg2
from dotenv import load_dotenv

# Load env
load_dotenv('web/tstr-automation/.env')

# Database connection details from TSTR_hub_Supabase_Keys.md
# Host: db.haimjeaetrsaauitrhfy.supabase.co
# Port: 5432
# DB: postgres
# User: postgres
# Password: 3jgUcxVKtxvuAhkZ

DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASS = "3jgUcxVKtxvuAhkZ"
DB_HOST = "db.haimjeaetrsaauitrhfy.supabase.co"
DB_PORT = "5432"

print(f"Connecting to Supabase Database ({DB_HOST})...")

try:
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        host=DB_HOST,
        port=DB_PORT
    )
    cur = conn.cursor()
    
    print("\n--- RLS POLICIES AUDIT ---")
    
    # Query RLS policies for listings table
    query = """
    SELECT 
        policyname, 
        roles, 
        cmd, 
        qual, 
        with_check 
    FROM 
        pg_policies 
    WHERE 
        schemaname = 'public' 
        AND tablename = 'listings';
    """
    
    cur.execute(query)
    policies = cur.fetchall()
    
    if not policies:
        print("No RLS policies found for table 'listings'.")
    else:
        for p in policies:
            print(f"\nPolicy: {p[0]}")
            print(f"  Roles: {p[1]}")
            print(f"  Command: {p[2]}")
            print(f"  Qual: {p[3]}")
            print(f"  With Check: {p[4]}")

    # Check if RLS is enabled on the table
    cur.execute("SELECT relrowsecurity FROM pg_class WHERE relname = 'listings';")
    rls_enabled = cur.fetchone()[0]
    print(f"\nRLS Enabled on 'listings': {rls_enabled}")

    # Check 'listing_premium_data' as well
    cur.execute("""
    SELECT 
        policyname, roles, cmd 
    FROM 
        pg_policies 
    WHERE 
        tablename = 'listing_premium_data';
    """)
    premium_policies = cur.fetchall()
    print(f"\nPolicies for 'listing_premium_data': {len(premium_policies)}")
    for p in premium_policies:
        print(f"  - {p[0]} ({p[2]}) for {p[1]}")

    cur.close()
    conn.close()
    print("\nAudit Complete.")

except Exception as e:
    print(f"Error connecting to database: {e}")
