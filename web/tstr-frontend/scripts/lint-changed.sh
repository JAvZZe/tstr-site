#!/usr/bin/env bash
# Enforce Prettier formatting on CHANGED frontend source files only.
# Never lints the whole tree, so pre-existing formatting debt (116 files today)
# can't break the live Cloudflare build. Works both in CI/CF build (committed
# diff vs HEAD~1) and as a pre-commit hook (staged diff).
#
# Exit codes: 0 = clean / nothing to check, 1 = formatting violation.
#
# Paths: git emits repo-root-relative names. We collect them from the repo root
# but run Prettier from the frontend dir so its local plugins
# (prettier-plugin-astro, prettier-plugin-tailwindcss) and .prettierrc resolve.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FRONTEND_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
REPO_ROOT="$(git -C "$FRONTEND_DIR" rev-parse --show-toplevel)"
FRONTEND_REL="${FRONTEND_DIR#"$REPO_ROOT"/}"

cd "$REPO_ROOT"

PRETTIER_BIN="$FRONTEND_DIR/node_modules/.bin/prettier"
if [[ ! -x "$PRETTIER_BIN" ]]; then
  echo "lint-changed: prettier not found at $PRETTIER_BIN (run npm install first)" >&2
  exit 1
fi

# Decide the file set: staged (pre-commit hook) or last commit (CI / CF build).
# NOTE: git --name-only -z emits NUL-separated names. A command substitution
# ("$(...)") strips NULs, so feed -z output straight into mapfile -d ''.
if git -C "$REPO_ROOT" diff --cached --quiet 2>/dev/null; then
  # Nothing staged -> CI / Cloudflare build mode: lint the last commit's diff.
  BASE="HEAD~1"
  git -C "$REPO_ROOT" rev-parse --verify "$BASE" >/dev/null 2>&1 || BASE="HEAD"
  mapfile -d '' FILES < <(git -C "$REPO_ROOT" diff --name-only -z "$BASE" HEAD 2>/dev/null || true)
else
  # Staged changes -> pre-commit hook mode: lint exactly what's staged.
  mapfile -d '' FILES < <(git -C "$REPO_ROOT" diff --cached --name-only -z 2>/dev/null || true)
fi

# Filter to frontend source extensions + files under the frontend subtree + exist.
EXT_RE='\.(astro|js|jsx|ts|tsx|json|css|md)$'
CHECK=()
for f in "${FILES[@]:-}"; do
  [[ -n "$f" ]] || continue
  [[ "$f" == "$FRONTEND_REL"/* ]] || continue   # scope to frontend subtree
  [[ -f "$f" ]] || continue                      # skip deletions
  [[ "$f" =~ $EXT_RE ]] || continue              # only file types we format
  CHECK+=("${f#"$FRONTEND_REL"/}")              # frontend-relative for prettier
done

if [[ ${#CHECK[@]} -eq 0 ]]; then
  echo "lint-changed: no frontend source files to check in this change — OK."
  exit 0
fi

echo "lint-changed: checking ${#CHECK[@]} changed file(s):"
printf '  %s\n' "${CHECK[@]}"

# Run Prettier from the frontend dir so plugins + config resolve, but pass the
# repo-root-relative paths (they are valid from REPO_ROOT which is our cwd).
if ( cd "$FRONTEND_DIR" && exec "$PRETTIER_BIN" --check "${CHECK[@]}" ); then
  echo "lint-changed: PASS"
  exit 0
else
  echo "lint-changed: FAIL — the file(s) above are not Prettier-formatted." >&2
  echo "Fix locally with: (cd \"$FRONTEND_DIR\" && ./node_modules/.bin/prettier --write <file>)" >&2
  exit 1
fi
