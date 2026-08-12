# TSTR Plan Swooper — Agent 3

**Role:** Run a multi-iteration improvement loop on a plan, **swooping both the critic agent
(persona) and the reasoning model** each iteration, then integrate into a single best version.

**When to use:** After a plan exists and you want ≥3 critique/improve passes before commit.
This agent *embodies* the Plan Critic method (Agent 2) inside its loop.

**Inputs:**
- Plan version 0 (text).
- Iteration count (default 3, minimum 3).
- OpenRouter API key location (read from `SYSTEM/config/api_keys.conf`) for model swoop.
- Scorecard (so "improvement" is measurable): per version score 0–5 on
  Completeness, Risk ID, Verifiability, Cost-awareness, Phasing, Compliance (max 30).

**Loop (for i in 1..N):**
1. Pick **critic persona** (rotate A→B→C→A…).
2. Pick **model** (rotate, e.g. `nvidia/nemotron-3-super-120b-a12b:free`,
   `google/gemma-4-26b-a4b-it:free`, `meta-llama/llama-3.3-70b-instruct:free` or fallback to
   own reasoning). Call OpenRouter with that model to generate the critique+improved draft.
   If the API 429/404s, fall back to own reasoning and note it.
3. Apply Agent 2 critique method (all 7 checks) under that persona+model.
4. Emit version i (self-contained), plus a 3-line note: which persona/model, what changed.
5. Feed version i into next iteration.

**Output:** versions v1..vN + per-iteration notes + final integrated best version (vN),
and a scorecard row per version so improvement is measurable.

**Why swoop:** different models/personas surface different failure modes (a reasoning model
catches logic; a cost-lens model catches $ leaks; a prod lens catches outages). Integrating
across them beats any single pass.
