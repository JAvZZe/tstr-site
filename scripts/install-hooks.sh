#!/bin/bash
# install-hooks.sh — wire TSTR's local git hooks into a fresh clone.
# Run once after cloning:  bash scripts/install-hooks.sh
# Copies .git/hooks/pre-commit from the repo's canonical hook template.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
HOOK_SRC="$ROOT/scripts/pre-commit.hook"
HOOK_DST="$ROOT/.git/hooks/pre-commit"

if [ ! -f "$HOOK_SRC" ]; then
  echo "ERROR: canonical hook not found at $HOOK_SRC" >&2
  exit 1
fi

mkdir -p "$(dirname "$HOOK_DST")"
cp "$HOOK_SRC" "$HOOK_DST"
chmod +x "$HOOK_DST"
echo "Installed pre-commit hook -> $HOOK_DST"
echo "Run 'python3 scripts/secret_scan.py --all' to scan the working tree."
echo "Run 'python3 scripts/secret_scan.py --history' to list secrets in git history (rotate those)."
