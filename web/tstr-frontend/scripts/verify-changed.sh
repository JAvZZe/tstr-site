#!/usr/bin/env bash
# Independent static security scan on CHANGED frontend source files.
# This is the machine-enforceable half of the verification gate (Part B).
# It does NOT replace the LLM independent reviewer (requesting-code-review
# skill) — it catches the cheap, high-confidence issues prettier can't:
# hardcoded secrets, shell/SQL injection, unsafe eval/exec, pickle.loads.
#
# Exit codes: 0 = clean / nothing to check, 1 = a security pattern matched.
#
# Paths: git emits repo-root-relative names. We collect from repo root and
# scope to the frontend subtree, like lint-changed.sh.
set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FRONTEND_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
REPO_ROOT="$(git -C "$FRONTEND_DIR" rev-parse --show-toplevel)"
FRONTEND_REL="${FRONTEND_DIR#"$REPO_ROOT"/}"

cd "$REPO_ROOT"

if git -C "$REPO_ROOT" diff --cached --quiet 2>/dev/null; then
  BASE="HEAD~1"
  git -C "$REPO_ROOT" rev-parse --verify "$BASE" >/dev/null 2>&1 || BASE="HEAD"
  mapfile -d '' FILES < <(git -C "$REPO_ROOT" diff --name-only -z "$BASE" HEAD 2>/dev/null || true)
else
  mapfile -d '' FILES < <(git -C "$REPO_ROOT" diff --cached --name-only -z 2>/dev/null || true)
fi

EXT_RE='\.(astro|js|jsx|ts|tsx|json|css|md)$'
SRC=()
for f in "${FILES[@]:-}"; do
  [[ -n "$f" ]] || continue
  [[ "$f" == "$FRONTEND_REL"/* ]] || continue
  [[ -f "$f" ]] || continue
  [[ "$f" =~ $EXT_RE ]] || continue
  SRC+=("${f#"$FRONTEND_REL"/}")
done

if [[ ${#SRC[@]} -eq 0 ]]; then
  echo "verify-changed: no frontend source files to scan in this change — OK."
  exit 0
fi

echo "verify-changed: scanning ${#SRC[@]} changed file(s) for security patterns:"

# Patterns: only scan ADDED/CHANGED lines (prefix '+'), ignore context.
# Each entry: <label>|<grep -E regex on the added line>
PATTERNS=(
  "hardcoded-secret|(api_key|apikey|secret|password|passwd|token|client_secret)\s*[:=]\s*['\"][^'\"]{6,}['\"]"
  "shell-injection|os\.system\(|subprocess[^)]*shell\s*=\s*True"
  "eval-exec|\beval\(|\bexec\("
  "pickle|\bpickle\.loads?\("
  "sql-injection|execute\(\s*f[\"']|execute\([^)]*\.format\(.*(SELECT|INSERT|UPDATE|DELETE)"
)

FOUND=0
for f in "${SRC[@]}"; do
  # Extract added lines for this file from the diff.
  if git -C "$REPO_ROOT" diff --cached --quiet 2>/dev/null; then
    ADDED="$(git -C "$REPO_ROOT" diff "$BASE" HEAD -- "$FRONTEND_REL/$f" | grep '^+' | grep -v '^+++' )"
  else
    ADDED="$(git -C "$REPO_ROOT" diff --cached -- "$FRONTEND_REL/$f" | grep '^+' | grep -v '^+++' )"
  fi
  [[ -z "$ADDED" ]] && continue
  for pat in "${PATTERNS[@]}"; do
    label="${pat%%|*}"
    re="${pat#*|}"
    if printf '%s\n' "$ADDED" | grep -Ei "$re" >/dev/null 2>&1; then
      echo "  [SECURITY:$label] $f" >&2
      FOUND=1
    fi
  done
done

if [[ $FOUND -eq 1 ]]; then
  echo "verify-changed: FAIL — security pattern(s) matched in added lines." >&2
  echo "Review the flagged lines; if a false positive, justify and re-run." >&2
  exit 1
fi

echo "verify-changed: PASS (no security patterns in added lines)"
exit 0
