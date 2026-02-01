# Implementation Plan - Security Remediation

The goal is to resolve all active Dependabot alerts for the TSTR-site project without introducing regressions.

## User Review Required

> [!IMPORTANT]
> I have used `overrides` in `package.json` to force newer versions of `wrangler` and `lodash`. This is a powerful tool but can cause instability if the consuming packages aren't compatible. The build seems to be starting okay, but runtime verification is recommended.

## Proposed Changes

### 1. Frontend (`web/tstr-frontend`)

- [x] **Update `@astrojs/cloudflare`**: Moved to `dependencies` and updated to `^12.6.12`.
- [x] **Override `wrangler`**: Forced to `^4.61.1` to fix OS Command Injection (High).
- [x] **Override `lodash`**: Forced to `^4.17.23` to fix Prototype Pollution (Moderate).
- [ ] **Verification**: Run `npm audit` to confirm clean state.

### 2. Automation (`web/tstr-automation`)

- [x] **Update `requests`**: Updated to `2.32.3` in `requirements.txt`.
- [ ] **Verification**: Re-build python environment (if applicable) or just verify file.

### 3. System Health

- [ ] **Root Linting**: Run `npm run lint:js` from the **root** directory to ensure no regressions in code style or static analysis.
- [ ] **Frontend Build**: Run `npm run build` in `web/tstr-frontend` to ensure the new dependency tree resolves correctly and builds the site.

## Verification Plan

### Automated Checks

- `npm audit` (Frontend): Must return 0 vulnerabilities.
- `npm run lint:js` (Root): Must pass.
- `npm run build` (Frontend): Must complete successfully (generate `dist/`).

### Manual Checks

- None required if build passes, as these are deep dependency security fixes.

## Next Steps

1. Execute verification commands.
2. Commit `package.json`, `package-lock.json`, and `requirements.txt`.
3. Push to `main`.
