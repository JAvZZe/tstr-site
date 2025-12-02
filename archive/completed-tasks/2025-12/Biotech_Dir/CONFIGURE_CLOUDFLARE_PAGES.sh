#!/bin/bash
# Configure Cloudflare Pages Environment Variables
# This script uses the Cloudflare API to set environment variables

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Cloudflare Pages Environment Variables Setup"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Configuration
ACCOUNT_ID="${CLOUDFLARE_ACCOUNT_ID}"
PROJECT_NAME="tstr-site"  # Your Cloudflare Pages project name
API_TOKEN="${CLOUDFLARE_API_TOKEN}"

# Environment Variables to Set
PUBLIC_SUPABASE_URL="https://haimjeaetrsaauitrhfy.supabase.co"
PUBLIC_SUPABASE_ANON_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhhaW1qZWFldHJzYWF1aXRyaGZ5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjAwNjAxNTksImV4cCI6MjA3NTYzNjE1OX0.1SoHZoMAeap4p2Fy4HxzHJ4IRZWZ78VamGd0JWQ0OqM"
SUPABASE_SERVICE_ROLE_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhhaW1qZWFldHJzYWF1aXRyaGZ5Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTcyOTQ0ODQzNywiZXhwIjoyMDQ1MDI0NDM3fQ.sb_secret_zRN1fTFOYnN7cEbEIfAP7A_YrEKBfI2"

# Check prerequisites
if [ -z "$ACCOUNT_ID" ]; then
    echo -e "${RED}❌ CLOUDFLARE_ACCOUNT_ID not set${NC}"
    echo ""
    echo "Get your Account ID from:"
    echo "https://dash.cloudflare.com/ → Click on Pages → Project Settings"
    echo ""
    echo "Then run:"
    echo "export CLOUDFLARE_ACCOUNT_ID='your-account-id'"
    exit 1
fi

if [ -z "$API_TOKEN" ]; then
    echo -e "${RED}❌ CLOUDFLARE_API_TOKEN not set${NC}"
    echo ""
    echo "Get your API Token from:"
    echo "https://dash.cloudflare.com/profile/api-tokens"
    echo ""
    echo "Required permissions:"
    echo "- Account.Cloudflare Pages: Edit"
    echo ""
    echo "Then run:"
    echo "export CLOUDFLARE_API_TOKEN='your-api-token'"
    exit 1
fi

echo -e "${YELLOW}📋 Configuration:${NC}"
echo "Account ID: $ACCOUNT_ID"
echo "Project: $PROJECT_NAME"
echo ""

# Function to set environment variable via Cloudflare API
set_env_var() {
    local key=$1
    local value=$2
    local environment=${3:-"production"}  # production or preview
    
    echo -e "${YELLOW}Setting: $key (${environment})${NC}"
    
    # Cloudflare Pages API endpoint
    API_URL="https://api.cloudflare.com/client/v4/accounts/${ACCOUNT_ID}/pages/projects/${PROJECT_NAME}"
    
    # Create JSON payload
    PAYLOAD=$(cat <<EOF
{
  "deployment_configs": {
    "${environment}": {
      "env_vars": {
        "${key}": {
          "value": "${value}"
        }
      }
    }
  }
}
EOF
)
    
    # Make API call
    response=$(curl -s -X PATCH "${API_URL}" \
        -H "Authorization: Bearer ${API_TOKEN}" \
        -H "Content-Type: application/json" \
        -d "${PAYLOAD}")
    
    if echo "$response" | grep -q '"success":true'; then
        echo -e "${GREEN}✅ Set $key${NC}"
        return 0
    else
        echo -e "${RED}❌ Failed to set $key${NC}"
        echo "Response: $response"
        return 1
    fi
}

# Set all environment variables
echo -e "${YELLOW}Setting environment variables for production...${NC}"
echo ""

set_env_var "PUBLIC_SUPABASE_URL" "$PUBLIC_SUPABASE_URL" "production"
set_env_var "PUBLIC_SUPABASE_ANON_KEY" "$PUBLIC_SUPABASE_ANON_KEY" "production"
set_env_var "SUPABASE_SERVICE_ROLE_KEY" "$SUPABASE_SERVICE_ROLE_KEY" "production"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${GREEN}✅ Environment variables configured!${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Next steps:"
echo "1. Trigger a new deployment (push to main or manual redeploy)"
echo "2. Wait 2-3 minutes for build"
echo "3. Test at: https://tstr.site/waitlist"
echo ""
