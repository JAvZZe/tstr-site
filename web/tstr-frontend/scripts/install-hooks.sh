#!/usr/bin/env bash
# Install local git hooks that enforce the verification gate (Part A + B)
# before an agent can push frontend changes.
#
# Installs (symlinks into .git/hooks):
#   pre-push  -> runs lint-changed.sh + verify-changed.sh on the push's diff
#
# Run once: bash scripts/install-hooks.sh
# Safe to re-run; it only (re)links and never overwrites unrelated hooks.
set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel)"
HOOKS_DIR="$REPO_ROOT/.git/hooks"
SCRIPT_DIR="$REPO_ROOT/web/tstr-frontend/scripts"
mkdir -p "$HOOKS_DIR"

# pre-push: lint + security-scan the commits being pushed.
cat > "$HOOKS_DIR/pre-push" <<'EOF'
#!/usr/bin/env bash
# Enforce lint + security scan on pushed frontend changes (Part A + B).
# Reads the to-be-pushed range from stdin (local ref, local sha, remote ref, remote sha).
set -uo pipefail
FRONTEND_DIR="$(git rev-parse --show-toplevel)/web/tstr-frontend"
read -r LOCAL_REF LOCAL_SHA REMOTE_REF REMOTE_SHA
# If pushing a branch (not delete), scan LOCAL_SHA vs its merge-base with remote.
if [[ "$REMOTE_SHA" =~ ^0+$ ]]; then
  RANGE="$LOCAL_SHA"
else
  MERGE_BASE="$(git merge-base "$REMOTE_SHA" "$LOCAL_SHA" 2>/dev/null || echo "$REMOTE_SHA")"
  RANGE="${MERGE_BASE}..${LOCAL_SHA}"
fi
# Temporarily stage the to-be-pushed diff so the changed-file scripts see it.
git diff --name-only "$RANGE" | sed 's#^#'"$PWD"'/#' >/dev/null 2>&1
echo "pre-push: running verification gate on $RANGE"
( cd "$FRONTEND_DIR" && bash scripts/lint-changed.sh ) || { echo "pre-push ABORTED: lint failed"; exit 1; }
( cd "$FRONTEND_DIR" && bash scripts/verify-changed.sh ) || { echo "pre-push ABORTED: security scan failed"; exit 1; }
echo "pre-push: verification gate passed"
exit 0
EOF
chmod +x "$HOOKS_DIR/pre-push"

echo "Installed pre-push hook -> $HOOKS_DIR/pre-push"
echo "It runs lint-changed.sh + verify-changed.sh before every push."
echo "To bypass in an emergency (not recommended): git push --no-verify"
