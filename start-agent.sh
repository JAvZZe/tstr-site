#!/bin/bash
# TSTR.site Agent Bootstrap Script
# Initializes agent with complete project context

echo "🚀 Initializing TSTR.site Agent Context..."

# Run the bootstrap script
./bootstrap.sh TSTR-site

echo "✅ Agent context loaded successfully"
echo "📋 Available commands:"
echo "  - ./start-agent.sh    # This script"
echo "  - ./monitoring/daily_check.sh  # Health monitoring"
echo "  - python3 management/status_validator.py report  # System validation"
echo ""
echo "Ready for TSTR.site development work."