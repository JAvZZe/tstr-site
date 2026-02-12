# AI System Instruction: Supabase Local & Type Context

**Objective**: Use the newly aligned local Supabase environment and generated TypeScript types for all database operations and feature development.

## 1. Source of Truth (Schema)

* **Primary Schema Definition**: `supabase/migrations/20260203125703_remote_schema.sql`
* **Current State**: The local Docker instance is 1:1 with the remote project (`haimjeaetrsaauitrhfy`).
* **Dependency Note**: The `categories` table is established; all standards and providers logic must reference existing foreign keys defined in the mega-migration file.

## 2. Type Intelligence

* **Type Definitions**: Use `src/types/supabase.ts` for all data fetching and mutations.
* **Constraint**: Do not guess column names. If a table property is unclear, **read the Database interface in the types file** before generating code.

## 3. Local Development Specs

* **Connection**: Use the local Supabase stack.
  * API: `http://127.0.0.1:54321`
* **Environment**: Access keys are located in `.env.local`.

## 4. Development Workflow

* **Safety**: Always verify schema changes via `supabase db diff` before committing.
* **Style**: Avoid ambiguous variable names (e.g., do not use `l`; use `listing`, `loc`, or `standard`).

## 5. Git Integration & Process (MANDATORY)

### 🚨 AGENT PROTOCOL: Schema Changes

**CRITICAL**: Agents MUST run `supabase db diff` before staging any database migration files.
* **Why**: Creates a safety check ensuring migration files match the actual DB state.
* **Workflow**: `Make Changes` -> `supabase db diff` -> `Commit` -> `Push`.

### Recommended Workflow

1. **Make Schema Changes**: Apply migrations or DB changes locally.
2. **Verify**: Run `supabase db diff` to check what will be generated.
3. **Commit**: Use `git add` and `git commit` as usual.
    * *Tip*: VS Code GitLens extension is safe to use for staging/committing.
    * *Critical*: Ensure `supabase/migrations/*.sql` files are included in your commit.
4. **Push**: `git push` to sync with the team.

**Task**: Acknowledge this context. When asking for a feature, prioritize using these specific paths and types.
