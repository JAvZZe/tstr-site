#!/bin/bash

# TSTR.SITE - Cloud Scheduler Setup Script
# Creates automated schedules for scrapers

set -e

echo "=================================="
echo "TSTR.SITE Scheduler Setup"
echo "=================================="

PROJECT_ID="tstr-automation"
REGION="us-central1"
TIMEZONE="Asia/Singapore"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Get function URLs
PRIMARY_URL=$(gcloud functions describe tstr-scraper-primary --region=$REGION --gen2 --format='value(serviceConfig.uri)')
SECONDARY_URL=$(gcloud functions describe tstr-scraper-secondary --region=$REGION --gen2 --format='value(serviceConfig.uri)')
CLEANUP_URL=$(gcloud functions describe tstr-cleanup --region=$REGION --gen2 --format='value(serviceConfig.uri)')

# Create Daily Primary Scraper Job
echo -e "${YELLOW}Creating daily primary scraper job...${NC}"
gcloud scheduler jobs create http tstr-daily-primary \
  --location=$REGION \
  --schedule="0 2 * * *" \
  --uri="$PRIMARY_URL" \
  --http-method=GET \
  --time-zone="$TIMEZONE" \
  --description="Daily primary scraper - runs at 2am Singapore time" \
  --quiet || echo "Job already exists, updating..."

gcloud scheduler jobs update http tstr-daily-primary \
  --location=$REGION \
  --schedule="0 2 * * *" \
  --uri="$PRIMARY_URL" \
  --quiet

echo -e "${GREEN}✓${NC} Daily primary scraper scheduled (2am daily)"

# Create Weekly Secondary Scraper Job
echo -e "${YELLOW}Creating weekly secondary scraper job...${NC}"
gcloud scheduler jobs create http tstr-weekly-secondary \
  --location=$REGION \
  --schedule="0 3 * * 0" \
  --uri="$SECONDARY_URL" \
  --http-method=GET \
  --time-zone="$TIMEZONE" \
  --description="Weekly secondary scraper - runs Sunday 3am" \
  --quiet || echo "Job already exists, updating..."

gcloud scheduler jobs update http tstr-weekly-secondary \
  --location=$REGION \
  --schedule="0 3 * * 0" \
  --uri="$SECONDARY_URL" \
  --quiet

echo -e "${GREEN}✓${NC} Weekly secondary scraper scheduled (Sunday 3am)"

# Create Monthly Cleanup Job
echo -e "${YELLOW}Creating monthly cleanup job...${NC}"
gcloud scheduler jobs create http tstr-monthly-cleanup \
  --location=$REGION \
  --schedule="0 4 1 * *" \
  --uri="$CLEANUP_URL" \
  --http-method=POST \
  --message-body='{"mode":"2"}' \
  --headers="Content-Type=application/json" \
  --time-zone="$TIMEZONE" \
  --description="Monthly database cleanup - runs 1st of month at 4am" \
  --quiet || echo "Job already exists, updating..."

gcloud scheduler jobs update http tstr-monthly-cleanup \
  --location=$REGION \
  --schedule="0 4 1 * *" \
  --uri="$CLEANUP_URL" \
  --message-body='{"mode":"2"}' \
  --quiet

echo -e "${GREEN}✓${NC} Monthly cleanup scheduled (1st of month, 4am)"

echo -e "\n${GREEN}Scheduler Setup Complete!${NC}"
echo -e "\nScheduled Jobs:"
echo "1. Primary Scraper:   Daily at 2:00 AM (Singapore)"
echo "2. Secondary Scraper: Sunday at 3:00 AM (Singapore)"
echo "3. Database Cleanup:  1st of month at 4:00 AM (Singapore)"

echo -e "\nManage jobs:"
echo "List:    gcloud scheduler jobs list --location=$REGION"
echo "Run now: gcloud scheduler jobs run tstr-daily-primary --location=$REGION"
echo "Pause:   gcloud scheduler jobs pause tstr-daily-primary --location=$REGION"
echo "Resume:  gcloud scheduler jobs resume tstr-daily-primary --location=$REGION"
