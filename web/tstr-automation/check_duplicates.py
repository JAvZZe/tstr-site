# ruff: noqa: E402
import os
from dotenv import load_dotenv
# Load environment variables from .env file in the same directory as this script
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))



# Load environment variables from .env file in the same directory as this script

from supabase import create_client

supabase = create_client(
    os.environ.get("SUPABASE_URL"),
    os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
)

# Get category
category = supabase.table('categories').select('id').eq('slug', 'environmental-testing').execute()
cat_id = category.data[0]['id']

# Query for duplicate detection - empty website
duplicates = supabase.table('listings').select('id, business_name, website').eq('category_id', cat_id).eq('website', '').execute()

print(f"Listings with empty website: {len(duplicates.data)}")
for listing in duplicates.data:
    print(f"  - {listing['business_name']}: website='{listing.get('website', 'NULL')}'")

# Query for all listings
all = supabase.table('listings').select('id, business_name, website').eq('category_id', cat_id).execute()
print(f"\nTotal listings: {len(all.data)}")
for listing in all.data:
    print(f"  - {listing['business_name']}: website='{listing.get('website', 'NULL')}'")

