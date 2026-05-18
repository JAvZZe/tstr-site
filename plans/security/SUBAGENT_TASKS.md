# Subagent Tasks For Credential Exposure Incident

## Coordination Rules

- Do not print secret values.
- Do not paste raw scanner output containing secrets.
- Use filenames, alert numbers, provider types, paths, and owner names only.
- Keep outputs small enough for review and commit.
- Stop and report blockers before changing production credentials.

## Gemini CLI: Filename-Only Secret Inventory

### Objective

Create a filename-only inventory of tracked files that may contain secrets or sensitive credential references.

### Inputs

- `plans/security/SECRET_EXPOSURE_AUDIT_FOR_GEMINI.md`
- Repository working tree

### Output

- Markdown table with file path, reason codes, recommended owner, and notes.
- No secret values.
- No full matching lines.

### Acceptance Criteria

- Every entry is actionable by cleanup owner.
- Output can be committed safely.
- Gemini explicitly states that no secret values are included.

## Security Subagent: GitHub Alert Summary

### Objective

Summarize all GitHub secret scanning, code scanning, and Dependabot alerts.

### Inputs

- `plans/security/GITHUB_SECURITY_AUDIT.md`
- GitHub CLI access to `JAvZZe/tstr-site`

### Output

Table columns:

| Alert | Category | Severity | Path | State | Owner | Required Action |
|---|---|---|---|---|---|---|

### Acceptance Criteria

- Includes all open secret scanning alerts.
- Includes all open high and medium code scanning alerts.
- Includes open Dependabot alerts.
- Uses alert numbers and paths, not secret values.

## Infra Subagent: Secret Surface Map

### Objective

Map each rotated secret to every deployment and runtime surface that must be updated.

### Inputs

- `plans/security/CREDENTIAL_ROTATION_RUNBOOK.md`
- Cloudflare Pages environment names
- OCI scraper environment locations
- GitHub Actions secret names
- Supabase Edge Function secret names
- Local `.env` variable names

### Output

Table columns:

| Secret Name | Service | Cloudflare | OCI | GitHub Actions | Supabase | Local Env | Owner | Status |
|---|---|---|---|---|---|---|---|---|

### Acceptance Criteria

- Covers Google Cloud, GitHub, Supabase, OpenRouter, and Cloudflare credentials.
- Uses variable names only.
- Identifies missing owners or unknown stores as blockers.

## Cleanup Subagent: Redaction And Prevention Controls

### Objective

Redact tracked docs/configs and add prevention controls after credentials have been rotated.

### Inputs

- Gemini filename-only inventory
- GitHub alert summary
- Rotation completion confirmation

### Scope

- Documentation
- `_ARCHIVE/`
- `.gitnexus/`
- MCP config files
- Management references
- GitHub workflows
- `.gitignore` and example env files

### Required Changes

- Replace literal secret values with placeholders.
- Keep environment variable names where helpful.
- Remove redundant temporary handoff files after preserving useful context.
- Add or tighten `.gitignore` entries for local secret files.
- Add explicit workflow `permissions:` blocks.

### Acceptance Criteria

- No tracked file contains known exposed secret values.
- Cleanup diff does not introduce new secrets.
- Workflows have least-privilege `permissions:`.
- GitHub push protection remains enabled.

## Codex: Final Risk Review And Sequencing

### Objective

Review subagent outputs, sequence production-safe remediation, and confirm no claims exceed evidence.

### Responsibilities

- Validate that rotation precedes alert closure.
- Validate that non-Git stores were included in the surface map.
- Check that docs do not contain secret values.
- Update `PROJECT_STATUS.md` only after actual remediation is completed.
- Prepare final remediation summary and remaining risk list.

### Acceptance Criteria

- Incident status is clear: planning, containment, rotation, cleanup, or verified resolved.
- Remaining blockers are assigned.
- Verification evidence uses timestamps, alert numbers, and redacted screenshots only.
- No secret values are included in final reports.
