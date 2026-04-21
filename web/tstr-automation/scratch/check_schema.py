import os
import requests
from dotenv import load_dotenv

# Load environment variables
ENV_PATH = '/media/al/AI_DATA/AI_PROJECTS_SPACE/ACTIVE_PROJECTS/tstr-site-working/web/tstr-automation/.env'
load_dotenv(dotenv_path=ENV_PATH)

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("PUBLIC_SUPABASE_ANON_KEY")

def check_schema():
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}"
    }
    # Query one row to see columns
    url = f"{SUPABASE_URL}/rest/v1/listings?select=*&limit=1"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data:
            print("Columns in 'listings':")
            print(list(data[0].keys()))
        else:
            print("No data in 'listings'")
    else:
        print(f"Error: {response.status_code} - {response.text}")

if __name__ == "__main__":
    check_schema()
