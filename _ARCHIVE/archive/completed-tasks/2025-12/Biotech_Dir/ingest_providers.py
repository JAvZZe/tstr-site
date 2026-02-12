import sqlite3
import re
import os

# Configuration
DB_PATH = os.path.expanduser("~/memory/db/tstr.db")
README_PATH = "awesome-biotech-niche-testing-README.md"

def parse_readme():
    """
    Parses the README.md file to extract provider data using Regex.
    Returns a list of dicts: {'name': str, 'url': str, 'category': str, 'desc': str}
    """
    if not os.path.exists(README_PATH):
        print(f"Error: {README_PATH} not found.")
        return []

    with open(README_PATH, "r", encoding="utf-8") as f:
        lines = f.readlines()

    providers = []
    current_category = "Uncategorized"
    
    # Regex patterns
    # Matches: ## Category Name
    category_pattern = re.compile(r"^##\s+(.+)") 
    # Matches: - [**Name**](Url) - Description
    provider_pattern = re.compile(r"^-\s+\[\*\*(.+?)\*\*\]\((.+?)\)\s+-\s+(.+)")

    for line in lines:
        line = line.strip()
        
        # Check for Category Header
        cat_match = category_pattern.match(line)
        if cat_match:
            current_category = cat_match.group(1).split("(")[0].strip() # Clean "Biotech (CROs)" -> "Biotech"
            continue

        # Check for Provider Entry
        prov_match = provider_pattern.match(line)
        if prov_match:
            name = prov_match.group(1)
            url = prov_match.group(2)
            # Description is captured but we might not need it for the DB primary columns, 
            # but good to have available.
            
            providers.append({
                "name": name,
                "website": url,
                "category": current_category
            })
            
    return providers

def sync_to_db(providers):
    """
    Inserts providers into the SQLite DB.
    Uses 'INSERT OR IGNORE' logic based on Website URL to prevent duplicates.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. Ensure we have a UNIQUE index on website to make sure we don't duplicate leads
    # This is a 'Schema Migration' step applied automatically.
    cursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_website ON providers(website)")
    
    added_count = 0
    
    print(f"Processing {len(providers)} providers...")

    for p in providers:
        try:
            # First Principle: Idempotency. Running this script 100 times should not break the DB.
            cursor.execute('''
                INSERT OR IGNORE INTO providers (name, website, category, status, tier)
                VALUES (?, ?, ?, 'unclaimed', 'free')
            ''', (p['name'], p['website'], p['category']))
            
            if cursor.rowcount > 0:
                added_count += 1
                print(f"[+] Added: {p['name']}")
            else:
                # Optional: Update category if it changed, but usually we skip
                pass
                
        except sqlite3.Error as e:
            print(f"Database error on {p['name']}: {e}")

    conn.commit()
    conn.close()
    print(f"--- Sync Complete. Added {added_count} new providers. ---")

if __name__ == "__main__":
    print("Starting Ingestion...")
    data = parse_readme()
    if data:
        sync_to_db(data)
