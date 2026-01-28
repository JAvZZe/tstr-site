#!/usr/bin/env python3
"""
Execute RLS policy fix for public form submissions to listings table
Allows anonymous users to submit pending listings
"""
import subprocess
import os
import sys

# Read the migration SQL
migration_file = '/media/al/AI_DATA/AI_PROJECTS_SPACE/ACTIVE_PROJECTS/TSTR-site/tstr-site-working/web/tstr-automation/supabase/migrations/20251118000001_fix_rls_public_submissions.sql'

if not os.path.exists(migration_file):
    print(f"Error: Migration file not found: {migration_file}")
    sys.exit(1)

with open(migration_file, 'r') as f:
    sql = f.read()

print("=" * 70)
print("tstr.directory - Execute RLS Policy for Public Form Submissions")
print("=" * 70)
print("\nSQL to execute:")
print("-" * 70)
print(sql)
print("-" * 70)

# Get DB password from environment or prompt
db_password = os.getenv('SUPABASE_DB_PASSWORD')
if not db_password:
    print("\nEnter Supabase database password:")
    print("(You can find it in Supabase dashboard > Database settings)")
    db_password = input('Password: ')

if not db_password:
    print("Error: Password required")
    sys.exit(1)

# Connection string for Supabase pooler
db_url = f"postgresql://postgres.haimjeaetrsaauitrhfy:{db_password}@aws-0-us-east-1.pooler.supabase.com:6543/postgres"

print("\nExecuting SQL...")
print("-" * 70)

# Execute via psql
result = subprocess.run(
    ['psql', db_url, '-c', sql],
    capture_output=True,
    text=True
)

# Display output
if result.stdout:
    print("RESULT:")
    print(result.stdout)

if result.stderr:
    print("\nDETAILS:")
    print(result.stderr)

print("-" * 70)

if result.returncode == 0:
    print("\n✓ SUCCESS: RLS policy for public submissions applied!")
    print("\nNext steps:")
    print("1. Test the form at https://tstr.directory/submit")
    print("2. Verify listing appears in database with status='pending'")
    print("3. Check admin dashboard for pending approvals")
else:
    print(f"\n✗ FAILED: Command returned code {result.returncode}")
    print("\nTroubleshooting:")
    print("1. Verify password is correct")
    print("2. Check Supabase dashboard for database connectivity")
    print("3. Verify database is running")
    sys.exit(1)

print("\n" + "=" * 70)
