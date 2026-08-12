"""Better scorecard: rewards concrete plan quality signals, not just keyword density.
Scored 0-5 per axis (max 30). Applied to baseline + each swoop version for honest comparison.
"""

def better_score(t):
    t = t.lower()
    axes = {
        "Acceptance/Verifiability": ["acceptance criteria", "unit test", "fixture",
                                       "ci schema", "on conflict", "upsert", "test data"],
        "Risk/Failure-mode": ["drift", "backoff", "proxy fallback", "rate-limit", "429",
                               "403", "risk mitigation", "expo", "retry"],
        "Cost-guard": ["max_tokens", "token_usage", "baml-first", "llm-as-recovery",
                       "tiered extraction", "hard cap", "$0", "free"],
        "Observability": ["prometheus", "metric", "alert", "trace", "drift_detection",
                          "success_rate", "error_rate", "threshold"],
        "Compliance/HITL": ["is_verified", "gdpr", "right-to-be-forgotten", "robots.txt",
                            "streamlit", "human review", "review ui", "can-spam", "popia"],
        "Architecture-clarity": ["job registry", "scrape_jobs", "composite key", "tier 1",
                                 "tier 2", "reppy", "ua rotation", "user-agent"],
    }
    total = 0
    detail = {}
    for ax, kws in axes.items():
        hits = sum(1 for k in kws if k in t)
        s = min(5, 1 + hits)
        total += s
        detail[ax] = s
    return total, detail

if __name__ == "__main__":
    files = {
        "baseline": "SCRAPER_TOOLSET_BUILD_PLAN.md",
        "v1": "PLAN_SWOO_P_v1.md",
        "v2": "PLAN_SWOO_P_v2.md",
        "v3/final": "PLAN_SWOO_FINAL.md",
    }
    print(f"{'version':12} {'score':5}  detail")
    for name, f in files.items():
        try:
            with open(f) as fh:
                s, d = better_score(fh.read())
            print(f"{name:12} {s:>3}/30  {d}")
        except FileNotFoundError:
            print(f"{name:12} FILE MISSING")
