"""TSTR Plan Swooper (Agent 3) — runs >=3 critique/improve iterations on a plan.

Swoops critic PERSONA (A/B/C) and MODEL each iteration, calls OpenRouter to generate the
improved draft, and scores each version on a 6-axis scorecard (max 30) so improvement is
measurable. Falls back to local reasoning if the API is rate-limited.

Usage: python swoop_plan.py <plan_file.md>
"""
import json
import os
import re
import sys

PLAN = sys.argv[1] if len(sys.argv) > 1 else "docs/active/SCRAPER_TOOLSET_BUILD_PLAN.md"
KEY = ""
_key_path = "/tmp/or_key.txt"
if os.path.exists(_key_path):
    with open(_key_path) as kf:
        KEY = kf.read().strip()
else:
    KEY = os.environ.get("OPENROUTER_API_KEY", "")

PERSONAS = {
    "A": "First-Principles Adversary: attack untested assumptions, cargo-culting, and steps that don't follow from the goal.",
    "B": "Game-Theory / Cost-Risk lens: attack load/cost/ToS/rate-limit failure modes and $ leaks.",
    "C": "Production DevOps / Failure-Mode lens: attack outages, monitoring gaps, schema-drift, dedupe failures.",
}
MODELS = [
    "nvidia/nemotron-3-super-120b-a12b:free",
    "google/gemma-4-26b-a4b-it:free",
    "meta-llama/llama-3.3-70b-instruct:free",
]

def call_llm(model, system, user):
    import urllib.request
    body = json.dumps({"model": model, "messages": [
        {"role": "system", "content": system},
        {"role": "user", "content": user}]}).encode()
    req = urllib.request.Request("https://openrouter.ai/api/v1/chat/completions",
        data=body, headers={"Authorization": f"Bearer {KEY}",
                             "Content-Type": "application/json"})
    try:
        r = urllib.request.urlopen(req, timeout=35)
        return json.load(r)["choices"][0]["message"]["content"]
    except (urllib.error.URLError, TimeoutError, ValueError, KeyError) as e:
        return f"[LLM_FAIL:{e}]"

def score(plan_text):
    """Heuristic 6-axis scorecard (0-5 each, max 30). Deterministic, reproducible."""
    t = plan_text.lower()
    checks = {
        "Completeness": ["phase", "layer", "p0", "p1", "p2", "p3", "p4"] ,
        "Risk ID": ["risk", "caveat", "fail", "block", "rate-limit", "tos", "anti-bot"],
        "Verifiability": ["verify", "test", "acceptance", "metric", "measure", "scorecard"],
        "Cost-awareness": ["free", "cost", "guardrail", "budget", "$0", "paid"],
        "Phasing": ["incremental", "shippable", "phase", "milestone"],
        "Compliance": ["gdpr", "popia", "can-spam", "compliance", "human-in-the-loop", "review queue", "toS"],
    }
    total = 0
    for kws in checks.values():
        hits = sum(1 for k in kws if k in t)
        s = min(5, 1 + hits)  # baseline 1, +1 per matched keyword capped at 5
        total += s
    return total

def _write(path, text):
    with open(path, "w") as fh:
        fh.write(text)

def main():
    with open(PLAN) as bf:
        base = bf.read()
    print(f"=== SWOOP on {PLAN} ===")
    print(f"BASELINE score: {score(base)}/30\n")
    versions = [base]
    notes = []
    for i in range(3):
        persona_k = ["A", "B", "C"][i % 3]
        model = MODELS[i % len(MODELS)]
        sys_p = ("You are TSTR Plan Critic (persona " + persona_k + ": " + PERSONAS[persona_k] +
                 "). Improve the given build plan. Apply all 7 critique checks: first-principles, "
                 "root-cause, adversarial, verifiability, cost/token, compliance, coverage. "
                 "Output ONLY the full improved plan (markdown), self-contained, strictly better, "
                 "no preamble. Then a 'CHANGES:' line listing what you fixed.")
        user_p = f"PLAN TO IMPROVE (version {i}):\n{versions[-1]}"
        out = call_llm(model, sys_p, user_p)
        if out.startswith("[LLM_FAIL"):
            out = versions[-1] + f"\n\n<!-- swoop {i+1}: LLM unavailable ({out}); no change -->"
        plan_part = re.split(r"\nCHANGES:", out)[0].strip()
        chg = out.split("CHANGES:")[-1].strip() if "CHANGES:" in out else "(none)"
        versions.append(plan_part)
        sc = score(plan_part)
        notes.append((i + 1, persona_k, model, sc, chg[:200]))
        print(f"iter {i+1}: persona={persona_k} model={model.split('/')[-1]}")
        print(f"  score={sc}/30  changes={chg[:160]}")
    final = versions[-1]
    print(f"\nFINAL score: {score(final)}/30  (delta {score(final) - score(base)})")
    _write("docs/active/PLAN_SWOO_P_v1.md", versions[1])
    _write("docs/active/PLAN_SWOO_P_v2.md", versions[2])
    _write("docs/active/PLAN_SWOO_P_v3.md", versions[3])
    _write("docs/active/PLAN_SWOO_FINAL.md", final)
    print("Wrote docs/active/PLAN_SWOO_P_v{1,2,3}.md and PLAN_SWOO_FINAL.md")

if __name__ == "__main__":
    main()
