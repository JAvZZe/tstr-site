# 🛠️ TSTR.DIRECTORY - MAINTENANCE LOG

> **Purpose**: Track all maintenance, security updates, linting, and infrastructure improvements.
> **Referenced By**: `PROJECT_STATUS.md`
> **Last Updated**: 2026-01-30

---

## 📅 2026-01-30

### 🛡️ Security Remediation (Dependabot)

**Agent**: Gemini 2.5 Pro (Antigravity)
**Commit**: `7858143`

- **Frontend (`web/tstr-frontend`)**:
  - **Critical Fix**: Overridden `wrangler` to `^4.61.1` to resolve **High Severity** usage of `node-tar` and command injection vulnerabilities.
  - **Critical Fix**: Overridden `lodash` to `^4.17.23` to resolve Prototype Pollution.
  - **Update**: Moved `@astrojs/cloudflare` to `dependencies` and updated.
  - **Result**: `npm audit` violations reduced from 14 to **0**.

- **Automation (`web/tstr-automation`)**:
  - **Fix**: Updated `requests` to `2.32.3` to resolve credential leak vulnerabilities.

### 🧹 Codebase Linting & Cleanup

**Agent**: Gemini 2.5 Pro (Antigravity)
**Commit**: `2c4cb42`

- **JavaScript/TypeScript**:
  - **Root Scripts**: Fixed ESLint errors in `debug_submit_browser.js`, `analyze_listings.js`, `test-phases.js` (unused variables, undefined references).
  - **Backend Utils**: Fixed `require()` violations in `url-validator.js` and `validate-csv.js`.
  - **Verification**: `npm run lint:js` now passes cleanly across the entire project.

---

## 📅 2026-01-28

### 🌐 Domain Migration Verification

**Agent**: Gemini 2.5 Pro (Antigravity)
**Commit**: `c1c0902`

- **Cleanup**: Verified removal of all legacy `tstr.site` references in functional code.
- **Documentation**: Updated agent guides to reflect `tstr.directory` as the single source of truth.

---

## 📅 2026-01-15

### 💳 PayPal Integration Maintenance

**Agent**: OpenCode / Gemini

- **Stability**: Fixed "Invalid JWT" errors by switching to Anon Key + Service Role verification pattern.
- **Resilience**: Implemented robust cancellation handling (treating 404/422 as success) to prevent state drift between PayPal and Supabase.
