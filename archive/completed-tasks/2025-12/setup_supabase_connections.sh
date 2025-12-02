#!/bin/bash
# Setup script for Supabase connections from dashboard

echo "🔗 Supabase Connection Setup"
echo "Copy these from: https://supabase.com/dashboard/project/haimjeaetrsaauitrhfy → Connect"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}1. CONNECTION STRING (for diagnostics):${NC}"
echo "   postgresql://postgres:[password]@db.haimjeaetrsaauitrhfy.supabase.co:5432/postgres"
echo "   → Save this for database diagnostics"
echo ""

echo -e "${GREEN}2. SERVICE ROLE KEY (most important):${NC}"
echo "   → From: Settings → API → service_role key"
echo "   → Run: ./update_service_key.sh [your_key_here]"
echo ""

echo -e "${YELLOW}3. MCP CONFIGURATION:${NC}"
echo "   → Copy the MCP JSON from Connect → MCP"
echo "   → This enables AI assistance with your database"
echo ""

echo -e "${YELLOW}4. APP FRAMEWORKS:${NC}"
echo "   → Get the JavaScript/TypeScript config"
echo "   → Useful for verifying current setup"
echo ""

echo -e "${RED}SKIP THESE:${NC}"
echo "   → Mobile Frameworks (not needed for web app)"
echo "   → ORMs (we use direct SQL for scrapers)"
