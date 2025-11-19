#!/usr/bin/env python3
"""
Complete A2LA Laboratory Data Extraction for All 64 PIDs
Uses web search with multiple strategies to extract complete lab data
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Read PID lists
PIDS_FILE = "/home/al/AI PROJECTS SPACE/ACTIVE_PROJECTS/tstr-site-working/web/tstr-automation/scrapers/a2la/a2la_pids_final.txt"
COLLECTED_FILE = "/home/al/AI PROJECTS SPACE/ACTIVE_PROJECTS/tstr-site-working/web/tstr-automation/scrapers/a2la/a2la_pids_collected.txt"

def read_pids() -> List[str]:
    """Read 64 PIDs from file."""
    with open(PIDS_FILE, 'r') as f:
        pids = []
        for line in f:
            line = line.strip()
            if line and line != "":
                # PIDs are UUIDs, clean format
                pid = line.split('→')[-1].strip() if '→' in line else line.strip()
                if pid and len(pid) > 30:  # UUID length check
                    pids.append(pid)
        return pids

def read_collected_data() -> Dict[str, Dict[str, str]]:
    """Read certificate numbers and scopes from collected data."""
    data = {}
    current_section = None

    with open(COLLECTED_FILE, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                if line.startswith('# '):
                    current_section = line.replace('# ', '').lower()
                continue

            if '|' in line:
                parts = line.split('|')
                if len(parts) >= 2:
                    pid = parts[0].strip()
                    cert = parts[1].strip()
                    scope = parts[2].strip() if len(parts) > 2 else ""

                    data[pid] = {
                        "cert": cert,
                        "scope": scope,
                        "category": current_section
                    }

    return data

def parse_location(location_str: str) -> Tuple[Optional[str], Optional[str]]:
    """Parse location string into city and state."""
    if not location_str or location_str in ["Not Found", ""]:
        return None, None

    # Handle "City, State" format
    if ',' in location_str:
        parts = location_str.split(',')
        if len(parts) >= 2:
            city = parts[0].strip()
            state = parts[1].strip()
            return city, state

    return None, None

def build_search_queries(pid: str, cert: str, scope: str) -> List[Dict[str, str]]:
    """Build list of search queries for a PID."""
    queries = []

    # Strategy 1: Direct A2LA site search with certificate
    if cert:
        queries.append({
            "query": f'site:customer.a2la.org "{cert}"',
            "strategy": "a2la_direct_cert",
            "order": 1
        })
        queries.append({
            "query": f'site:a2la.org "{cert}"',
            "strategy": "a2la_site_cert",
            "order": 2
        })

    # Strategy 2: A2LA search with PID
    queries.append({
        "query": f'site:a2la.org "{pid}"',
        "strategy": "a2la_pid",
        "order": 3
    })

    # Strategy 3: Certificate with A2LA context
    if cert:
        queries.append({
            "query": f'"A2LA" "{cert}" laboratory accreditation',
            "strategy": "a2la_context",
            "order": 4
        })

    # Strategy 4: Scope-based search if available
    if scope:
        # Extract category (first part before dash/space)
        scope_parts = scope.split('-')[0].strip() if '-' in scope else scope.split()[0]
        queries.append({
            "query": f'A2LA "{scope_parts}" laboratory accreditation',
            "strategy": "scope_search",
            "order": 5
        })

    return sorted(queries, key=lambda x: x['order'])

def get_gemini_data() -> Dict[str, Dict]:
    """Load Gemini's partial extraction results."""
    gemini_data = {}
    gemini_file = "/home/al/AI PROJECTS SPACE/ACTIVE_PROJECTS/tstr-site-working/web/tstr-automation/scrapers/a2la/claude_extraction.jsonl"

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

def create_extraction_record(
    pid: str,
    cert: str,
    org: Optional[str],
    city: Optional[str],
    state: Optional[str],
    scope: str,
    confidence: str,
    notes: str = ""
) -> Dict:
    """Create a complete extraction record."""
    return {
        "pid": pid,
        "cert": cert,
        "org": org or "",
        "city": city or "",
        "state": state or "",
        "country": "USA",
        "scope": scope,
        "confidence": confidence,
        "notes": notes
    }

def main():
    print("=" * 80)
    print("A2LA LABORATORY DATA EXTRACTION - ALL 64 PIDs")
    print("=" * 80)

    # Read all data
    pids = read_pids()
    collected = read_collected_data()
    gemini_data = get_gemini_data()

    print(f"\nLoaded {len(pids)} PIDs")
    print(f"Collected data for {len(collected)} PIDs")
    print(f"Gemini's partial results: {len(gemini_data)} records\n")

    # Build mapping for search queries
    extraction_plan = {}

    for i, pid in enumerate(pids, 1):
        if pid not in collected:
            continue

        cert = collected[pid].get("cert", "")
        scope = collected[pid].get("scope", "")
        category = collected[pid].get("category", "")

        queries = build_search_queries(pid, cert, scope)

        extraction_plan[pid] = {
            "index": i,
            "cert": cert,
            "scope": scope,
            "category": category,
            "queries": queries,
            "gemini_result": gemini_data.get(pid),
            "needs_extraction": True
        }

        # Check if Gemini already found it
        if pid in gemini_data:
            gemini_org = gemini_data[pid].get("org", "")
            if gemini_org and gemini_org != "Not Found":
                extraction_plan[pid]["needs_extraction"] = False

    # Save extraction plan
    plan_file = "/home/al/AI PROJECTS SPACE/ACTIVE_PROJECTS/tstr-site-working/web/tstr-automation/scrapers/a2la/extraction_plan_64.json"
    with open(plan_file, 'w') as f:
        # Serialize queries for JSON
        plan_for_json = {}
        for pid, data in extraction_plan.items():
            plan_for_json[pid] = {
                "index": data["index"],
                "cert": data["cert"],
                "scope": data["scope"],
                "category": data["category"],
                "queries": data["queries"],
                "needs_extraction": data["needs_extraction"]
            }
        f.write(json.dumps(plan_for_json, indent=2))

    print(f"Extraction plan saved to: {plan_file}")
    print(f"Total PIDs in plan: {len(extraction_plan)}")
    print(f"PIDs needing extraction: {sum(1 for p in extraction_plan.values() if p['needs_extraction'])}")
    print(f"PIDs already found by Gemini: {sum(1 for p in extraction_plan.values() if not p['needs_extraction'])}")

    # Print Gemini's failures (to retry)
    print("\n" + "=" * 80)
    print("GEMINI'S REPORTED FAILURES (need retry):")
    print("=" * 80)
    retry_count = 0
    for pid, data in extraction_plan.items():
        if data["needs_extraction"]:
            gemini_result = data["gemini_result"]
            if gemini_result and gemini_result.get("org") == "Not Found":
                retry_count += 1
                print(f"{retry_count}. PID: {pid}")
                print(f"   Cert: {data['cert']}")
                print(f"   Scope: {data['scope']}")
                print(f"   Queries to try: {len(data['queries'])}")

    print(f"\nTotal Gemini failures to retry: {retry_count}")
    print("\n" + "=" * 80)
    print("READY FOR CLAUDE EXTRACTION")
    print("=" * 80)
    print(f"\nNext step: Run web searches for each PID using the queries above")
    print(f"Output file: a2la_claude_complete.jsonl")

if __name__ == "__main__":
    main()
