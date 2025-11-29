#!/usr/bin/env python3
"""Log learnings from A2LA A/B test to system database"""

import sys
sys.path.insert(0, "/home/al/AI_PROJECTS_SPACE/SYSTEM/state")

from db_utils import add_learning

# Learning 1: Gemini execution failure
add_learning(
    "Gemini cannot complete multi-step batch tasks (>10 items). Exhibits 1h+ startup overhead, loops after 5-10 operations, marks data Not Found prematurely. Use Claude for sustained execution despite higher cost.",
    "gotcha",
    confidence=5,
    tags=["gemini", "agent-routing", "batch-processing", "reliability", "execution-failure"]
)

# Learning 2: A2LA extraction technique
add_learning(
    "A2LA lab PIDs require cert-based searches (site:a2la.org cert_number). PDFs are unreadable via WebFetch. Successfully extracted 37/64 labs with high/med confidence. Cert search is most reliable method.",
    "technique",
    confidence=5,
    tags=["a2la", "web-scraping", "laboratory-data", "search-strategy", "certification"]
)

# Learning 3: Agent routing strategy
add_learning(
    "A/B test confirmed: Claude completes batch tasks 100%, Gemini fails at 60% with loops. Cost difference ($0.25 vs $0) irrelevant when including 1h 40m time waste. Always use Claude for >5 step tasks.",
    "strategy",
    confidence=5,
    tags=["agent-routing", "cost-optimization", "claude", "gemini", "ab-testing"]
)

print("\n✓ All learnings logged to system database")
print("✓ Location: /home/al/AI_PROJECTS_SPACE/SYSTEM/state/project.db")
