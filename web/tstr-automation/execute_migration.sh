#!/bin/bash
# Execute SQL migration using Supabase Management API

PROJECT_ID="haimjeaetrsaauitrhfy"
ACCESS_TOKEN="sbp_e290bc7ea1ba64ae4b0be38134b7b4a67ca24e04"
MIGRATION_FILE="/home/al/tstr-site-working/web/tstr-automation/migrations/add_niche_custom_fields.sql"

echo "=================================="
echo "Executing Custom Fields Migration"
echo "=================================="
echo ""
echo "Project ID: $PROJECT_ID"
echo "Migration file: $MIGRATION_FILE"
echo ""

# Read the SQL file
SQL_CONTENT=$(cat "$MIGRATION_FILE")

# Execute via Supabase Management API
# https://supabase.com/docs/reference/api/introduction
curl -X POST \
  "https://api.supabase.com/v1/projects/${PROJECT_ID}/database/query" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d "{\"query\": $(jq -Rs . < "$MIGRATION_FILE")}"

echo ""
echo "=================================="
echo "Migration execution completed"
echo "=================================="
