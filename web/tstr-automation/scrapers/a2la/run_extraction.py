#!/usr/bin/env python3
"""
Execute A2LA extraction with web search integration
This script coordinates with Claude's WebSearch tool to extract all 64 PIDs
"""

import json
from pathlib import Path
from typing import Dict, List, Optional

# Load extraction plan
PLAN_FILE = "/media/al/AI_DATA/AI_PROJECTS_SPACE/ACTIVE_PROJECTS/tstr-site-working/web/tstr-automation/scrapers/a2la/extraction_plan_64.json"

def load_plan() -> Dict:
    """Load the extraction plan."""
    with open(PLAN_FILE, 'r') as f:
        return json.load(f)

def load_gemini_results() -> Dict[str, Dict]:
    """Load Gemini's partial results."""
    gemini_file = "/media/al/AI_DATA/AI_PROJECTS_SPACE/ACTIVE_PROJECTS/tstr-site-working/web/tstr-automation/scrapers/a2la/claude_extraction.jsonl"
    gemini_data = {}

    if Path(gemini_file).exists():
        with open(gemini_file, 'r') as f:
            for line in f:
                if line.strip():
                    try:
                        record = json.loads(line)
                        gemini_data[record['pid']] = record
                    except:
                        pass

    return gemini_data

def generate_search_instructions() -> str:
    """Generate instructions for manual web search extraction."""
    plan = load_plan()
    gemini_data = load_gemini_results()

    instructions = []
    instructions.append("# A2LA LABORATORY EXTRACTION - SEARCH INSTRUCTIONS")
    instructions.append("\n## Task: Extract data for 64 PIDs using web search")
    instructions.append(f"\nGemini completed: 8 PIDs (use these as baseline)")
    instructions.append(f"Need to complete: 56 PIDs")
    instructions.append(f"Gemini failures to retry: 2 PIDs\n")

    # Group by status
    gemini_success = []
    gemini_failure = []
    no_data = []

    for pid in sorted(plan.keys()):
        data = plan[pid]
        cert = data["cert"]
        scope = data["scope"]

        if pid in gemini_data:
            result = gemini_data[pid]
            if result.get("org") == "Not Found":
                gemini_failure.append((pid, cert, scope))
            else:
                gemini_success.append((pid, cert, scope, result.get("org")))
        else:
            no_data.append((pid, cert, scope, data.get("category", "unknown")))

    # Print summary
    instructions.append("## GEMINI'S SUCCESSFUL EXTRACTIONS (8 PIDs):")
    instructions.append("These are baseline data we can verify or use directly:\n")
    for i, (pid, cert, scope, org) in enumerate(gemini_success, 1):
        instructions.append(f"{i}. {pid} | Cert: {cert} | Org: {org}")

    instructions.append("\n## GEMINI'S FAILURES TO RETRY (2 PIDs):")
    instructions.append("These reported 'Not Found' but may be findable with different searches:\n")
    for i, (pid, cert, scope) in enumerate(gemini_failure, 1):
        instructions.append(f"{i}. PID: {pid}")
        instructions.append(f"   Cert: {cert} | Scope: {scope}")
        instructions.append(f"   Search queries:")
        instructions.append(f"   a) site:customer.a2la.org \"{cert}\"")
        instructions.append(f"   b) site:a2la.org \"{cert}\"")
        instructions.append(f"   c) \"A2LA {cert}\" laboratory")
        instructions.append(f"   d) A2LA accreditation {scope}")

    instructions.append("\n## REMAINING EXTRACTIONS (56 PIDs):")
    instructions.append("Need full web search for organization + location\n")

    # Group by category
    by_category = {}
    for pid, cert, scope, category in no_data:
        if category not in by_category:
            by_category[category] = []
        by_category[category].append((pid, cert, scope))

    for category in sorted(by_category.keys()):
        items = by_category[category]
        instructions.append(f"\n### {category.upper()} ({len(items)} PIDs)")
        for i, (pid, cert, scope) in enumerate(items[:3], 1):  # Show first 3 per category
            instructions.append(f"{i}. Cert {cert}: {scope} | Search: site:a2la.org \"{cert}\"")
        if len(items) > 3:
            instructions.append(f"   ... and {len(items) - 3} more in this category")

    return "\n".join(instructions)

def main():
    # Generate search instructions
    instructions = generate_search_instructions()

    # Save instructions
    instr_file = "/media/al/AI_DATA/AI_PROJECTS_SPACE/ACTIVE_PROJECTS/tstr-site-working/web/tstr-automation/scrapers/a2la/EXTRACTION_INSTRUCTIONS.txt"
    Path(instr_file).write_text(instructions)

    print(instructions)
    print("\n" + "=" * 80)
    print(f"Instructions saved to: {instr_file}")
    print("=" * 80)

if __name__ == "__main__":
    main()
