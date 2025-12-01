#!/bin/bash
# Deploy updated scraper to OCI

echo "🚀 Deploying TSTR.site scraper updates to OCI"

# OCI connection details
OCI_HOST="84.8.139.90"
OCI_USER="opc"
SSH_KEY="/media/al/1TB_AI_ARCH/AI_PROJECTS_ARCHIVE/Oracle Cloud Machines/avz Oracle Linux 9 pvt ssh-key-2025-10-25.key"
REMOTE_DIR="/home/opc/tstr-scraper"

# Files to deploy
FILES_TO_DEPLOY=(
    "main_scraper.py"
    "run_scraper.py"
    "scrapers/oil_gas_playwright.py"
    "scrapers/a2la_materials.py"
    "scrapers/tni_environmental.py"
    "requirements.txt"
)

echo "📦 Copying files to OCI..."
for file in "${FILES_TO_DEPLOY[@]}"; do
    if [ -f "$file" ]; then
        echo "Copying $file..."
        scp -i "$SSH_KEY" "$file" "$OCI_USER@$OCI_HOST:$REMOTE_DIR/"
    else
        echo "Warning: $file not found locally"
    fi
done

echo "🔧 Installing dependencies on OCI..."
ssh -i "$SSH_KEY" "$OCI_USER@$OCI_HOST" "cd $REMOTE_DIR && pip install -r requirements.txt"

echo "🎭 Installing Playwright browsers..."
ssh -i "$SSH_KEY" "$OCI_USER@$OCI_HOST" "cd $REMOTE_DIR && python3 -m playwright install chromium"

echo "✅ Deployment completed!"
echo "📋 Next steps:"
echo "1. Test the scraper manually: ssh -i '$SSH_KEY' $OCI_USER@$OCI_HOST 'cd $REMOTE_DIR && python3 run_scraper.py --dry-run'"
echo "2. Check cron job is still active: ssh -i '$SSH_KEY' $OCI_USER@$OCI_HOST 'crontab -l'"
echo "3. Monitor tomorrow's automated run"