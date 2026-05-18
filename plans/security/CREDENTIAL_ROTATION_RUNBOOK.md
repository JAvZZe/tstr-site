# Credential Rotation Runbook

## Purpose

Rotate every credential class implicated by the public exposure incident and update every runtime surface that consumes those credentials.

This runbook is a sequencing guide. It must not contain secret values.

## Rotation Principles

- Rotate first, then redact. Public Git history is compromised.
- Use separate credentials per service, environment, and trust boundary.
- Restrict new credentials by API, IP, referrer, role, and environment wherever supported.
- Update all non-Git secret stores before deleting old credentials when downtime would otherwise occur.
- Verify old credentials fail after cutover.

## Credential Classes

| Service | Credential Types | Rotation Owner | Primary Stores |
|---|---|---|---|
| Google Cloud | API keys, service account keys | Infra | Google Cloud, Cloudflare, OCI, GitHub Actions, local `.env` |
| GitHub | PATs, `gh` auth token, Actions secrets | Security | GitHub user settings, repo secrets, local auth |
| Supabase | Service role key, PATs, MCP token, Edge Function secrets | Data/Infra | Supabase dashboard, Cloudflare, OCI, GitHub Actions, local `.env` |
| OpenRouter | API keys | App/Infra | Cloudflare, OCI, GitHub Actions, local `.env` |
| Cloudflare | API token, Pages environment variables | Infra | Cloudflare dashboard, local operator machine |

## Systemic Audit Map

For each rotated secret, check every surface:

- Cloudflare Pages production environment variables
- Cloudflare Pages preview environment variables
- Cloudflare Workers secrets, if any
- GitHub Actions repository secrets and environment secrets
- OCI scraper `.env` files and systemd service environments
- Supabase Edge Function secrets
- Local development `.env` files
- MCP config files
- Management scripts and scheduled jobs
- Documentation and archived handoff files

## Rotation Order

1. Freeze risky automation that could consume old credentials during rotation.
2. Inventory active usage by environment variable name and deployment surface.
3. Create replacement credentials with least privilege and restrictions.
4. Update non-Git secret stores:
   - Cloudflare production and preview variables
   - OCI environment files or systemd drop-ins
   - GitHub Actions secrets
   - Supabase Edge Function secrets
   - Local `.env` files
5. Deploy or restart services that need the new credentials.
6. Run smoke tests for production, preview, automation, and admin/write paths.
7. Revoke old credentials.
8. Confirm old credentials fail.
9. Redact tracked files and docs.
10. Resolve GitHub secret scanning alerts with evidence that credentials were revoked.

## Service-Specific Notes

### Google Cloud

- Delete exposed API keys and service account keys.
- Recreate separate keys for browser Maps, backend Maps/geocoding, and Gemini.
- Restrict browser keys by HTTP referrer.
- Restrict backend keys by OCI egress IP.
- Restrict all keys to required APIs only.

### GitHub

- Revoke leaked PATs from user settings.
- Rotate the local `gh` authentication token.
- Review repo, environment, organization, and Dependabot secrets.
- Add explicit `permissions:` blocks to workflows.

### Supabase

- Rotate service role keys and personal access tokens.
- Rotate MCP access tokens.
- Update Cloudflare, OCI, GitHub Actions, local `.env`, and Edge Function secrets.
- Validate admin/write flows after rotation.

### OpenRouter

- Revoke leaked keys.
- Create replacement keys scoped to required usage.
- Update all runtime stores.
- Confirm old keys fail and new keys work only where expected.

### Cloudflare

- Rotate broad API tokens.
- Replace broad admin privileges with scoped tokens.
- Confirm Pages production and preview variables no longer reference stale values.

## Verification Matrix

| Check | Expected Result |
|---|---|
| Old Google keys | Authentication fails |
| New browser Maps key | Works only from approved referrers |
| New backend Maps key | Works only from approved OCI egress IP |
| Supabase admin/write path | Works with rotated service role |
| Supabase old service role | Fails |
| OpenRouter old key | Fails |
| Cloudflare Pages production | Uses rotated env vars |
| Cloudflare Pages preview | Uses rotated env vars |
| GitHub secret alerts | Resolved only after revocation |
| Build/test suite | Passes after env updates |

## Completion Criteria

- [ ] Every exposed credential class has been rotated.
- [ ] Every runtime surface has been updated.
- [ ] Old credentials fail.
- [ ] New credentials are restricted.
- [ ] GitHub secret scanning alerts are resolved or documented with pending provider action.
- [ ] Cleanup PR contains no secret values.
- [ ] `PROJECT_STATUS.md` is updated only after actual remediation, not merely planning.
