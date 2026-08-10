---
name: tstr-secret-scanner
description: Reusable secret-exposure scanner + prevention agent for TSTR.directory. Use when (a) auditing the repo for leaked credentials, (b) before committing/secreting code that may contain keys, (c) after a suspected leak, or (d) to wire secret prevention into CI/hooks. Catches Supabase service-role/PAT, Google/Gemini, Resend, OpenAI/Stripe/OpenRouter, LinkedIn, Stitch, PayPal, GitHub/GitLab PATs, JWTs.
---

# tstr-secret-scanner

Secret-exposure scanner and prevention agent for TSTR.directory. The repo has a
history of plaintext credentials committed to docs, configs, agent defs, and
reference files (19 OPEN GitHub secret-scanning alerts as of 2026-08-10, some
dating to 2025-10). This agent finds them, redacts them in the working tree,
and wires prevention so they can't be re-committed.

## Tooling (already in repo)
- `scripts/secret_scan.py` — pattern scanner.
  - `python3 scripts/secret_scan.py --staged`   # staged files (used by pre-commit)
  - `python3 scripts/secret_scan.py --all`      # whole working tree
  - `python3 scripts/secret_scan.py --history`  # git history blobs (report only)
  - Exit 1 = secrets found (in --staged/--all); 0 = clean.
- `scripts/pre-commit.hook` — canonical hook (secret scan + lint, scoped to staged files).
- `scripts/install-hooks.sh` — copies the canonical hook into `.git/hooks/`.
  Run once per clone: `bash scripts/install-hooks.sh`

## When to run
1. **Proactive**: run `--all` on any session touching secrets/credentials or auth code.
2. **Before commit**: the pre-commit hook runs `--staged` automatically; do not bypass.
3. **After a leak report**: run `--all` and `--history`, redact, then require ROTATION.
4. **Periodic**: monthly `--history` to confirm old alerts stay resolved.

## Redaction rules (Pareto + least-surprise)
- Redact the VALUE, keep the KEY NAME and context (e.g. `SUPABASE_SERVICE_ROLE_KEY=[REDACTED]`).
- Use exact markers: `[REDACTED Supabase service role]`, `[REDACTED Gemini]`,
  `[REDACTED GitHub PAT]`, `[REDACTED Stitch]`, `[REDACTED PayPal]`, etc.
- NEVER paste the real secret into chat, commits, issues, or logs.
- **Do NOT redact `.env` / `.dev.vars`** — those are git-ignored local dev secrets by design
  (see AGENTS.md). The scanner skips git-ignored files, so they never reach the hook.
- `secret_alerts.json` is a copy of GitHub alert metadata; redact its `secret` field values.

## CRITICAL: redaction ≠ remediated
Redacting a file does NOT close a GitHub secret-scanning alert. The key may still be
in git HISTORY and in the live runtime (Cloudflare/OCI/.env). Per
`plans/security/GITHUB_SECURITY_AUDIT.md` and `CREDENTIAL_ROTATION_RUNBOOK.md`:
- **Rotate every exposed credential** in its provider dashboard.
- Update every surface: Cloudflare Pages env, OCI .env, GitHub Actions secrets,
  Supabase Edge Function secrets, local .env.
- Only then mark the alert resolved/revoked.
- Git history cannot be "cleaned" without a force-push/rewrite — coordinate with the owner.

## False-positive guard
Scanner minimums match REAL key lengths (Google 39, Supabase PAT ~40, GitHub PAT ~36,
Stitch ~60, OpenAI/Stripe ~48). Documentation placeholders like `AIzaSy...L96k`
(only prefix + last 4) won't trigger. If you see a flagged placeholder that is a real
full key, lower the threshold only with justification.

## Escalation
If a secret is found in the COMMITTED tree (not git-ignored) and the push was already
attempted, GitHub push protection blocks it — do NOT use the unblock URL. Redact, then
squash so the secret is absent from every commit in the push.
