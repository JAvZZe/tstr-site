
import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv("/media/al/AI_DATA/AI_PROJECTS_SPACE/ACTIVE_PROJECTS/tstr-site-working/web/tstr-automation/.env")

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

res = supabase.table("listings").select("business_name, address, region, latitude").is_("latitude", "null").limit(20).execute()
for row in res.data:
    print(f"{row['business_name']} | {row['address']} | {row['region']}")
