#!/bin/bash

# Source this file to get quick aliases
# usage: source management/quick_actions.sh

PROJECT_ROOT="$(dirname "$(dirname "${BASH_SOURCE[0]}")")"
MANAGER="$PROJECT_ROOT/management/status_manager.py"

# Default agent name (can be overridden)
export AGENT_NAME="${AGENT_NAME:-OpenCode}"

function tstr_log() {
    if [ "$#" -lt 2 ]; then
        echo "Usage: tstr_log \"Action description\" \"Result description\""
        return 1
    fi
    python3 "$MANAGER" log --agent "$AGENT_NAME" --action "$1" --result "$2"
}

function tstr_update() {
    python3 "$MANAGER" update --agent "$AGENT_NAME"
}

echo "✅ TSTR.site Quick Actions Loaded:"
echo "  tstr_log \"Action\" \"Result\"  -> Log to .ai-session.md"
echo "  tstr_update                 -> Update PROJECT_STATUS.md timestamp"
