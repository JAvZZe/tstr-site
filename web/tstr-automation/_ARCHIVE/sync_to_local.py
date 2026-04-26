import os
from supabase import create_client
from dotenv import load_dotenv

# Remote config
load_dotenv('.env')
remote_url = os.getenv('SUPABASE_URL')
remote_key = os.getenv('SUPABASE_SERVICE_ROLE_KEY')
remote_supabase = create_client(remote_url, remote_key)

# Local config
local_url = "http://127.0.0.1:54321"
local_key = os.getenv("LOCAL_SUPABASE_SERVICE_ROLE_KEY", "placeholder")
local_supabase = create_client(local_url, local_key)

def sync_category(slug):
    print(f"Syncing {slug}...")
    # Get remote category
    cat = remote_supabase.from_('categories').select('*').eq('slug', slug).single().execute().data
    if not cat:
        print("Category not found on remote")
        return
    
    # Upsert local category
    local_supabase.from_('categories').upsert(cat).execute()
    cat_id = cat['id']
    
    # Sync custom fields
    cfs = remote_supabase.from_('custom_fields').select('*').eq('category_id', cat_id).execute().data
    if cfs:
        local_supabase.from_('custom_fields').upsert(cfs).execute()
        print(f"Synced {len(cfs)} custom fields")
        
    # Sync listings (limited for speed)
    listings = remote_supabase.from_('listings').select('*').eq('category_id', cat_id).limit(50).execute().data
    if listings:
        local_supabase.from_('listings').upsert(listings).execute()
        print(f"Synced {len(listings)} listings")

if __name__ == "__main__":
    sync_category('materials-testing')
