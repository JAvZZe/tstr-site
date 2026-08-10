#!/usr/bin/env bash
# ShellCheck gate for CHANGED shell scripts only (mirrors lint-changed.sh /
# verify-changed.sh so we never fail on pre-existing debt in _ARCHIVE or
# committed scaffolding). Runs `shellcheck -S warning` on staged files in a
# pre-commit hook, or on the last commit's diff in CI / Cloudflare build.
#
# Exit codes: 0 = clean / nothing to check, 1 = shellcheck found a warning+.
#
# Scope:  *.sh anywhere in the repo, EXCLUDING _ARCHIVE/ (committed historical
# scripts) and broken symlinks (e.g. Link_to_bootstrap_agent.sh).
set -uo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel)"
cd "$REPO_ROOT" || exit 1

if ! command -v shellcheck >/dev/null 2>&1; then
  echo "shellcheck-changed: shellcheck not installed; skipping (install it for local enforcement)." >&2
  # Local grace: don't hard-fail a dev commit if the tool is missing.
  # CI installs it explicitly, so CI never hits this branch.
  exit 0
fi

# Decide the file set: staged (pre-commit hook) or last commit (CI / CF build).
# Use the plumbing `git diff-index` (not porcelain `git diff --cached`) — it is
# deterministic and immune to the index-refresh flakiness that porcelain can hit
# in child processes. In a pre-commit hook the index already holds the staged
# tree, so diff-index --cached HEAD is the authoritative changed-set.
if git diff --cached --quiet 2>/dev/null; then
  BASE="HEAD~1"
  git rev-parse --verify "$BASE" >/dev/null 2>&1 || BASE="HEAD"
  mapfile -d '' FILES < <(git diff --name-only -z "$BASE" HEAD 2>/dev/null || true)
else
  mapfile -d '' FILES < <(git diff-index --cached -z HEAD --name-only 2>/dev/null || true)
fi

CHECK=()
for f in "${FILES[@]:-}"; do
  [[ -n "$f" ]] || continue
  [[ "$f" == _ARCHIVE/* ]] && continue          # skip committed historical scripts
  [[ "$f" == */_ARCHIVE/* ]] && continue
  [[ "$f" == *.sh ]] || continue
  [[ -f "$f" ]] || continue                       # skip deletions + broken symlinks
  CHECK+=("$f")
done

if [[ ${#CHECK[@]} -eq 0 ]]; then
  echo "shellcheck-changed: no active shell scripts in this change — OK."
  exit 0
fi

echo "shellcheck-changed: linting ${#CHECK[@]} changed shell script(s) at warning severity:"
printf '  %s\n' "${CHECK[@]}"

if shellcheck -S warning "${CHECK[@]}"; then
  echo "shellcheck-changed: PASS"
  exit 0
else
  echo "shellcheck-changed: FAIL — fix the warning(s) above (or justify with '# shellcheck disable=SCxxxx')." >&2
  exit 1
fi
