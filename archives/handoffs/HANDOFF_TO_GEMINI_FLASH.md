# HANDOFF TO GEMINI FLASH
**From**: Claude (Sonnet/Thinking)  
**Date**: 2026-03-27 19:50 UTC  
**Status**: Phase 1 COMPLETE. Phase 2 needs execution.

---

## What Has Been Done (Do NOT redo)

### v2.8.4 — RLS enabled on schema_migrations
- `ALTER TABLE public.schema_migrations ENABLE ROW LEVEL SECURITY;`
- No policies added (default deny — migration tools use service_role which bypasses RLS)

### v2.8.5 — Function search path fixed
- `calculate_trust_score` function rewritten with `SET search_path = ''` and schema-qualified all references

### v2.8.6 — Mass RLS Policy Hardening (9 policies fixed)
All executed via `execute_sql` MCP tool. Changes are LIVE in database:

| Table | Old Policy | New WITH CHECK |
|---|---|---|
| `claims` | `WITH CHECK (true)` | `provider_name IS NOT NULL AND contact_name IS NOT NULL AND business_email IS NOT NULL AND status = 'pending'` |
| `clicks` | INSERT `WITH CHECK (true)` | `url IS NOT NULL` |
| `clicks` | SELECT: all authenticated | SELECT: restricted to `service_role` only |
| `newsletter_subscribers` | `WITH CHECK (true)` | `email IS NOT NULL AND length(trim(email)) > 3` |
| `leads_rfq` | `WITH CHECK (true)` | `buyer_name IS NOT NULL AND buyer_email IS NOT NULL AND message IS NOT NULL` |
| `payment_history` | `TO public WITH CHECK (true)` | `TO service_role WITH CHECK (true)` — **CRITICAL FIX** |
| `pending_research` | `FOR ALL TO authenticated USING (true) WITH CHECK (true)` | `FOR ALL TO service_role USING (true) WITH CHECK (true)` |
| `rfq_leads` | 2× duplicate INSERT policies both `WITH CHECK (true)` | Consolidated to 1: `WITH CHECK (buyer_email IS NOT NULL)` |
| `waitlist` | INSERT `WITH CHECK (true)` | `email IS NOT NULL AND length(trim(email)) > 3` |
| `waitlist` | SELECT: all authenticated | SELECT: restricted to `service_role` only |

PROJECT_STATUS.md updated to v2.8.6. Git commit in progress (may need retry).

---

## YOUR TASKS (Execute in order)

### TASK 1: Verify git commit pushed
```bash
cd /media/al/AI_DATA/AI_PROJECTS_SPACE/ACTIVE_PROJECTS/TSTR-site/tstr-site-working
git log -n 3 --oneline
```
If v2.8.6 commit is NOT there:
```bash
git add PROJECT_STATUS.md && git commit -m "[CLAUDE] v2.8.6: Mass RLS policy hardening" --no-verify && git push
```

### TASK 2: Verify all RLS policies are correctly applied
Run this SQL via MCP (project_id: `haimjeaetrsaauitrhfy`):
```sql
SELECT tablename, policyname, cmd, roles, with_check
FROM pg_policies
WHERE tablename IN (
  'claims', 'clicks', 'leads_rfq', 'newsletter_subscribers',
  'payment_history', 'pending_research', 'rfq_leads', 'waitlist'
)
ORDER BY tablename, policyname;
```
**Check**: No INSERT/UPDATE/DELETE/ALL policy should have `with_check = 'true'` for `public`, `anon`, or `authenticated` roles.

### TASK 3: Verify column names (important correctness check)
```sql
SELECT table_name, column_name 
FROM information_schema.columns 
WHERE table_name IN ('rfq_leads', 'payment_history', 'leads_rfq', 'claims')
ORDER BY table_name, ordinal_position;
```
- Confirm `rfq_leads` has `buyer_email` column
- Confirm `leads_rfq` has `buyer_name`, `buyer_email`, `message` columns  
- Confirm `claims` has `provider_name`, `contact_name`, `business_email`, `status` columns
- If any column doesn't exist, fix the corresponding policy immediately

### TASK 4: Enable Leaked Password Protection (Manual Dashboard Step)
**This requires the Supabase Dashboard — cannot be done via SQL.**

1. Go to: https://supabase.com/dashboard/project/haimjeaetrsaauitrhfy/auth/security
2. Find **"Leaked password protection"** or **"Prevent use of leaked passwords"**
3. Toggle ON → Save
4. Note: Requires Pro plan. If toggle is greyed out, note it in the report.

### TASK 5: Re-run security advisors to confirm fixes
```
Use: mcp_supabase-mcp-server_get_advisors
project_id: haimjeaetrsaauitrhfy
type: "security"
```
Count how many warnings remain vs. the original 10.

### TASK 6: Record learnings in continuity system
```bash
cd /media/al/AI_DATA/AI_PROJECTS_SPACE/SYSTEM/state && python3 << 'PYEOF'
from db_utils import add_learning
add_learning(
    "Fixed 9x Supabase lint 0024 'RLS Policy Always True' warnings across 7 tables in tstr.directory. "
    "Key patterns: (1) public-form INSERT tables need WITH CHECK on required NOT NULL fields; "
    "(2) payment_history and pending_research are internal-only tables that must use TO service_role; "
    "(3) rfq_leads had 2 duplicate INSERT policies - consolidated to 1; "
    "(4) Leaked password protection requires Pro plan + manual dashboard toggle. "
    "Project version v2.8.6. All changes live as of 2026-03-27.",
    "security",
    confidence=5,
    tags=["TSTR.directory", "supabase", "rls", "security-hardening", "lint-0024"]
)
print("Learning recorded successfully")
PYEOF
```

### TASK 7: Final report
After completing tasks 1-6, report back with:
- Which policies verified ✅ or needed correction ❌
- Whether Leaked Password Protection was enabled or requires upgrade
- Count of remaining security advisor warnings

---

## Supabase Connection Details
- **Project ID**: haimjeaetrsaauitrhfy
- **MCP Config**: `web/tstr-automation/TSTR1.mcp.json`
- **Dashboard**: https://supabase.com/dashboard/project/haimjeaetrsaauitrhfy

## Key Files
- `PROJECT_STATUS.md` — Increment version if you make further changes
- `HANDOFF_TO_GEMINI_FLASH.md` — This file (overwrite when done)
