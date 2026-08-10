# Secret Rotation — Exact Checklist (non-tech, run in dashboards)

> **Why this exists:** The repo redaction sweep (2026-08-10) removed plaintext secrets from
> files, but it did NOT rotate the real keys. GitHub still shows **19 OPEN secret-scanning
> alerts** (alerts #1–#19, some from 2025-10). An alert closes only when the leaked
> credential is **revoked or rotated in its provider** — not when the file is edited.
> This sheet tells you exactly what to click. You need to be logged into each provider.
>
> **Golden rule (do it in this order, every time):**
> 1. Create the NEW key in the dashboard.
> 2. Paste the new key into EVERY place listed ("surfaces").
> 3. Redeploy / restart the service that uses it, then test it works.
> 4. **Only then** revoke/delete the OLD key.
> 5. Resolve the matching GitHub alert.
>
> If you revoke the old key before updating everywhere, the live site breaks.
> Never paste a real key into a file, chat, or commit — use the provider dashboards and
> environment-variable settings only. The pre-commit scanner will block any key you stage.

---

## 0. Before you start — capture where keys live

The 19 alerts, grouped by provider (the first path is where GitHub first saw it; several
alerts have more locations — the `secret_scan.py --history` output lists them all):

| # | Provider | Type | First seen at |
|---|----------|------|---------------|
| 1 | Google | API key | `DEPLOYMENT_ENV.md` |
| 2 | Google | API key | `web/tstr-automation/auto_updater.py` |
| 7 | Google | API key | `web/tstr-automation/debug_page.html` |
| 16 | Google | GCP key bound to service account | `web/tstr-automation/TSTR1.mcp.json` |
| 18,19 | Google | API key (x2) | `.gitnexus/lbug` |
| 8 | Supabase | Service role key | `apply_rls_policy.py` |
| 9 | Supabase | Service role key | `management/reference/SUPABASE_KEYS1.txt` |
| 10 | Supabase | Service role key | `web/tstr-frontend/src/pages/api/submit.ts` |
| 11 | Supabase | Service role key | `apply_standards_migration.py` |
| 12 | Supabase | Service role key | `OPENCODE.md` |
| 13 | Supabase | Personal Access Token (PAT) | `GEMINI.md` |
| 14 | Supabase | Secret key | `web/tstr-automation/export_to_sheets.py` |
| 17 | Supabase | PAT | `web/tstr-automation/TSTR1.mcp.json` |
| 3 | GitHub | Personal Access Token (PAT) | `management/reference/Github Key - Windsurf Cascade Claude Sonnet AI.txt` |
| 4 | GitHub | PAT | `management/reference/Github Key JAvZZe - New site deploy.txt` |
| 5 | GitHub | PAT | `management/reference/Github tstr.site1 MCP Key for Windsurf.txt` |
| 6 | OpenRouter | API key | `management/reference/Openrouter TSTR.site API Key.txt` |
| 15 | OpenRouter | API key | `management/Roo_Code_API_Key_at_Openrouter` |

**Surfaces to update for EACH key** (Systems-Thinking: a key leaked in one file is used in many):
- Cloudflare Pages → **Production** environment variables
- Cloudflare Pages → **Preview** environment variables
- OCI scraper server → `.env` file (and any systemd service env)
- GitHub repo → **Actions secrets** (Settings → Secrets and variables → Actions)
- Supabase → **Edge Function secrets** (if any function uses it)
- Your local dev `.env` (only if you run the scraper locally)
- MCP / agent config files that reference the key (e.g. `TSTR1.mcp.json`, `GEMINI.md`)

---

## 1. Supabase (the big one — 8 alerts: #8,9,10,11,12,13,14,17)

The **service role key** is the master DB key. It is used live by the site
(`submit.ts`, `ai-search.ts`) and by admin scripts. Rotating it is safe ONLY if you
update all surfaces before revoking the old one.

**Steps:**
1. Open **https://supabase.com/dashboard** → your project → **Project Settings → API**.
2. Under "Project API keys", find the **service_role** key. Use **Regenerate / Roll**
   (this issues a new value and invalidates the old after you confirm).
3. Copy the NEW service_role value.
4. Paste it into these surfaces as `SUPABASE_SERVICE_ROLE_KEY`:
   - Cloudflare Pages Production env
   - Cloudflare Pages Preview env
   - OCI scraper `.env`
   - GitHub Actions secrets
   - Supabase Edge Function secrets (if any)
   - local `.env` (if used)
5. Redeploy the site (push to `main`, or redeploy in Cloudflare Pages) so Production
   picks up the new key. Confirm the site still works (submit a test listing, run a search).
6. **Now** revoke the old service_role key in Supabase (the regenerate step usually does this;
   confirm old key shows "invalid").
7. **PATs (#13, #17):** Supabase → **Settings → Access Tokens** → revoke the two leaked
   PATs (the ones referenced in `GEMINI.md` and `TSTR1.mcp.json`). Create fresh PATs only
   if you still use MCP/agent access, and paste the new PAT into the MCP config files.
8. **Secret key (#14):** this is the `anon`/publishable key family — regenerate in the same
   API panel if flagged; it is less sensitive but still rotate and update surfaces.

**Verify:** old service_role key → any admin/write call fails; new key → works.

---

## 2. Google (6 alerts: #1,2,7,16,18,19)

These are Maps + Gemini API keys. Simplest safe path: **rotate all Google API keys** in
the project (you can't easily tell which is which, and rotating all is safer than missing one).

**Steps:**
1. Open **https://console.cloud.google.com** → your project → **APIs & Services → Credentials**.
2. For each **API key** listed: click it → **DELETE** (or **Regenerate key** if you want to
   keep the same restriction profile). Prefer recreate-with-restrictions:
   - Browser/Maps keys → restrict by **HTTP referrer** (`https://tstr.directory/*`).
   - Backend/Gemini keys → restrict by **IP** (the OCI scraper egress IP) and to required APIs only.
3. Copy each NEW key.
4. Paste into surfaces (match the variable name from the code: `PUBLIC_GOOGLE_MAPS_API_KEY`,
   `GOOGLE_API_KEY`, `GEMINI_API_KEY`, etc.):
   - Cloudflare Pages Production + Preview env
   - OCI scraper `.env`
   - local `.env`
   - `web/tstr-automation/TSTR1.mcp.json` (the Gemini/GCP key at line 22)
5. Redeploy and test: a map loads on the site; a Gemini call succeeds from the scraper.

**Verify:** old Google keys → calls return 403; new keys → work only from allowed referrer/IP.

---

## 3. OpenRouter (2 alerts: #6, #15)

**Steps:**
1. Open **https://openrouter.ai/keys**.
2. Revoke the two leaked keys. Create a **new key** only if you still use OpenRouter
   (for agent/LLM access).
3. Paste the new key into:
   - Cloudflare Pages Production + Preview env
   - OCI scraper `.env` / local `.env`
   - any agent config that referenced it (`management/Roo_Code_API_Key_at_Openrouter`,
     `TSTR1.mcp.json` if present)
4. Test the agent/LLM path that uses it.

**Verify:** old OpenRouter key → API returns 401; new key → works.

---

## 4. GitHub PATs (3 alerts: #3, #4, #5)

These are old agent/Windsurf keys (2025-10). Almost certainly unused now, so just revoke.

**Steps:**
1. Open **https://github.com/settings/tokens** (or Settings → Developer settings →
   Personal access tokens → Tokens (classic) + Fine-grained).
2. Find and **Revoke** the three leaked tokens:
   - "Github Key - Windsurf Cascade Claude Sonnet AI"
   - "Github Key JAvZZe - New site deploy"
   - "Github tstr.site1 MCP Key for Windsurf"
3. Only create a replacement if a current CI/job actually needs it, and store it as a
   **GitHub Actions secret**, never in a file.
4. Check **repo → Settings → Secrets and variables → Actions** for any secret that held
   these; update if present.

**Verify:** the revoked tokens no longer authenticate (`gh auth` or API call with them fails).

---

## 5. Close the 19 GitHub alerts

After a key is revoked/rotated, resolve its alert:
1. Open **https://github.com/JAvZZe/tstr-site/security/secret-scanning**.
2. For each of alerts #1–#19: open it → **Resolve** → choose **"This is a false positive"**
   ONLY if you are 100% sure it's dead; otherwise choose **"Revoked"** (or "Used in tests"
   if applicable) and add a short note (e.g. "Supabase service role rotated 2026-08-XX").
3. Alerts with `has_more_locations: true` (most of them) close once the underlying key is
   revoked — you don't need to resolve each location separately.

> **Note on git history:** the `secret_scan.py --history` output will STILL list these files
> after rotation. That's expected — history can't be cleaned without a force-push/rewrite,
> which we coordinate separately. The alerts close because the LIVE key is revoked, not
> because history is clean. Do not try to rewrite history just to satisfy the scan.

---

## 6. Final verification

- [ ] All 19 alerts at `github.com/JAvZZe/tstr-site/security/secret-scanning` show **Closed**.
- [ ] Live site works: submit a listing, run a search, a map renders, Gemini call succeeds.
- [ ] `python3 scripts/secret_scan.py --all` on the working tree shows ONLY `.env`/`.dev.vars`
      (by-design local dev secrets) — nothing else.
- [ ] No new secret committed: try `git add` a file containing a key → the pre-commit hook
      blocks it.

When all boxes are ticked, update `PROJECT_STATUS.md` (Security line) to mark rotation done.
Until then, leave it as "KEY ROTATION STILL PENDING".
