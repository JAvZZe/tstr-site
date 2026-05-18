# GitHub Security Audit

## Purpose

Audit and remediate GitHub security findings for public repository `JAvZZe/tstr-site` on default branch `main`.

Do not print, copy, or commit secret values. Inventory findings by alert number, provider, path, and remediation owner only.

## Known Starting State

- Repository: `JAvZZe/tstr-site`
- Visibility: Public
- Default branch: `main`
- Issues: none open or closed at the time of incident planning
- Open pull requests:
  - `#13` Dependabot grouped npm/yarn update
  - `#9` Dependabot `python-dotenv` update

## Secret Scanning Findings

Known open alert classes:

- 5 Google API Key
- 1 GCP API Key Bound to a Service Account
- 3 GitHub Personal Access Token
- 5 Supabase Service Key
- 2 Supabase Personal Access Token
- 1 Supabase Secret Key
- 2 OpenRouter API Key

Audit command guidance:

```bash
gh api repos/JAvZZe/tstr-site/secret-scanning/alerts --paginate
```

Record only:

- Alert number
- Secret type
- State
- Resolution
- File path
- Commit SHA
- First detected timestamp
- Remediation owner

## Code Scanning Findings

Known open high/medium alert categories:

- URL substring checks
- Stack trace exposure
- Clear-text sensitive logging
- Flask debug mode
- Missing workflow permissions

Audit command guidance:

```bash
gh api repos/JAvZZe/tstr-site/code-scanning/alerts --paginate
```

Record only:

- Alert number
- Rule ID
- Severity
- State
- Tool
- File path
- Line
- Remediation owner

## Dependabot Findings

Known affected areas:

- Root lockfiles
- Frontend lockfiles
- `requests` in `web/tstr-automation`
- `python-dotenv` in `web/tstr-automation`

Audit command guidance:

```bash
gh api repos/JAvZZe/tstr-site/dependabot/alerts --paginate
```

Record:

- Alert number
- Package
- Ecosystem
- Manifest path
- Severity
- Patched version
- PR number if available
- Remediation owner

## GitHub Controls To Confirm

- [ ] Secret scanning enabled.
- [ ] Push protection enabled.
- [ ] Dependabot alerts enabled.
- [ ] Dependabot security updates enabled.
- [ ] CodeQL enabled.
- [ ] Branch protection active for `main`.
- [ ] Workflows include explicit least-privilege `permissions:` blocks.
- [ ] Repository secrets contain only current rotated values.
- [ ] Organization and user PATs related to the repo are revoked or rotated.

## Remediation Rules

- Treat Git history as compromised. Redaction reduces future exposure but does not make old leaked credentials safe.
- Rotate every exposed credential before closing the related alert.
- Never close an alert as false positive unless the provider confirms it cannot authenticate.
- Redact tracked files only after replacements have been moved into approved secret stores.
- Do not paste alert `secret` fields into any output.

## Output Format For Subagents

Produce a Markdown table with these columns:

| Alert | Category | Severity | Path | State | Owner | Required Action |
|---|---|---|---|---|---|---|

Use `redacted` for any sensitive field. Do not include credential values.
