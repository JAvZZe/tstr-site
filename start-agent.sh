#!/bin/bash
# TSTR.site Agent Bootstrap Script
# Initializes agent with complete project context

echo "🚀 Initializing TSTR.site Agent Context..."

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# First: Global bootstrap (MANDATORY for all agents)
echo "📋 Step 1: Global system bootstrap..."
cd "/media/al/AI_DATA/AI_PROJECTS_SPACE" && ./bootstrap_global.sh

# Second: Project-specific bootstrap
echo "📋 Step 2: Project-specific context..."
cd "$SCRIPT_DIR" && ./bootstrap.sh TSTR.directory

echo "✅ Complete agent context loaded successfully"
echo "📋 Available commands:"
echo "  - ./start-agent.sh    # This script"
echo "  - ./monitoring/daily_check.sh  # Health monitoring"
echo "  - python3 management/status_validator.py report  # System validation"
echo ""
echo "Ready for TSTR.site development work."
