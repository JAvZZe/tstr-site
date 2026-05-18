# Agent Handoff: Security And Credential Remediation

Date: 2026-05-13
Project: TSTR.directory
Repo: `JAvZZe/tstr-site`
Working directory: `/media/al/AI_DATA/AI_PROJECTS_SPACE/ACTIVE_PROJECTS/tstr-site-working`

## Hard Rules

- Do not print, copy, commit, or summarize secret values.
- Do not inspect raw alert JSON unless you can guarantee no secret values are emitted.
- Use alert numbers, provider names, file paths, variable names, and redacted metadata only.
- Do not use MCP/Gemini for this handoff; Gemini is unavailable.
- Prefer local shell, Opencode, Qwen, or bounded subagents.
- Treat public Git history as compromised for any exposed credential.

## Required Startup

Run the project protocol first:

```bash
cd "/media/al/AI_DATA/AI_PROJECTS_SPACE" && ./bootstrap_global.sh
cd "/media/al/AI_DATA/AI_PROJECTS_SPACE/ACTIVE_PROJECTS/tstr-site-working"
git branch -a --sort=-authordate
./start-agent.sh
```

Read:

- `AGENTS.md`
- `CODEX.md`
- `PROJECT_STATUS.md`
- `plans/security/GITHUB_SECURITY_AUDIT.md`
- `plans/security/CREDENTIAL_ROTATION_RUNBOOK.md`
- `plans/security/GEMINI_FILENAME_ONLY_SECRET_INVENTORY_2026-05-13.md`

## Current Status

Incident phase: local hardening in progress. Credential/provider verification is not complete.

Local fixes applied by Codex:

- Removed a hardcoded instrumentation API key from `instrumentation.node.ts`; code now uses `SYN_CAUSE_API_KEY`.
- Replaced vulnerable substring host checks in instrumentation filtering with exact URL host checks.
- Removed exception details from frontend API JSON responses.
- Removed outward `str(e)` responses from Python scraper HTTP handlers.
- Disabled local Flask debug defaults and bound local test servers to `127.0.0.1`.
- Reduced sensitive business/provider names and response bodies in flagged logs.
- Added least-privilege workflow permissions to CI and Playwright workflows.
- Added `.gitignore` rules for raw GitHub alert exports.
- Updated `PROJECT_STATUS.md` to v2.6.4 security-hardening status.

Verification already run:

- `python3 -m py_compile web/tstr-automation/main.py web/tstr-automation/cloud_function_main.py web/tstr-automation/backfill_a2la.py web/tstr-automation/import_csv.py web/tstr-automation/scraper.py`
- `git diff --check`
- Local `rg` pattern check for the fixed CodeQL-triggering patterns.
- `npm run build` in `web/tstr-frontend` passed.

Build warnings observed but not fixed in this pass:

- stale browser baseline/caniuse data
- unresolved `/images/standards-bg.jpg`
- `getStaticPaths()` ignored on dynamic routes
- CSS warning involving literal `${p.color}`

## Current Working Tree Notes

There are unrelated pre-existing or separate-session changes. Do not revert them unless the human owner explicitly asks.

Known status at handoff time included:

- Modified session files: `.ai-session.md`, `.frolic-session.json`
- Modified security/code files from this pass
- Modified `PROJECT_STATUS.md`
- Modified `web/tstr-automation/requirements.txt` with dependency bumps
- Deleted `archives/handoffs/*` files and untracked `_ARCHIVE/archives/` from an existing archive move
- Untracked `plans/security/` incident docs

Raw GitHub alert exports are now ignored by `.gitignore`:

- `secret_alerts.json`
- `secret_summary.tsv`
- `code_alerts.json`
- `code_summary.tsv`
- `dependabot_alerts.json`
- `dependabot_summary.tsv`

If these files exist locally, treat them as sensitive artifacts and do not commit them.

## Credentials To Rotate Or Verify

### Rotate Now

`SYN_CAUSE_API_KEY`

- Reason: hardcoded in tracked `instrumentation.node.ts` before this pass.
- Action: create a new key, store it only in approved secret stores, revoke the old key, and verify the old key fails.

### Rotate Unless Already Rotated After Alert Creation

Google Cloud / Google API keys

- Alert classes include Google API keys and a GCP API key bound to a service account.
- Create separate restricted keys for browser Maps, backend Maps/geocoding, and Gemini if applicable.
- Restrict by HTTP referrer, OCI egress IP, and required APIs.

GitHub Personal Access Tokens

- Revoke exposed PATs.
- Refresh local `gh` auth if it used the same token family.
- Review GitHub Actions, Dependabot, repo, environment, and organization secrets.

OpenRouter API keys

- Revoke exposed keys.
- Update Cloudflare, OCI, GitHub Actions, and local env stores if used.

PayPal credentials

- Historical/large files were flagged as possibly containing PayPal material.
- Rotate or verify the exposed client/webhook credentials are no longer valid.

### Supabase: Verify Before Re-Rotating

The human owner says Supabase credentials were rotated some weeks before this handoff.

Do not blindly rotate Supabase again unless current production values still match an alert or a provider confirms active exposure.

Required verification:

- Old Supabase service role keys fail.
- Old Supabase PATs fail.
- Old MCP tokens fail.
- Old secret keys fail.
- Cloudflare Pages production and preview env vars use rotated values.
- OCI scraper env files or systemd environments use rotated values.
- GitHub Actions secrets use rotated values.
- Supabase Edge Function secrets use rotated values.
- Local `.env` files use rotated values.
- GitHub secret scanning alerts are closed only after revocation/invalidity evidence exists.

## Next Recommended Work

1. Commit the local hardening changes separately from unrelated archive/session churn.
2. Verify current GitHub secret scanning alerts by alert number without printing secret values.
3. Build a redacted rotation evidence table:

```markdown
| Alert | Provider | Path | Credential Class | Rotated/Verified | Evidence Location | Owner | Status |
|---|---|---|---|---|---|---|---|
```

4. Complete provider/dashboard rotations or invalidity checks.
5. Only after rotation/verification, redact tracked historical files identified in `GEMINI_FILENAME_ONLY_SECRET_INVENTORY_2026-05-13.md`.
6. Close GitHub alerts only with evidence that old credentials are revoked or invalid.

## Do Not Do

- Do not close secret-scanning alerts before rotation/invalidity evidence.
- Do not paste secrets into handoff docs, commits, issues, tickets, or chat.
- Do not delete alert exports with destructive commands unless the human owner explicitly requests cleanup.
- Do not revert unrelated archive/session/status changes.
