#!/bin/bash
# TSTR.site Monitoring Script
# Run daily health checks and log results

echo "=== TSTR.site Health Check $(date) ==="

# System health
echo "1. System Integrity:"
python3 management/status_validator.py report

echo -e "\n2. Site Accessibility:"
curl -s -o /dev/null -w "HTTP Status: %{http_code}\n" https://tstr.site/

echo -e "\n3. Build Verification:"
cd web/tstr-frontend
npm run build > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ Build successful"
else
    echo "❌ Build failed"
fi

echo -e "\n4. Scraper Status Check:"
# Check if OCI scraper is running (placeholder - would need SSH access)
echo "OCI Status: Check manually via SSH"
echo "Local Status: Check systemd logs"

echo -e "\n=== End Health Check ==="