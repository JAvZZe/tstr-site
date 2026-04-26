
import psycopg2
import os
from dotenv import load_dotenv

# Try to load from root or current dir
load_dotenv(".env")
load_dotenv("web/tstr-automation/.env")

DB_PASS = "3jgUcxVKtxvuAhkZ"
DB_HOST = "aws-0-us-east-1.pooler.supabase.com"
DB_PORT = "5432" # Session Mode
DB_NAME = "postgres"
DB_USER = "postgres.haimjeaetrsaauitrhfy"

def apply_migration():
    conn_str = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    
    query = """
    ALTER TABLE listing_premium_data
      ADD COLUMN IF NOT EXISTS map_tier TEXT NOT NULL DEFAULT 'static'
        CHECK (map_tier IN ('none', 'static', 'premium')),
      ADD COLUMN IF NOT EXISTS coverage_radius_km INTEGER DEFAULT NULL;

    COMMENT ON COLUMN listing_premium_data.map_tier IS
      'none=no map, static=Static Maps API img, premium=interactive JS map';
    COMMENT ON COLUMN listing_premium_data.coverage_radius_km IS
      'Service area radius in km for premium map polygon. NULL = no polygon.';
    """
    
    print(f"Connecting to {DB_HOST} (pooler)...")
    try:
        conn = psycopg2.connect(conn_str)
        conn.autocommit = True
        cur = conn.cursor()
        print("Executing migration...")
        cur.execute(query)
        print("✅ Migration applied successfully.")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ Error applying migration: {e}")

if __name__ == "__main__":
    apply_migration()
