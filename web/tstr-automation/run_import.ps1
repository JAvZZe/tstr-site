# Paste your service_role key here (replace the xxx part)
$serviceKey = 'PASTE_YOUR_SERVICE_ROLE_KEY_HERE'

# Temporarily set environment variable
$env:SUPABASE_SERVICE_KEY = $serviceKey

# Update import script to use service key
(Get-Content import_to_supabase.py) -replace 'Supabase_Gemini_tstr_site1_API_KEY', 'SUPABASE_SERVICE_KEY' | Set-Content import_to_supabase_temp.py

# Run import
python import_to_supabase_temp.py
