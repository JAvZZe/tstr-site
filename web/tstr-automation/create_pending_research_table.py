"""
Create pending_research table in Supabase
"""

import os
from dotenv import load_dotenv

load_dotenv()

def create_table():
    """Create the pending_research table"""
    try:
        from supabase import create_client
        
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
        
        client = create_client(supabase_url, supabase_key)
        
        # Read SQL file
        with open('create_pending_research_table.sql', 'r') as f:
            sql = f.read()
        
        # Execute SQL (note: Supabase Python client doesn't directly support raw SQL execution)
        # We'll use the REST API instead
        print("⚠️  Note: This SQL needs to be executed in Supabase SQL Editor")
        print("Please copy the SQL from create_pending_research_table.sql")
        print("and run it in: https://app.supabase.com/project/haimjeaetrsaauitrhfy/sql")
        
        print("\nOr run this command:")
        print("supabase db push")
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    create_table()
