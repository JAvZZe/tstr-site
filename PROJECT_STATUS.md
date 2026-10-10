# TSTR.DIRECTORY - PROJECT STATUS

> **SINGLE SOURCE OF TRUTH** for agents. Prefer this file over chat memory.
> **Last Updated**: 2026-10-10 08:07 UTC
> **Updated By**: Al ai
> **Live**: https://tstr.directory responds 200. Debug `/api/debug-env` and `/api/debug-full` return 404.
> **Strategy flag**: IAF CertSearch **DEFERRED** until first client payment (stub client, no key, no $499 plan).
> **Repo flag**: `main` is **4 commits ahead of origin/main** (local tip not on GitHub; includes this status ledger). Dirty tree still has real uncommitted work (notably `ai-search.ts`). Do not blind-commit.

---

## Do next (ordered)

1. **Decide fate of the 4 unpushed commits** (push, PR, or reset). Until then Cloudflare will not build this tip.
2. **Finish or discard the uncommitted `ai-search.ts` anon-key change**. HEAD and `origin/main` still use `SUPABASE_SERVICE_ROLE_KEY`. Working tree swaps to `PUBLIC_SUPABASE_ANON_KEY`. That fix is **not** in any commit yet (commit message on `65bd86c` claims it; the file list does not include it).
3. **Triage ~50 modified files** outside `_ARCHIVE/` (mostly Ubuntu-26 path/doc string churn). Keep real code separate from path noise.
4. **Credential rotation** still open per older security docs. Live debug exposure is contained. Checklist: `docs/active/SECRET_ROTATION_CHECKLIST.md` (and `docs/active/LIVE_CREDENTIAL_EXPOSURE_REMEDIATION_PLAN.md`). Re-count GitHub secret-scanning alerts before treating “19” as current.
5. **AdSense**: docs still say waiting since 2025-10-29. Check the Google account; update or archive `docs/active/ADSENSE_APPROVAL_WAITING.md`.
6. **IAF work**: do not start until a paying client exists.

---

## Overnight verify

| Night | Verdict | Note |
|-------|---------|------|
| 2026-10-10 | PASS | Live 200, SSR build ~78s, lint 0, secrets CLEAN |
| 2026-10-05 … 2026-10-09 | PASS | Same pattern |
| 2026-10-04 | Mixed | History/links/audit fails; build/live still OK |

Recurring warning only: unpushed commits (since Oct 5).

---

## Git reality (verified 2026-10-10)

### Ahead of origin (4 commits)

| SHA | What it actually contains |
|-----|---------------------------|
| `65bd86c` | Path/doc updates under agents + automation docs; supabase `.temp` cleanup. **Does not change `ai-search.ts`.** Message claims an ai-search fix; file list does not. |
| `0dce6c0` | Ubuntu-26 layout path migration across docs/scripts |
| `4e8f24f` | `europe-pseo.astro`, `hydrogen_scraper.py` skeleton, IAF deferred docs |
| *(tip)* | This `PROJECT_STATUS.md` correction (v2.6.6) |

Real code in that tip vs origin: Europe PSEO page, hydrogen scraper skeleton, plus a few scraper helper path edits.

### Still dirty (selected)

- `web/tstr-frontend/src/pages/api/ai-search.ts`: service-role → anon (uncommitted)
- Dozens of path/doc files from the Ubuntu-26 migration leftover vs what was already committed
- Untracked noise: plans, `audiences/`, `newsletters/`, `_ARCHIVE/tstr_verify_*`, one listing-logo migration SQL

### Stale branches (do not merge blindly)

| Branch | Note |
|--------|------|
| `hydrogen-standards` | Stale since 2026-03-19; high conflict |
| `feat/astro-6-migration` | Stale since 2026-03-24; later phase |

---

## Project overview

| Field | Value |
|-------|-------|
| Name | TSTR.directory |
| Type | Testing services directory |
| Stack | Astro 5.x + React 18 + Supabase + Python scrapers |
| Deploy | Cloudflare Pages (frontend) + OCI (scrapers) |
| Listings | 783 active (homepage, 2026-10-10) |
| Categories | 33+ specialized (+3 Hydrogen) |
| Maps | Google Maps Static + Interactive |

---

## Geographic expansion

- [x] Europe (EA): ScopeMatch.eu scaled (54+ labs). PSEO page local in unpushed `4e8f24f`.
- [x] Middle East (ARAC): GAC + manual seeding (25+ labs). Saudi Energy hub seeded (GCC Lab, Al-Hoty, ETLCO).
- [ ] APAC: NATA blocked; further scale waits on IAF (deferred).

### IAF CertSearch (deferred)

Paused until first subscription payment. No API key. No plan purchased. Client stub only. See `docs/active/IAF_API_INTEGRATION_PLAN.md`. Lead-gen pays first; verification is a claim/value-add, not a pre-revenue cost.

---

## Security snapshot

| Item | State (2026-10-10) |
|------|--------------------|
| Public debug routes | Contained (404 in production) |
| Repo plaintext redaction + pre-commit secret scan | Present (`scripts/secret_scan.py`) |
| `ai-search.ts` key type | **Still service-role on HEAD/origin**; anon fix only in working tree |
| Credential rotation | Incomplete; follow `docs/active/SECRET_ROTATION_CHECKLIST.md`. Older notes claimed 19 open GitHub alerts; re-verify with `gh` before acting on that number. |

---

## Done (context only)

- Unified form handler (claim/submit/contact/RFQ) on main history
- Scraper BaseNicheScraper standardization + international location parsing
- Scraper Telegram alerting with cooldown
- ShellCheck gate in pre-commit + CI
- Consent-gated analytics + Cloudflare Web Analytics live
- Invalid URL scan 2026-08-10: one confirmed malformed (`ABIOMED HIGIENE`); full dead-link re-scan must run from OCI (dev box outbound false positives)

---

## Links

- Live: https://tstr.directory
- GitHub: https://github.com/JAvZZe/tstr-site
- Supabase: https://haimjeaetrsaauitrhfy.supabase.co

---

## Changelog

- **v2.6.6 (2026-10-10)**: Critique pass. Fixed false claim that `ai-search` anon-key landed in `65bd86c`. Separated verified git facts from aspirational commit messages. Replaced missing `CREDENTIAL_ROTATION_RUNBOOK.md` pointer. Softened unverified “19 alerts” count. Collapsed history into actionable “Do next”.
- **v2.6.5 (2026-10-10)**: First refresh after stale Oct 4 ledger (overnight PASS streak, unpushed list, listing count).
