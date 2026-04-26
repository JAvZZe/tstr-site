from supabase import create_client

url = "http://127.0.0.1:54321"
key = "LOCAL_KEY_REMOVED"

# Force standard client creation
try:
    supabase = create_client(url, key)
    res = supabase.from_("categories").select("id, slug").execute()
    print("Success! Categories found:")
    print(res.data)
except Exception as e:
    print(f"Failed to connect: {e}")
