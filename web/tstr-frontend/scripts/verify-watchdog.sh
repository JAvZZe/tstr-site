#!/usr/bin/env bash
# Verification watchdog (Part B2) — the dedicated, scheduled half of the
# verification agent. Detects frontend commits landed since the last run and
# runs the static security scan (verify-changed.sh) on each, reporting any
# hits. This guarantees no agent-produced commit lands without at least the
# machine verification being logged and surfaced to the owner.
#
# The LLM independent reviewer (requesting-code-review skill) is layered on top
# by the Hermes agent before it commits; this watchdog is the unattended safety
# net that catches anything that slipped through.
#
# State is kept in .verification-watchdog.state (last seen commit sha).
set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FRONTEND_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
REPO_ROOT="$(git -C "$FRONTEND_DIR" rev-parse --show-toplevel)"
STATE_FILE="$REPO_ROOT/.verification-watchdog.state"

cd "$REPO_ROOT"

LAST_SHA="$(cat "$STATE_FILE" 2>/dev/null || echo "")"
if [[ -z "$LAST_SHA" ]] || ! git rev-parse --verify "$LAST_SHA" >/dev/null 2>&1; then
  # First run: only look at the most recent commit to avoid a huge backfill.
  LAST_SHA="$(git rev-parse HEAD~1 2>/dev/null || git rev-parse HEAD)"
fi

# New frontend-related commits since LAST_SHA.
NEW_COMMITS="$(git rev-list --reverse "$LAST_SHA..HEAD" -- "$FRONTEND_DIR" 2>/dev/null)"
if [[ -z "$NEW_COMMITS" ]]; then
  echo "verification-watchdog: no new frontend commits since $LAST_SHA — OK."
  echo "$LAST_SHA" > "$STATE_FILE"
  exit 0
fi

echo "verification-watchdog: reviewing $(echo "$NEW_COMMITS" | wc -l) new frontend commit(s):"
ALERTS=0
while IFS= read -r c; do
  [[ -z "$c" ]] && continue
  SUBJECT="$(git log -1 --format='%h %s' "$c")"
  echo "  - $SUBJECT"
  # Run verify-changed logic on this single commit's diff.
  RANGE="${c}^..${c}"
  mapfile -d '' FILES < <(git diff --name-only -z "$RANGE" 2>/dev/null || true)
  HITS=""
  for f in "${FILES[@]:-}"; do
    [[ -n "$f" ]] || continue
    [[ "$f" == web/tstr-frontend/* ]] || continue
    ADDED="$(git diff "$RANGE" -- "$f" | grep '^+' | grep -v '^+++' )"
    [[ -z "$ADDED" ]] && continue
    if printf '%s\n' "$ADDED" | grep -Ei "(api_key|apikey|secret|password|passwd|token|client_secret)\s*[:=]\s*['\"][^'\"]{6,}['\"]" >/dev/null 2>&1; then
      HITS+="    [SECURITY:hardcoded-secret] $f"$'\n'
    fi
    if printf '%s\n' "$ADDED" | grep -Ei "os\.system\(|subprocess[^)]*shell\s*=\s*True|\beval\(|\bexec\(|\bpickle\.loads?\(" >/dev/null 2>&1; then
      HITS+="    [SECURITY:injection/exec] $f"$'\n'
    fi
    if printf '%s\n' "$ADDED" | grep -Ei "execute\(\s*f[\"']|execute\([^)]*\.format\(.*(SELECT|INSERT|UPDATE|DELETE)" >/dev/null 2>&1; then
      HITS+="    [SECURITY:sql-injection] $f"$'\n'
    fi
  done
  if [[ -n "$HITS" ]]; then
    echo "    SECURITY PATTERN(S) DETECTED:" >&2
    printf '%s' "$HITS" >&2
    ALERTS=1
  fi
done <<< "$NEW_COMMITS"

echo "$LAST_SHA" > "$STATE_FILE"

if [[ $ALERTS -eq 1 ]]; then
  echo "verification-watchdog: ALERT — security pattern(s) found in new commits." >&2
  exit 1
fi
echo "verification-watchdog: all new commits passed static verification."
# Advance the marker to HEAD so the next run starts after these commits.
git rev-parse HEAD > "$STATE_FILE"
exit 0
