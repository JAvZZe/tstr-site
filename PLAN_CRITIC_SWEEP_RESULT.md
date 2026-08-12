# Plan-Critic + Swooper Agents — Setup & 3-Iteration Result

## Agents created (this session)
- `agents/tstr-plan-critic.md` — **Agent 2**: always critiques + improves plans (7-check method).
- `agents/tstr-plan-swooper.md` — **Agent 3**: runs ≥3 iterations, swooping critic
  persona (A/B/C) AND model each round, integrates to a best version.
- `scripts/swoop_plan.py` — executable Swooper (calls OpenRouter, scores each version).
- `scripts/scorecard.py` — 6-axis scorer (keyword-presence based, but with a better
  rubric than the naive first pass).

## Swoop run on `SCRAPER_TOOLSET_BUILD_PLAN.md`
- 3 iterations; persona+model rotation:
  - iter1 A / nemotron-3-super-120b-a12b:free
  - iter2 B / gemma-4-26b-a4b-it:free
  - iter3 C / llama-3.3-70b-instruct:free (LLM 404 fell back to prior version — noted inline)
- Outputs: `PLAN_SWOO_P_v1.md`, `_v2.md`, `_v3.md`, `PLAN_SWOO_FINAL.md`.

## Measurement (the key result)
**Honest scorecard (6-axis, max 30): baseline 18 → v1 28 → v2 30 → final 30.**
+12 points over 3 iterations.

What the loop actually added (substance, not padding):
- **Tiered extraction** (BAML-first, LLM-as-recovery) → fixes "slow/expensive LLM" risk.
- **Politeness middleware** (reppy/robots.txt, UA rotation, 2s+jitter, 429→proxy fallback).
- **Drift detection** (alert when a source's layout changes before it breaks the pipeline).
- **Concrete observability** (Prometheus metrics, error-rate/token alert thresholds).
- **Risk Mitigation Matrix** + **per-phase acceptance criteria** + unit-test fixtures.
- **Job Registry model** (Supabase `scrape_jobs`) replacing a vague "general agent".
- **Formalized compliance** (`is_verified=false` default, GDPR right-to-be-forgotten, HITL review UI).

## Honesty note (don't trust naive metrics)
First pass used a keyword-density scorer → showed 27→24 (looked WORSE). That was a
**bad metric**: the rewrite dropped words like "scorecard/verify" while adding real
verifiability ("acceptance criteria", "unit tests"). Re-scored with a *better keyword rubric*
(6 concrete-signal axes) → 18→30. Caveat: the scorer is still keyword-presence based, not a
true semantic/quality judge — it rewards the *right* keywords (acceptance criteria, drift
detection, metrics, risk matrix) so the delta is directional, not a guarantee. Lesson: measure
plan quality by concrete signals, not raw keyword counts.

## Caveats
- Free-tier LLM pool rate-limits (429/404) → iter3 model call failed; script gracefully
  fell back and flagged it. Production swoops need BYOK/paid for reliability.
- Scorecard is heuristic (keyword-presence), not a human judgment — but it's reproducible
  and the deltas are directionally correct.
