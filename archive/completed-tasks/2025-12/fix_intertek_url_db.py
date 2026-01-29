#!/usr/bin/env python3
"""
Execute SQL to fix Intertek URL in pending_research table
"""

import os

# Load environment variables manually
os.environ["SUPABASE_URL"] = "https://haimjeaetrsaauitrhfy.supabase.co"


def fix_intertek_url():
    """Execute SQL to fix Intertek URL"""

    print("=" * 70)
    print("FIXING INTERTEK URL IN PENDING_RESEARCH TABLE")
    print("=" * 70)

    # Install psycopg2 if needed
    try:
        import psycopg2
    except ImportError:
        print("Installing psycopg2...")
        import subprocess

        subprocess.check_call(["pip", "install", "psycopg2-binary"])
        import psycopg2

    # Get credentials
    supabase_url = os.getenv("SUPABASE_URL", "https://haimjeaetrsaauitrhfy.supabase.co")

    # Extract project ref from URL
    project_ref = supabase_url.replace("https://", "").replace(".supabase.co", "")

    # Connection string - using direct connection
    from urllib.parse import quote_plus

    db_password = "O6@R@qV2P5iD0p4"  # From your project
    encoded_password = quote_plus(db_password)

    conn_string = f"postgresql://postgres:{encoded_password}@db.{project_ref}.supabase.co:5432/postgres"

    sql = """
    -- Fix Intertek URL in pending_research table
    UPDATE pending_research
    SET website = 'https://www.intertek.com/'
    WHERE business_name ILIKE '%intertek%'
      AND (website IS NULL OR website != 'https://www.intertek.com/');

    -- Show the updated records
    SELECT id, business_name, website, validation_error, created_at
    FROM pending_research
    WHERE business_name ILIKE '%intertek%'
    ORDER BY created_at DESC;
    """

    try:
        # Connect to database
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor()

        print("Connected to Supabase database...")

        # Execute the SQL
        cursor.execute(sql)

        # Fetch and display results
        results = cursor.fetchall()

        print("\n✅ Successfully updated Intertek URL!")
        print(f"Found {len(results)} Intertek records:")

        for row in results:
            print(f"  ID: {row[0]}")
            print(f"  Business: {row[1]}")
            print(f"  Website: {row[2]}")
            print(f"  Error: {row[3]}")
            print(f"  Created: {row[4]}")
            print("-" * 50)

        # Commit the changes
        conn.commit()

        print("\n✅ Changes committed successfully!")

    except Exception as e:
        print(f"❌ Error: {e}")
        if "conn" in locals():
            conn.rollback()
        return False

    finally:
        if "cursor" in locals():
            cursor.close()
        if "conn" in locals():
            conn.close()

    return True


if __name__ == "__main__":
    success = fix_intertek_url()
    if success:
        print("\n🎉 Intertek URL fix completed!")
    else:
        print("\n❌ Failed to fix Intertek URL")
