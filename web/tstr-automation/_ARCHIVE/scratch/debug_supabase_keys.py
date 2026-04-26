import os
import requests
from dotenv import load_dotenv

# Load environment variables
ENV_PATH = '/media/al/AI_DATA/AI_PROJECTS_SPACE/ACTIVE_PROJECTS/tstr-site-working/web/tstr-frontend/.env'
load_dotenv(dotenv_path=ENV_PATH)

SUPABASE_URL = os.environ.get("PUBLIC_SUPABASE_URL")
SERVICE_ROLE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")

def check_db():
    print(f"Supabase URL: {SUPABASE_URL}")
    print(f"Service Role Key: {SERVICE_ROLE_KEY[:10]}...")

    headers = {
        "apikey": SERVICE_ROLE_KEY,
        "Authorization": f"Bearer {SERVICE_ROLE_KEY}"
    }

    # Query policies
    # Postgrest doesn't expose pg_policies by default.
    # We'll try to query the listings table directly to see if it works with service role.
    url = f"{SUPABASE_URL}/rest/v1/listings?select=count&status=eq.active"
    response = requests.get(url, headers=headers)
    print(f"Listings Count (Service Role): {response.status_code}")
    if response.status_code == 200:
        print(f"Result: {response.json()}")

    # Query with anon key
    ANON_KEY = os.environ.get("PUBLIC_SUPABASE_ANON_KEY")
    headers_anon = {
        "apikey": ANON_KEY,
        "Authorization": f"Bearer {ANON_KEY}"
    }
    response_anon = requests.get(url, headers=headers_anon)
    print(f"Listings Count (Anon Key): {response_anon.status_code}")
    if response_anon.status_code == 200:
        print(f"Result: {response_anon.json()}")

if __name__ == "__main__":
    check_db()
