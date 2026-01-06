# Verify PayPal Schema
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

try:
    from supabase import create_client, Client
    print("✅ Supabase library found")
except ImportError:
    print("❌ Supabase library not installed")
    print("Run: pip install supabase python-dotenv")
    exit()

# Supabase credentials
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY") or os.getenv("SUPABASE_ANON_KEY")


if not SUPABASE_URL or not SUPABASE_KEY:
    print("❌ Error: SUPABASE_URL and SUPABASE_KEY environment variables are not set.")
    exit()

print("\nConnecting to Supabase...")
try:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("✅ Connection successful.")
except Exception as e:
    print(f"❌ Error connecting to Supabase: {e}")
    exit()

# Test 0: Check connectivity (Categories)
print("\nTest 0: Checking connectivity (Categories)...")
try:
    response = supabase.table("categories").select("*", count="exact").limit(1).execute()
    print(f"✅ Connection verified. Categories count: {response.count}")
except Exception as e:
    print(f"❌ Error checking 'categories' (Key might be invalid): {e}")


# Test 1: Check payment_history table
print("\nTest 1: Checking payment_history table...")
try:
    # Try to select one row, or just count. If table doesn't exist, it will throw error.
    response = supabase.table("payment_history").select("*", count="exact").limit(1).execute()
    print(f"✅ 'payment_history' table exists. Count: {response.count}")
except Exception as e:
    print(f"❌ Error checking 'payment_history' table: {e}")

# Test 2: Check user_profiles columns
print("\nTest 2: Checking user_profiles columns...")
try:
    # We can't easily check columns via API without selecting.
    # We'll try to select 'paypal_subscription_id' from user_profiles.
    response = supabase.table("user_profiles").select("paypal_subscription_id").limit(1).execute()
    print(f"✅ 'paypal_subscription_id' column exists in user_profiles.")
except Exception as e:
    print(f"❌ Error checking columns in 'user_profiles': {e}")
