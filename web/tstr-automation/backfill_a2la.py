import logging
import argparse
import re
from typing import List, Dict
from difflib import SequenceMatcher
from scrapers.a2la_materials import A2LAMaterialsScraper

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("A2LABackfill")

class A2LABackfiller:
    def __init__(self):
        self.scraper = A2LAMaterialsScraper()
        
    def find_lab_pids_by_name(self, name: str) -> List[Dict]:
        """Wrapper for A2LA search"""
        return self.scraper._search_by_keyword(name)

    def run_backfill(self, limit: int = 10):
        # 1. Fetch listings from database that need enrichment
        # Filter for Materials Testing category and those not already processed by this script
        logger.info(f"Fetching up to {limit} listings for backfill...")
        
        # We target listings in Materials Testing (3f99a311-9bd4-4366-b9bc-49860ad931d5)
        # that haven't been successfully enriched yet
        response = self.scraper.supabase.table("listings").select("id, business_name, website").eq("category_id", "3f99a311-9bd4-4366-b9bc-49860ad931d5").or_("source_script.neq.backfill_a2la.py,source_script.is.null").limit(limit).execute()
        
        listings = response.data
        if not listings:
            logger.info("No listings found needing backfill.")
            return

        logger.info(f"Found {len(listings)} listings to process.")

        for listing in listings:
            lid = listing['id']
            name = listing['business_name']
            website = listing.get('website', '') or ''
            
            # 1. Determine the A2LA URL
            url = None
            if 'a2la.org' in website:
                url = website
                logger.info(f"Using existing A2LA URL for {name}: {url}")
            else:
                # Try to find by name with fuzzy matching
                logger.info(f"Searching A2LA for: {name}")
                
                # 1. Clean the name for better search results
                # Normalize common accents
                norm_name = name.replace('ü', 'u').replace('Ü', 'U').replace('ö', 'o').replace('Ö', 'O').replace('ä', 'a').replace('Ä', 'A')
                
                # Remove common business suffixes and special characters
                clean_name = re.sub(r' (Inc|LLC|Ltd|Limited|Laboratories|Laboratory|Lab|Corp|Corporation|Pty|Pvt|Group|Services|Testing|International)\.?$', '', norm_name, flags=re.I).strip()
                clean_name = re.sub(r'[^\w\s]', ' ', clean_name).strip()
                
                # Build search variations
                search_queries = [norm_name, clean_name]
                words = clean_name.split()
                if len(words) >= 2:
                    search_queries.append(' '.join(words[:2]))
                if len(words) >= 3:
                    search_queries.append(' '.join(words[:3]))
                
                final_results = []
                
                for query in search_queries:
                    if not query or len(query) < 3:
                        continue
                    logger.debug(f"Trying search query: {query}")
                    results = self.find_lab_pids_by_name(query)
                    if results:
                        for res in results:
                            res_name = res['labName'].replace('ü', 'u').replace('Ü', 'U') # Normalize result name too
                            # Scoring
                            score = SequenceMatcher(None, clean_name.lower(), res_name.lower()).ratio()
                            
                            # Boost if clean name is exactly in result name (or vice versa)
                            if clean_name.lower() in res_name.lower() or res_name.lower() in clean_name.lower():
                                score = max(score, 0.85)
                            
                            # Additional boost for first word match
                            res_words = res_name.split()
                            if words and res_words and words[0].lower() == res_words[0].lower():
                                score += 0.05
                                
                            final_results.append((score, res))
                
                if final_results:
                    # Sort by score descending
                    final_results.sort(key=lambda x: x[0], reverse=True)
                    highest_score, best_match = final_results[0]
                    
                    # Only accept matches above threshold (0.80 for more strict matching)
                    if highest_score >= 0.80:
                        lab_pid = best_match['labPID']
                        url = f"https://customer.a2la.org/index.cfm?event=directory.detail&labPID={lab_pid}"
                        logger.info(f"Found match ({highest_score:.2f}) on A2LA: {best_match['labName']} (PID: {lab_pid})")
                    else:
                        logger.warning(f"No high-confidence match found on A2LA for: {name} (Highest: {highest_score:.2f})")
                        continue
                else:
                    logger.warning(f"No search results on A2LA for variations of: {name}")
                    continue

            if not url:
                continue

            # 2. Scrape detail page and update
            logger.info(f"Processing: {name} ({lid}) at {url}")
            soup = self.scraper.fetch_page(url)
            if soup:
                custom_fields = self.scraper.extract_custom_fields(soup, url)
                
                # Prepare standard fields for update (especially source_script)
                standard_fields = {
                    "business_name": name,
                    "website": url,
                    "source_script": "backfill_a2la.py"
                }
                
                # Save/Update
                self.scraper.save_listing(standard_fields, custom_fields, url)
                logger.info(f"Successfully enriched {name}")
            else:
                logger.error(f"Failed to fetch detail page for {name}")

def main():
    parser = argparse.ArgumentParser(description="Backfill A2LA custom fields")
    parser.add_argument("--limit", type=int, default=10, help="Number of listings to process")
    args = parser.parse_args()
    
    backfiller = A2LABackfiller()
    backfiller.run_backfill(limit=args.limit)

if __name__ == "__main__":
    main()
