# Gemini Filename-Only Secret Inventory (2026-05-13)

## Objective
Inventory of tracked files potentially containing secrets or sensitive credential references. No secret values or source lines are included in this report.

| File | Reason Codes | Recommended Owner | Notes |
|---|---|---|---|
| `.ai-session.md` | secret-reference, manual-review | Cleanup subagent | Contains detailed session history with secret references |
| `.mcp.json` | mcp-config, environment-config | Cleanup subagent | Root MCP configuration file |
| `AGENTS.md` | secret-reference, docs-redaction-needed | Cleanup subagent | Mentions Supabase credential rotation and legacy formats |
| `CLAUDE.md` | secret-reference, docs-redaction-needed | Cleanup subagent | Contains legacy JWT format examples |
| `GEMINI.md` | secret-reference, docs-redaction-needed | Cleanup subagent | Contains legacy JWT format examples |
| `OPENCODE.md` | possible-secret-value, docs-redaction-needed | Cleanup subagent | Contains publishable keys and legacy JWT examples |
| `TSTR.md` | secret-reference | Cleanup subagent | Primary agent instructions with key references |
| `web/tstr-automation/TSTR1.mcp.json` | possible-secret-value, mcp-config | Cleanup subagent | Contains exposed Supabase Access Token |
| `web/tstr-automation/requirements.txt` | environment-config | Cleanup subagent | Updated to fix vulnerable dependencies |
| `web/tstr-frontend/.env.example` | environment-config | Cleanup subagent | Example environment file |
| `web/tstr-frontend/src/lib/supabase.ts` | secret-reference | Cleanup subagent | Supabase client initialization logic |
| `management/reference/SUPABASE_KEYS1.txt` | possible-secret-value, manual-review | Cleanup subagent | Tracked file likely containing literal keys |
| `management/reference/Supabase_TSTR.site_Gemini_CLI_token.txt` | possible-secret-value, manual-review | Cleanup subagent | Tracked file likely containing literal tokens |
| `management/reference/Openrouter_TSTR.site_API_Key.txt` | possible-secret-value, manual-review | Cleanup subagent | Tracked file likely containing literal keys |
| `management/reference/Github_Key_JAvZZe_-_New_site_deploy.txt` | possible-secret-value, manual-review | Cleanup subagent | Tracked file likely containing literal keys |
| `.gitnexus/lbug` | possible-secret-value, archive-risk | Cleanup subagent | Large file containing Google and PayPal credentials |
| `.github/workflows/ci.yml` | workflow-secret-use | Cleanup subagent | Uses repository secrets |
| `.github/workflows/keep-supabase-active.yml` | workflow-secret-use | Cleanup subagent | Uses repository secrets |
| `_ARCHIVE/archive/completed-tasks/2025-12/Biotech_Dir/GET_CORRECT_SUPABASE_KEYS.md` | legacy-handoff, possible-secret-value | Cleanup subagent | Historical doc with potential keys |
| `_ARCHIVE/archive/completed-tasks/2025-12/Biotech_Dir/HANDOFF_WAITLIST_SUPABASE_KEY_2025-11-22.md` | legacy-handoff, docs-redaction-needed | Cleanup subagent | Historical handoff with key references |
| `_ARCHIVE/archive/completed-tasks/2025-12/Biotech_Dir/WAITLIST_DEBUG_COMPLETE_ANALYSIS.md` | legacy-handoff, possible-secret-value | Cleanup subagent | Historical analysis with potential keys |
| `_ARCHIVE/archive/completed-tasks/2025-12/SESSION_PROGRESS_2025-11-22.md` | legacy-handoff, docs-redaction-needed | Cleanup subagent | Historical progress report with key references |
| `_ARCHIVE/archive/completed-tasks/2025-12/update_service_key.sh` | possible-secret-value, archive-risk | Cleanup subagent | Script with potential hardcoded examples |
| `plans/security/GITHUB_SECURITY_AUDIT.md` | secret-reference | Cleanup subagent | Audit file referencing categories of findings |
| `secret_alerts.json` | possible-secret-value, manual-review | Cleanup subagent | Untracked but observed JSON with alert details |

## Verification
- NO secret values are included in this report.
- NO full matching source lines are included in this report.
- All identified files have at least one reason code.
- This inventory is commit-safe.
