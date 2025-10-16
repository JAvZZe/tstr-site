#!/bin/bash

# TSTR.SITE - Cloud Function Deployment Script
# Deploys scrapers to Google Cloud Functions

set -e  # Exit on error

echo "=================================="
echo "TSTR.SITE Cloud Deployment"
echo "=================================="

# Configuration
PROJECT_ID="tstr-automation"
REGION="us-central1"
RUNTIME="python311"
TIMEOUT="540s"
MEMORY="512MB"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo -e "${RED}Error: gcloud CLI is not installed${NC}"
    echo "Install from: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

echo -e "${GREEN}✓${NC} gcloud CLI found"

# Check if project is set
CURRENT_PROJECT=$(gcloud config get-value project 2>/dev/null)
if [ "$CURRENT_PROJECT" != "$PROJECT_ID" ]; then
    echo -e "${YELLOW}Setting project to: $PROJECT_ID${NC}"
    gcloud config set project $PROJECT_ID
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo -e "${RED}Error: .env file not found${NC}"
    echo "Please create .env file with:"
    echo "  SUPABASE_URL=..."
    echo "  SUPABASE_KEY=..."
    echo "  GOOGLE_MAPS_API_KEY=..."
    exit 1
fi

echo -e "${GREEN}✓${NC} .env file found"

# Load environment variables
source .env

# Deploy Primary Scraper
echo -e "\n${YELLOW}Deploying primary scraper...${NC}"
gcloud functions deploy tstr-scraper-primary \
  --gen2 \
  --runtime=$RUNTIME \
  --region=$REGION \
  --source=. \
  --entry-point=run_primary_scraper \
  --trigger-http \
  --allow-unauthenticated \
  --timeout=$TIMEOUT \
  --memory=$MEMORY \
  --set-env-vars="SUPABASE_URL=$SUPABASE_URL,SUPABASE_KEY=$SUPABASE_KEY,SUPABASE_SERVICE_ROLE_KEY=$SUPABASE_SERVICE_ROLE_KEY,GOOGLE_MAPS_API_KEY=$GOOGLE_MAPS_API_KEY" \
  --quiet

echo -e "${GREEN}✓${NC} Primary scraper deployed"

# Deploy Secondary Scraper
echo -e "\n${YELLOW}Deploying secondary scraper...${NC}"
gcloud functions deploy tstr-scraper-secondary \
  --gen2 \
  --runtime=$RUNTIME \
  --region=$REGION \
  --source=. \
  --entry-point=run_secondary_scraper \
  --trigger-http \
  --allow-unauthenticated \
  --timeout=$TIMEOUT \
  --memory=$MEMORY \
  --set-env-vars="SUPABASE_URL=$SUPABASE_URL,SUPABASE_KEY=$SUPABASE_KEY,SUPABASE_SERVICE_ROLE_KEY=$SUPABASE_SERVICE_ROLE_KEY,GOOGLE_MAPS_API_KEY=$GOOGLE_MAPS_API_KEY" \
  --quiet

echo -e "${GREEN}✓${NC} Secondary scraper deployed"

# Deploy Cleanup Function
echo -e "\n${YELLOW}Deploying cleanup function...${NC}"
gcloud functions deploy tstr-cleanup \
  --gen2 \
  --runtime=$RUNTIME \
  --region=$REGION \
  --source=. \
  --entry-point=run_cleanup \
  --trigger-http \
  --allow-unauthenticated \
  --timeout=$TIMEOUT \
  --memory=$MEMORY \
  --set-env-vars="SUPABASE_URL=$SUPABASE_URL,SUPABASE_KEY=$SUPABASE_KEY,SUPABASE_SERVICE_ROLE_KEY=$SUPABASE_SERVICE_ROLE_KEY" \
  --quiet

echo -e "${GREEN}✓${NC} Cleanup function deployed"

# Get function URLs
echo -e "\n${GREEN}Deployment Complete!${NC}"
echo -e "\nFunction URLs:"
echo "Primary Scraper:   $(gcloud functions describe tstr-scraper-primary --region=$REGION --gen2 --format='value(serviceConfig.uri)')"
echo "Secondary Scraper: $(gcloud functions describe tstr-scraper-secondary --region=$REGION --gen2 --format='value(serviceConfig.uri)')"
echo "Cleanup:           $(gcloud functions describe tstr-cleanup --region=$REGION --gen2 --format='value(serviceConfig.uri)')"

echo -e "\nNext steps:"
echo "1. Test functions manually"
echo "2. Setup Cloud Scheduler (run: ./setup_scheduler.sh)"
echo "3. Monitor logs: gcloud functions logs read tstr-scraper-primary"
