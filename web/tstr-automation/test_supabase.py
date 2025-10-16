# Test Supabase Connection
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Check if supabase library is installed
try:
    from supabase import create_client, Client
    print("✅ Supabase library found")
except ImportError:
    print("❌ Supabase library not installed")
    print("Run: pip install supabase python-dotenv")
    exit()

# Supabase credentials from environment variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    print("❌ Error: SUPABASE_URL and SUPABASE_KEY environment variables are not set.")
    print("Please create a .env file in this directory with the following content:")
    print("SUPABASE_URL=your_supabase_url")
    print("SUPABASE_KEY=your_supabase_key")
    exit()

# Create Supabase client
print("\nConnecting to Supabase...")
try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("✅ Connection successful.")
except Exception as e:
    print(f"❌ Error connecting to Supabase: {e}")
    exit()

# Test 1: Fetch categories
print("\nTest 1: Fetching categories...")
try:
    response = supabase.table("categories").select("*").limit(5).execute()
    print(f"✅ Found {len(response.data)} categories (showing up to 5):")
    for cat in response.data:
        print(f"   - {cat['name']}")
except Exception as e:
    print(f"❌ Error fetching categories: {e}")

# Test 2: Fetch locations
print("\nTest 2: Fetching locations...")
try:
    response = supabase.table("locations").select("*").eq("level", "city").limit(5).execute()
    print(f"✅ Found {len(response.data)} cities (showing up to 5):")
    for loc in response.data:
        print(f"   - {loc['name']}")
except Exception as e:
    print(f"❌ Error fetching locations: {e}")

# Test 3: Check listings count
print("\nTest 3: Checking existing listings...")
try:
    response = supabase.table("listings").select("*", count="exact").execute()
    print(f"✅ Current listings: {response.count}")
except Exception as e:
    print(f"❌ Error counting listings: {e}")

print("\n✅ Supabase connection test complete!")
