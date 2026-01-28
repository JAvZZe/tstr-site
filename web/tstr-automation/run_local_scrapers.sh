#!/bin/bash

# tstr.directory Local Scraper Automation Script
# Runs heavy-duty scrapers locally with 40GB RAM available

set -e

LOG_FILE="/media/al/AI_SSD/AI_PROJECTS_SPACE/ACTIVE_PROJECTS/TSTR-site/tstr-site-working/web/tstr-automation/local_scraper.log"
SCRIPT_DIR="/media/al/AI_SSD/AI_PROJECTS_SPACE/ACTIVE_PROJECTS/TSTR-site/tstr-site-working/web/tstr-automation"

echo "$(date): Starting local scraper automation" >> "$LOG_FILE"

cd "$SCRIPT_DIR"

# Test basic functionality first
echo "$(date): Testing scraper environment..." >> "$LOG_FILE"
python3 -c "import sys; print(f'Python version: {sys.version}')">> "$LOG_FILE" 2>&1

# Run Oil & Gas scraper (heavy processing, browser automation)
echo "$(date): Running Oil & Gas scraper..." >> "$LOG_FILE"
python3 scrapers/oil_gas_playwright.py >> "$LOG_FILE" 2>&1

# Run other heavy scrapers as needed
# python3 scrapers/a2la_materials.py >> "$LOG_FILE" 2>&1

echo "$(date): Local scraper automation completed" >> "$LOG_FILE"