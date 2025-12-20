# Manual Migration Deployment Instructions

## Issue
Supabase CLI push is failing due to migration history sync issues. The `pg_stat_statements` extension migration needs to be applied manually.

## Migration Details
- **File**: `supabase/migrations/20251216000001_enable_stat_statements.sql`
- **SQL**: `create extension if not exists "pg_stat_statements" with schema "extensions";`

## Manual Deployment Steps

### Option 1: Supabase Dashboard SQL Editor (Recommended)
1. Go to [Supabase Dashboard](https://supabase.com/dashboard/project/haimjeaetrsaauitrhfy)
2. Navigate to **SQL Editor**
3. Run the following SQL:
   ```sql
   create extension if not exists "pg_stat_statements" with schema "extensions";
   ```
4. Click **Run** to execute

### Option 2: CLI Repair (If Preferred)
If you want to fix the CLI sync issue:
1. Run: `npx supabase db pull` (may take time)
2. If pull succeeds, then: `npx supabase db push`
3. If still failing, use Option 1 above

## Verification
After deployment, you can verify the extension is enabled by running in SQL Editor:
```sql
SELECT * FROM pg_extension WHERE extname = 'pg_stat_statements';
```

## Purpose
This enables `pg_stat_statements` for database performance monitoring and security auditing, allowing detection of slow queries that could indicate DoS attempts.

## Status
- Migration file created locally ✅
- Ready for manual deployment