# HANDOFF TO GEMINI FLASH — Email Exposure Removal

**Created**: 2026-03-20 20:29 UTC  
**Created By**: Antigravity  
**Branch**: `search-fix`  
**Priority**: P1 — Fixes broken links and protects domain reputation

---

## Context

Ahrefs flagged broken links on tstr.directory. Root causes identified and partially fixed:

1. ✅ **ISO/TS 15916:2026 slug** — Fixed. Set `slug = 'iso-ts-15916-2026'` in Supabase `standards` table. Will go live on next deploy.

2. 🔜 **Email exposure → Cloudflare 404s** — NOT YET DONE. This is your task.

---

## Your Task

Execute the plan in this file:

```
.gemini/antigravity/brain/68635c4f-00e9-4560-9cf6-a26df25ae66f/gemini_flash_execution_plan.md
```

Absolute path:
```
/home/al/.gemini/antigravity/brain/68635c4f-00e9-4560-9cf6-a26df25ae66f/gemini_flash_execution_plan.md
```

**Read it fully before starting.**

---

## Summary of Required Changes

| File | Changes Needed |
|------|---------------|
| `src/pages/pricing.astro` | Replace 2 EFT/BTC mailto JS calls → contact form redirects; fix Enterprise CTA href; remove raw `{CONTACTS.sales}` text in FAQ (×2); fix 2 inline modal `mailto:` links |
| `src/pages/contact.astro` | Replace 3 raw `{CONTACTS.*}` email outputs with "use the contact form above" text |
| `src/pages/privacy.astro` | Replace `mailto:` contact link with `/contact` page link |
| `src/pages/terms.astro` | Same as privacy.astro |

---

## Environment Notes

- **Working directory**: `/media/al/AI_DATA/AI_PROJECTS_SPACE/ACTIVE_PROJECTS/TSTR-site/tstr-site-working`
- **Frontend**: `web/tstr-frontend/`
- **Branch**: `search-fix` (already checked out)
- **⚠️ `npx supabase db query` is broken** in this environment — use Node.js scripts with `@supabase/supabase-js` and the service key from `web/tstr-automation/.env` if DB access is needed.
- **Do NOT touch** the Supabase `standards` table — the slug was already fixed.

---

## Verification

After changes:
```bash
# Zero emails in source
grep -rn "@tstr.directory\|mailto:" web/tstr-frontend/src/pages/ --include="*.astro" --include="*.ts"

# Build must succeed
cd web/tstr-frontend && npm run build

# Commit
git add web/tstr-frontend/src/pages/{pricing,contact,privacy,terms}.astro
git commit -m "[GeminiFlash] Remove email exposure: replace mailto links with /contact redirects"
git push origin search-fix
```

---

## Out of Scope

Do NOT implement in this session:
- Cloudflare Turnstile CAPTCHA
- Per-provider contact modal
- Any new Edge Functions

These are Phase 2, documented in `PROJECT_STATUS.md`.
