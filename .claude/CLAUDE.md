# Claude Code Agents — Orchestrator

The 24 legacy micro-agents (code-auditor, bug-auditor, seo-auditor, ui-auditor,
etc.) were **retired on 2026-08-09** and moved to `.claude/agents/_ARCHIVE/`.
They are superseded by the canonical TSTR agent skills (Hermes `tstr-*` set),
which are the single source of truth for agent behavior on this project.

## Canonical agents (Hermes `tstr-*` skills)
Defined in `/home/al/.hermes/profiles/tstr-hub_pm/skills/`:
- tstr-team-lead — orchestrator / router
- tstr-frontend — Astro 6 frontend engineering
- tstr-seo — SEO + content contract (incl. GEO/AEO)
- tstr-content — content/writing agent (anti-AI-slop voice)
- tstr-scraper-agent — OCI scraper ops
- tstr-data-ops — scraper/data operations
- tstr-security / tstr-security-hardening — security
- tstr-growth — marketing/growth
- tstr-code-review — code review discipline
- tstr-tdd — test-driven development
- tstr-qa — dedicated QA/testing agent (Playwright + independent LLM critic)
- tstr-verification-gate — static CI lint/scan gate
- tstr-agent-creator — meta-agent: creates new TSTR agents/skills as needed

## Rules
1. Use the `tstr-*` skills as the agent definitions. Do not resurrect
   `_ARCHIVE/` agents — update or extend the canonical skill instead.
2. New agent needs → route to tstr-agent-creator (it researches best practice,
   functions, and existing skills, then scaffolds the new agent).
3. One clean change per commit; report-first before irreversible actions
   (tstr-team-lead protocol).
