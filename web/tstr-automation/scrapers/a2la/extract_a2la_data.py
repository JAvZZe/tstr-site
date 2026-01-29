#!/usr/bin/env python3
"""
A2LA Laboratory Data Extraction Script
Extracts lab information from first 10 A2LA accreditation PIDs
"""

import json
from pathlib import Path

# First 10 PIDs to process
PIDS = [
    "031C4AF0-B0DA-4AD7-BCDE-940DEECDE25E",  # Fire Resistance Construction
    "07745F0D-416C-4BB1-9CAC-3588866196F3",  # Cannabis Testing
    "09A84789-6D1A-4C35-B656-96FDBD68C0C6",  # Calibration
    "1106BCD8-2659-41F2-996B-E6A4BF0E302B",  # Intertek - Mechanical
    "11FE2BD5-8663-412B-A881-43F3F86414B8",  # Toys Testing
    "12A618F6-8114-4994-A522-26D9F1AA0986",  # Adhesives Plastics
    "12B5296B-1C26-4A2B-9834-86DED1337C27",  # Environmental
    "130248C5-EBD2-4BA1-8A85-DD99BC51104F",  # RF Microwave Calibration
    "13AE1E37-EF52-47AA-9BB4-048022563882",  # Element Materials - Aerospace
    "17806F1C-4EFA-484D-A34C-0C4438CE34EA",  # Mechanical
]

# Known certificate numbers and scopes from collected data
KNOWN_DATA = {
    "031C4AF0-B0DA-4AD7-BCDE-940DEECDE25E": {
        "cert": "6754.03",
        "scope": "Fire Resistance Construction"
    },
    "07745F0D-416C-4BB1-9CAC-3588866196F3": {
        "cert": "4356.02",
        "scope": "Cannabis Testing"
    },
    "09A84789-6D1A-4C35-B656-96FDBD68C0C6": {
        "cert": "1621.01",
        "scope": "Calibration"
    },
    "1106BCD8-2659-41F2-996B-E6A4BF0E302B": {
        "cert": "2310.02",
        "scope": "Intertek - Mechanical"
    },
    "11FE2BD5-8663-412B-A881-43F3F86414B8": {
        "cert": "2815.02",
        "scope": "Toys Testing"
    },
    "12A618F6-8114-4994-A522-26D9F1AA0986": {
        "cert": "0363.01",
        "scope": "Adhesives Plastics"
    },
    "12B5296B-1C26-4A2B-9834-86DED1337C27": {
        "cert": "0214.27",
        "scope": "Environmental"
    },
    "130248C5-EBD2-4BA1-8A85-DD99BC51104F": {
        "cert": "4950.01",
        "scope": "RF Microwave Calibration"
    },
    "13AE1E37-EF52-47AA-9BB4-048022563882": {
        "cert": "1719.06",
        "scope": "Element Materials - Aerospace"
    },
    "17806F1C-4EFA-484D-A34C-0C4438CE34EA": {
        "cert": "1176.02",
        "scope": "Mechanical"
    },
}

def build_extraction_plan():
    """Build detailed extraction plan with multiple search strategies."""
    return {
        "title": "A2LA Laboratory Data Extraction Plan",
        "objective": "Extract organization name, certificate details, location, and testing scope",
        "pids_count": 10,
        "search_strategies": [
            {
                "strategy": "Direct A2LA search",
                "format": "site:customer.a2la.org accreditationPID={PID}",
                "priority": 1,
                "rationale": "Official A2LA site has most complete data"
            },
            {
                "strategy": "Certificate number search",
                "format": 'site:customer.a2la.org "{CERT}"',
                "priority": 2,
                "rationale": "Certificate numbers are unique identifiers"
            },
            {
                "strategy": "Lab name with certification",
                "format": 'A2LA {CERT} accreditation',
                "priority": 3,
                "rationale": "Lab name + cert number combination"
            },
            {
                "strategy": "Scope-based search",
                "format": 'A2LA "{SCOPE}" accreditation',
                "priority": 4,
                "rationale": "Scope provides context for lab type"
            },
        ],
        "expected_data_fields": [
            "pid",
            "cert",
            "org",
            "location",
            "scope",
            "extraction_method",
            "confidence",
            "notes"
        ],
        "pids_to_extract": PIDS,
        "known_data": KNOWN_DATA
    }

def main():
    plan = build_extraction_plan()
    
    # Save extraction plan
    plan_path = Path("/media/al/AI_DATA/AI_PROJECTS_SPACE/ACTIVE_PROJECTS/tstr-site-working/web/tstr-automation/scrapers/a2la/extraction_plan.json")
    plan_path.write_text(json.dumps(plan, indent=2))
    print(f"Extraction plan saved to: {plan_path}")
    
    # Initialize extraction results structure
    results = {
        "project": "A2LA Laboratory Data Extraction",
        "batch_size": 10,
        "pids": PIDS,
        "known_data": KNOWN_DATA,
        "extraction_results": []
    }
    
    results_path = Path("/media/al/AI_DATA/AI_PROJECTS_SPACE/ACTIVE_PROJECTS/tstr-site-working/web/tstr-automation/scrapers/a2la/claude_extraction.jsonl")
    
    # Pre-populate with known data as baseline
    for pid in PIDS:
        if pid in KNOWN_DATA:
            results["extraction_results"].append({
                "pid": pid,
                "cert": KNOWN_DATA[pid]["cert"],
                "org": None,  # To be filled by web search
                "location": None,  # To be filled by web search
                "scope": KNOWN_DATA[pid]["scope"],
                "extraction_method": "web_search_required",
                "confidence": "medium",  # Will be refined
                "notes": "Certificate and scope known; need to find org and location"
            })
    
    # Save initialization
    with open(results_path, 'w') as f:
        for result in results["extraction_results"]:
            f.write(json.dumps(result) + '\n')
    
    print(f"Initialized extraction results: {results_path}")
    print(f"Total PIDs to process: {len(PIDS)}")
    print("\nPIDs with known data:")
    for pid in PIDS:
        if pid in KNOWN_DATA:
            print(f"  {pid}: {KNOWN_DATA[pid]['scope']} (Cert: {KNOWN_DATA[pid]['cert']})")

if __name__ == "__main__":
    main()
