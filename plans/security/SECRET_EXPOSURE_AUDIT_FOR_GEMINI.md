# Secret Exposure Audit For Gemini

## Objective

Produce a filename-only inventory of tracked files that may contain committed secrets or sensitive configuration references. This is a discovery pass for cleanup planning, not a credential extraction task.

## Hard Rules

- Never print secret values.
- Never print full lines containing secret values.
- Never copy values into Markdown, chat, shell history, logs, issues, commits, or tickets.
- Output filenames and reason codes only.
- If a command would print matching lines, redirect or transform it so only filenames are emitted.

## Search Scope

Scan tracked files in the repository, including:

- Docs and handoff files
- `_ARCHIVE/`
- `.gitnexus/`
- `.github/`
- `management/`
- `plans/`
- MCP config files
- Frontend and automation config files

Skip untracked local `.env` files unless explicitly asked by the human owner.

## Suggested Filename-Only Commands

Use filename-only output:

```bash
git grep -Il -E 'AIza|ghp_|github_pat_|sb_secret|supabase|service_role|OPENROUTER|CLOUDFLARE|GCP|GOOGLE_API|PRIVATE KEY|BEGIN PRIVATE KEY'
```

For broader filename discovery:

```bash
git ls-files | rg -i '(\.env|secret|credential|key|token|mcp|supabase|cloudflare|openrouter|google|gcp|github|pat|handoff|archive)'
```

If a tool prints matching lines by default, stop and switch to filename-only mode.

## Reason Codes

Assign one or more codes to each filename:

- `possible-secret-value`
- `secret-reference`
- `environment-config`
- `mcp-config`
- `legacy-handoff`
- `archive-risk`
- `workflow-secret-use`
- `docs-redaction-needed`
- `manual-review`

## Output Format

```markdown
| File | Reason Codes | Recommended Owner | Notes |
|---|---|---|---|
| path/to/file.md | secret-reference, docs-redaction-needed | Cleanup subagent | Filename-only review required |
```

Notes must not include secret values or full matching lines.

## Cleanup Handoff

For each file, recommend one of:

- Redact literal secret value.
- Replace with environment variable name.
- Move historical context to `_ARCHIVE/` after redaction.
- Delete redundant temporary file.
- Keep file and add warning that secrets belong in secret stores.
- No action after manual review.

## Verification

- [ ] Output contains no credential values.
- [ ] Output contains no full matching source lines.
- [ ] Every listed file has a reason code.
- [ ] Cleanup subagent can act from filenames without seeing secret values.
