#!/bin/bash
# Script to update Supabase service role key across all config files

if [ -z "$1" ]; then
    echo "Usage: $0 <service_role_key>"
    echo "Example: $0 eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    exit 1
fi

SERVICE_KEY="$1"

# Update frontend .env
sed -i "s|SUPABASE_SERVICE_ROLE_KEY=.*|SUPABASE_SERVICE_ROLE_KEY=$SERVICE_KEY|" web/tstr-frontend/.env

# Update automation .env if it exists
if [ -f "web/tstr-automation/.env" ]; then
    sed -i "s|SUPABASE_SERVICE_ROLE_KEY=.*|SUPABASE_SERVICE_ROLE_KEY=$SERVICE_KEY|" web/tstr-automation/.env
fi

echo "✅ Service role key updated in environment files"
echo "🔄 Restart any running applications to pick up the new key"
