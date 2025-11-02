#!/usr/bin/env python3
"""
Execute RLS fix for locations table
"""
import subprocess
import os

# Read the SQL file
with open('/home/al/tstr-site-working/web/tstr-automation/migrations/fix_locations_rls.sql', 'r') as f:
    sql = f.read()

print("Executing RLS fix for locations table...")
print("SQL to execute:")
print(sql)
print("\n" + "="*50 + "\n")

# Get DB password from environment or prompt
db_password = os.getenv('SUPABASE_DB_PASSWORD')
if not db_password:
    db_password = input('Enter Supabase DB password: ')

# Connection string
db_url = f"postgresql://postgres.haimjeaetrsaauitrhfy:{db_password}@aws-0-us-east-1.pooler.supabase.com:6543/postgres"

# Execute via psql
result = subprocess.run(
    ['psql', db_url, '-c', sql],
    capture_output=True,
    text=True
)

print("STDOUT:")
print(result.stdout)

if result.stderr:
    print("\nSTDERR:")
    print(result.stderr)

if result.returncode == 0:
    print("\n✓ RLS policy added successfully!")
else:
    print(f"\n✗ Failed with return code {result.returncode}")
