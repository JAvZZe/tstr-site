# Claude Code Agents — Orchestrator

The 24 legacy micro-agents (code-auditor, bug-auditor, seo-auditor, ui-auditor,
etc.) were **retired on 2026-08-09** and moved to `.claude/agents/_ARCHIVE/`.
They are superseded by the canonical TSTR agent skills (Hermes `tstr-*` set),
which are the single source of truth for agent behavior on this project.

## Two definitions of each agent (keep in sync)
1. **Canonical (Hermes skills)** — `/home/al/.hermes/profiles/tstr-hub_pm/skills/tstr-*/SKILL.md`.
   Authoritative; edit here first.
2. **Claude/CLI mirror** — `.claude/agents/tstr-*.md` (this folder). Generated
   from the canonical skills so non-Hermes agents (Claude Code, Codex, CLI
   agents) share the SAME principles. Read the matching `.md` when operating
   outside the Hermes harness. If the two disagree, the Hermes skill wins.

## Canonical agents (full roster, 18)
- tstr-team-lead — orchestrator / router
- tstr-agent-creator — meta-agent: creates new TSTR agents/skills
- tstr-frontend — Astro 6 frontend engineering
- tstr-perf — Core Web Vitals / performance audit
- tstr-ux — accessibility / responsive / UX audit
- tstr-db — Supabase/Postgres schema + query health
- tstr-deploy — deploy-readiness + live verification (Wrangler)
- tstr-qa — dedicated QA/testing (Playwright + independent LLM critic)
- tstr-tdd — test-driven development
- tstr-code-review — code review discipline
- tstr-verification-gate — static CI lint/scan gate
- tstr-content — content/writing (anti-AI-slop voice)
- tstr-seo — SEO + content contract (incl. GEO/AEO)
- tstr-growth — marketing/growth
- tstr-security / tstr-security-hardening — security
- tstr-data-ops — scraper/data operations
- tstr-scraper-agent — OCI scraper ops

## Rules
1. Use the `tstr-*` skills/.md as the agent definitions. Do not resurrect
   `_ARCHIVE/` agents — update or extend the canonical skill instead.
2. New agent needs → route to tstr-agent-creator (researches best practice,
   functions, and existing skills, then scaffolds the new agent).
3. One clean change per commit; report-first before irreversible actions
   (tstr-team-lead protocol).
