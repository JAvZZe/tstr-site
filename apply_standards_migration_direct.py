#!/usr/bin/env python3
"""
Apply standards and capabilities migration directly to Supabase PostgreSQL
"""

import os
import sys

def apply_migration():
    """Apply the standards migration using direct PostgreSQL connection"""
    
    print("="*70)
    print("APPLYING STANDARDS & CAPABILITIES MIGRATION")
    print("="*70)
    
    # Install psycopg2 if needed
    try:
        import psycopg2
    except ImportError:
        print("Installing psycopg2-binary...")
        import subprocess
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'psycopg2-binary'])
        import psycopg2
    
    # Database connection details
    project_ref = "haimjeaetrsaauitrhfy"
    db_password = "O6@R@qV2P5iD0p4"
    
    from urllib.parse import quote_plus
    encoded_password = quote_plus(db_password)
    
    conn_string = f"postgresql://postgres:{encoded_password}@db.{project_ref}.supabase.co:5432/postgres"
    
    # Read migration file
    migration_path = "supabase/migrations/20251120000001_add_standards_and_capabilities.sql"
    print(f"\n📄 Reading migration: {migration_path}")
    
    with open(migration_path, 'r') as f:
        migration_sql = f.read()
    
    print(f"📊 Migration size: {len(migration_sql)} characters")
    
    try:
        print("\n🔌 Connecting to database...")
        conn = psycopg2.connect(conn_string)
        conn.autocommit = False  # Use transaction
        cursor = conn.cursor()
        
        print("🚀 Executing migration SQL...")
        cursor.execute(migration_sql)
        
        print("💾 Committing transaction...")
        conn.commit()
        
        print("\n✅ Migration applied successfully!")
        
        # Verify tables were created
        print("\n🔍 Verifying new tables...")
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_name IN ('standards', 'listing_capabilities')
            ORDER BY table_name;
        """)
        
        tables = cursor.fetchall()
        for table in tables:
            print(f"  ✓ {table[0]} table created")
            
            # Count rows
            cursor.execute(f"SELECT COUNT(*) FROM {table[0]};")
            count = cursor.fetchone()[0]
            print(f"    Current rows: {count}")
        
        # Verify search function exists
        cursor.execute("""
            SELECT routine_name 
            FROM information_schema.routines 
            WHERE routine_schema = 'public' 
            AND routine_name = 'search_by_standard';
        """)
        
        if cursor.fetchone():
            print("  ✓ search_by_standard() function created")
        
        cursor.close()
        conn.close()
        
        print("\n" + "="*70)
        print("✅ MIGRATION COMPLETE!")
        print("="*70)
        print("\nNext steps:")
        print("  1. Seed initial standards data")
        print("  2. Build search API endpoint")
        print("  3. Create frontend search interface")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error applying migration: {e}")
        print("\nTrying to rollback...")
        try:
            conn.rollback()
            print("✓ Rollback successful")
        except:
            print("✗ Rollback failed")
        
        print("\nPlease apply migration manually:")
        print(f"  1. Go to: https://supabase.com/dashboard/project/{project_ref}/sql")
        print(f"  2. Copy SQL from: {migration_path}")
        print("  3. Paste and run in SQL Editor")
        
        return False

if __name__ == "__main__":
    success = apply_migration()
    sys.exit(0 if success else 1)
