
import json
import os
import subprocess

# CONFIG
PASTE_FILE = "/home/al/.gemini/antigravity/brain/2382ce1c-5eab-4fa7-97b6-5596e6bbaad6/linkedin_raw_paste.txt"
GET_LISTINGS_SCRIPT = "get_current_listings.py"
OUTPUT_FILE = "new_listings_to_add.json"

# CATEGORY MAPPING (Keyword -> Slug)
CATEGORY_MAP = {
    "Biotechnology": "biotech-testing",
    "Pharmaceutical": "pharmaceutical-testing", 
    "Oil and Gas": "oil-gas-testing",
    "Environmental": "environmental-testing",
    "Hydrogen": "hydrogen-infrastructure-testing",
    "Renewable": "environmental-testing", # Fallback
    "Chemical": "materials-testing",
    "Materials": "materials-testing",
    "Semiconductor": "appliances-electrical-electronics-testing", # Closest
    "Medical Device": "medical-device-testing", # Wait, we only have 6 categories? 
    # Current active: biotech-testing, environmental-testing, hydrogen-infrastructure-testing, 
    # materials-testing, oil-gas-testing, pharmaceutical-testing
    # We need to map strict to these.
}

DEFAULT_CATEGORY = "materials-testing" # Fallback

def get_db_listings():
    """Run the existing script to get current DB state."""
    print("Fetching current listings from DB...")
    # We assume get_current_listings.py prints JSON to stdout or saves to file?
    # Let's check get_current_listings.py content first? 
    # We'll try running it and capturing output.
    try:
        result = subprocess.run(
            ['python3', GET_LISTINGS_SCRIPT],
            capture_output=True,
            text=True,
            cwd="/media/al/AI_DATA/AI_PROJECTS_SPACE/ACTIVE_PROJECTS/TSTR-site/tstr-site-working/web/tstr-automation"
        )
        if result.returncode != 0:
            print(f"Error running script: {result.stderr}")
            return []
        
        # Try to parse stdout as JSON
        try:
            return json.loads(result.stdout)
        except (json.JSONDecodeError, TypeError):
            print("Could not parse script output as JSON. Checking for file output...")
            # If script saves to file, we'd need to know where. 
            # For now, let's assume valid JSON output or empty list & warn.
            print(f"Raw output: {result.stdout[:200]}...")
            return []

    except Exception as e:
        print(f"Execution error: {e}")
        return []

def parse_paste(file_path):
    """Parse the raw LinkedIn text."""
    companies = []
    with open(file_path, 'r') as f:
        lines = f.readlines()

    # Heuristic parsing based on the paste format:
    # Logo for [Name]
    # [Name]
    # [Industry] · [Location]
    # Followed [Date]
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        if line.startswith("Logo for "):
            # Next line is usually the Name
            if i + 1 < len(lines):
                name = lines[i+1].strip()
                industry_loc = lines[i+2].strip() if i+2 < len(lines) else ""
                
                # Split Industry / Location
                parts = industry_loc.split(' · ')
                industry = parts[0] if len(parts) > 0 else "Unknown"
                location = parts[1] if len(parts) > 1 else "Unknown"
                
                companies.append({
                    "name": name,
                    "linkedin_industry": industry,
                    "location": location,
                    "source": "LinkedIn Following"
                })
                i += 3 # Skip processed lines
            else:
                i += 1
        else:
            i += 1
            
    return companies

def map_category(industry):
    """Map LinkedIn industry to TSTR category."""
    industry_lower = industry.lower()
    
    if "bio" in industry_lower or "pharma" in industry_lower:
        if "pharma" in industry_lower:
            return "pharmaceutical-testing"
        return "biotech-testing"
    
    if "oil" in industry_lower or "gas" in industry_lower or "energy" in industry_lower:
        return "oil-gas-testing"
        
    if "hydrogen" in industry_lower:
        return "hydrogen-infrastructure-testing"
        
    if "environ" in industry_lower:
        return "environmental-testing"
        
    return "materials-testing" # Generic fallback

def main():
    # 1. Get Baseline
    # db_listings = get_db_listings() # Commented out for now until we confirm script output format
    # Simulating DB for now or relying on fuzzy match in next step
    
    # 2. Parse Paste
    if not os.path.exists(PASTE_FILE):
        print("Paste file not found!")
        return

    linkedin_companies = parse_paste(PASTE_FILE)
    print(f"Found {len(linkedin_companies)} companies in paste.")
    
    # 3. Transform
    new_entries = []
    for co in linkedin_companies:
        cat = map_category(co['linkedin_industry'])
        new_entries.append({
            "company_name": co['name'],
            "primary_category": cat,
            "description": f"{co['linkedin_industry']} company based in {co['location']}. Source: LinkedIn Following.",
            "status": "pending_approval",
            "source_data": co
        })

    # 4. Save
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(new_entries, f, indent=2)
    
    print(f"Saved {len(new_entries)} processed entries to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
