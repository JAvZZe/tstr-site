import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv('web/tstr-automation/.env')

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
supabase = create_client(url, key)

# Check columns in listing_premium_data
try:
    # We can't query information_schema directly easily via the client sometimes
    # but we can try to fetch one row and see the keys
    data = supabase.table("listing_premium_data").select("*").limit(1).execute()
    if data.data:
        print("listing_premium_data columns:", data.data[0].keys())
    else:
        print("listing_premium_data is empty")
except Exception as e:
    print("Error querying listing_premium_data:", e)

# Also check if there's a subscriptions table
try:
    # Try a common name
    data = supabase.table("subscriptions").select("*").limit(1).execute()
    print("subscriptions table exists")
except:
    print("subscriptions table does not exist or access denied")
