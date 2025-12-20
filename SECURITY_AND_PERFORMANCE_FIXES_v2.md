# Security & Performance Fixes v2 (2025-12-16)

**Target Agent**: OpenCode Grok Code Fast 1 Free
**Context**: Supabase Dashboard flags 15 Security Issues & 55 Performance Issues despite previous attempts.

## 🚨 Root Cause Analysis

## 🚨 Root Cause Analysis

### Security Issues (Status: 13 Fixed, 2 Remaining)
**Update**: The application of `20251216000001_security_harden_search_paths.sql` successfully resolved 13 high-risk vulnerabilities (12 Function Search Paths + 1 View).

**The Remaining 2 Issues**:
Since the database schema is now clean (`db lint` passes), the final 2 issues are likely **Project-Level Configuration** items that must be resolved in the Dashboard:
1.  **Point in Time Recovery (PITR)**: Supabase often flags if this is disabled.
2.  **MFA / Auth Policies**: "Enable MFA" or "Confirm Email" settings.

**Action**: Check Dashboard > Security > Advisor to confirm. These cannot be fixed via SQL migration.

### Performance Issues (55 Total)
*   **Missing Indexes**: Now that `pg_stat_statements` is enabled, use the **Index Advisor** in the dashboard.
*   **High Sequential Scans**: The dashboard is likely flagging tables like `listings` (191 rows) or `categories` (42k rows) being scanned without indexes.

---

## 🛠️ Execution Instructions

### Step 1: Apply Security Hardening & Enable Monitoring
Run the new migration which enforces strict search paths and enables `pg_stat_statements`.

**Command**:
```bash
npx supabase db push --linked
```
*Note: If `db push` is not preferred, copy the content of `supabase/migrations/20251216000001_security_harden_search_paths.sql` and run it in the Supabase SQL Editor.*

### Step 2: Verify Security Issues
After applying Step 1, the "Security Advisor" count should drop.
*   Check Dashboard > Security > Advisor.

### Step 3: Analyze Performance (Post-fix)
Once `pg_stat_statements` is enabled (from Step 1), the Dashboard's "Query Performance" tab will start collecting data.
*   **Wait 24 hours** for meaningful data.
*   Then Check "Index Advisor" in the Dashboard.

### Step 4: Verification Queries (Manual)
Run this SQL to verify `search_path` is correct (should start with `pg_catalog`):

```sql
SELECT proname, proconfig 
FROM pg_proc 
WHERE proname IN (
  'handle_new_user', 'get_click_stats', 'get_top_clicked_listings', 
  'make_user_admin', 'update_website_domain', 'can_auto_claim', 
  'extract_domain', 'search_by_standard', 'user_owns_listing', 
  'can_view_contact_info', 'get_user_tier', 'update_updated_at_column'
);
```

## 📂 Files Created
*   `supabase/migrations/20251216000001_security_harden_search_paths.sql`: The master fix script.
