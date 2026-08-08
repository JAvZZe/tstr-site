# TSTR Frontend Security Findings (tracked)

Source: scan per tstr-security-hardening skill, 2026-08-07.

## F2 — No centralized input validation (MEDIUM, OPEN)
- `grep -rln 'zod|safeParse'` across src → ZERO.
- Routes do ad-hoc checks (contact.ts loosely; outreach-email.ts validates JSON + size cap).
- No schema contract at API boundaries. Violates skill rule "Always validate all input at the boundary with a schema."
- Recommendation: adopt zod; add a shared `validateBody(schema)` helper in src/lib; apply to all src/pages/api/* POST routes.
- NOT auto-fixed (scope: introduces a dependency + touches 25+ routes). Awaiting decision.

## F1 — Stored/Reflected XSS via innerHTML of user strings (FIXED 2026-08-07)
- Added src/lib/escape.ts (escapeHtml).
- Patched: leads.astro (business_name, owner_notes, contact_type, status), edit.astro (business_name attr), subscription.astro (error.message).
- Verified: npm run build exit 0. Live render NOT verifiable here (astro-preview broken on cloudflare adapter) — compile-only.
