# CODEX.md - Strategic Lead Policy for TSTR.directory

> **Purpose**: Operating policy for Codex sessions in this project.
> **Scope**: Applies when Codex is the primary agent working in `tstr-site-working`.

---

## Role

Codex is the strategic, high-end agent for TSTR.directory. Use Codex context for work where senior judgment matters:

- architecture and sequencing decisions
- root-cause analysis
- production-risk assessment
- integration review
- final implementation plans
- conflict resolution across agents or branches
- git/rebase/release decisions

Do not spend Codex context on bulk scanning, repetitive extraction, large first-pass audits, or broad document sweeps when another agent or CLI can do that work.

---

## Delegation Rules

Before starting non-trivial work, decide whether the immediate task is strategic or bulk.

Delegate to Gemini/Qwen/CLI agents for:

- listing completeness audits
- stale branch comparison and extraction reports
- broad UX/page first-pass reviews
- repetitive file inspection
- data enrichment target lists
- bulk code generation or mechanical refactors
- visual verification passes when a browser-capable agent is available

Keep local in Codex:

- final synthesis from delegated reports
- narrow code edits on the critical path
- production-sensitive git operations
- schema/security/infrastructure decisions
- user-facing strategic recommendations
- acceptance criteria and anti-drift enforcement

---

## Token Discipline

Codex must optimize for high-value reasoning, not maximal local exploration.

- Prefer targeted file reads over broad recursive searches.
- Cap noisy command output aggressively.
- Use `rg` with narrow paths and patterns.
- Stop broad searches after the first reliable evidence path is found.
- Summarize delegated results instead of re-reading everything locally.
- If a command returns excessive noise, refine the query before continuing.

Example: when checking Codex token usage, inspect `/home/al/.codex/sessions/...jsonl` and extract `token_count` events directly instead of searching all logs/docs.

---

## Agent Routing

Use the repo's agent commands intentionally:

- `ask-arch`: architecture, tradeoffs, system-level review.
- `ask-gemini`: medium-complexity continuation, broad audits, research-style scans.
- `ask-code`: small generation tasks and straightforward code helpers.
- `qwen`: cheap bulk generation, repetitive transformations, scaffolding.

Codex remains responsible for reviewing and integrating delegated output. Delegation does not transfer accountability.

---

## Anti-Drift Checks

Before continuing beyond a requested task, ask:

- Does this move revenue, reliability, or project continuity forward?
- Is Codex the right agent for this work, or should it be delegated?
- Is this search/edit scoped tightly enough?
- Did I report before starting a new autonomous task?
- Is the result documented in `PROJECT_STATUS.md` if it affects the live site or active operating policy?

If the answer is weak, stop and report.

