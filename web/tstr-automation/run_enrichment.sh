#!/bin/bash

# Navigate to the automation directory
cd "/media/al/AI_DATA/AI_PROJECTS_SPACE/ACTIVE_PROJECTS/tstr-site-working/web/tstr-automation"

# Run the enrichment script using the fresh virtual environment
# We set a limit of 20 per run to be polite to search engines and stay within safety bounds
./fresh_venv/bin/python3 -u enrich_listings.py >> enrichment_cron.log 2>&1

echo "Enrichment run completed at $(date)" >> enrichment_cron.log
