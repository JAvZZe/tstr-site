#!/usr/bin/env python3
# ruff: noqa: E402
"""
GAC (GCC Accreditation Center) Scraper
Standardized to use BaseNicheScraper architecture.
Extracts accredited labs in the GCC (Saudi Arabia, UAE, Qatar, Oman, Bahrain, Kuwait, Yemen).
Source: http://www.gcc-accreditation.org/public/cabs
"""

import os
import sys
import logging
import re
import time
from typing import Dict, List, Optional

from bs4 import BeautifulSoup
import requests

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from base_scraper import BaseNicheScraper

logger = logging.getLogger(__name__)


class GACMiddleEastScraper(BaseNicheScraper):
    """
    Scraper for GCC accredited labs from GAC
    """

    def __init__(self, dry_run: bool = False):
        super().__init__(
            category_slug="materials-testing", # General category for now
            source_name="GCC Accreditation Center",
            rate_limit_seconds=1.5,
            dry_run=dry_run
        )
        self.base_url = "http://www.gcc-accreditation.org"
        self.directory_url = f"{self.base_url}/public/cabs"

    def get_listing_urls(self, limit: Optional[int] = None) -> List[str]:
        """
        GAC uses a standard paginated table. We'll return page URLs or synthetic IDs.
        Since all data is in the table, we'll return page URLs and extract in scrape_listing.
        """
        urls = []
        # Total ~460 bodies, ~10-20 per page. Let's do first 5 pages for PoC.
        for page_num in range(1, 6):
            if limit and len(urls) >= limit:
                break
            # Note: The Exa highlights showed ?page_no=3
            page_url = f"{self.directory_url}?page_no={page_num}"
            logger.info(f"Fetching GAC page {page_num}: {page_url}")
            
            try:
                response = requests.get(page_url, timeout=20)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, "html.parser")
                
                # Find all rows in the table
                rows = soup.find_all("tr")[1:] # Skip header
                if not rows:
                    break
                    
                for i in range(len(rows)):
                    if limit and len(urls) >= limit:
                        break
                    # We'll use a synthetic URL to trigger row-level extraction
                    urls.append(f"{page_url}#row-{i}")
                
                logger.info(f"Collected {len(rows)} items from page {page_num}")
                time.sleep(self.rate_limit_seconds)

            except Exception as e:
                logger.error(f"Error fetching GAC page {page_num}: {e}")
                break
                
        return urls

    def scrape_listing(self, url: str) -> bool:
        """
        Extract data from the table row identified by the fragment
        """
        base_page_url = url.split('#')[0]
        row_idx = int(url.split('#row-')[1])
        
        try:
            response = requests.get(base_page_url, timeout=20)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            
            rows = soup.find_all("tr")[1:]
            if row_idx >= len(rows):
                return False
                
            cols = rows[row_idx].find_all("td")
            if len(cols) < 3:
                return False
                
            # Column mapping based on Exa highlights:
            # 0: Domain/Code, 1: CAB Name, 2: Country, 3: Status, ...
            code = cols[0].get_text(strip=True)
            name = cols[1].get_text(strip=True)
            country = cols[2].get_text(strip=True)
            status = cols[3].get_text(strip=True) if len(cols) > 3 else "Active"
            
            if status.lower() not in ["active", "suspended"]:
                logger.info(f"Skipping {name} (Status: {status})")
                return False

            # GAC names often have trailing periods or whitespace
            name = name.strip().rstrip('.')

            standard_fields = {
                "business_name": name,
                "description": f"GAC Accredited Laboratory in {country}. Accreditation Code: {code}.",
                "website": url, # Use the unique row-level URL as primary identifier if no external website
                "phone": "",
                "email": "",
                "address": country,
                "region": "middle-east",
                "source_script": "gac_middle_east.py"
            }

            # Link location
            if self.location_parser:
                standard_fields["location_id"] = self.location_parser.parse_and_link(country)

            custom_fields = {
                "cert_number": code,
                "accreditation_body": "GAC",
                "accreditation_type": "Testing" if "ATL" in code else ("Calibration" if "APC" in code else "Other")
            }

            # Check for schedule links
            schedule_link = cols[-1].find("a")
            if schedule_link:
                href = schedule_link.get("href")
                if href:
                    if not href.startswith("http"):
                        href = f"{self.base_url}{href}"
                    custom_fields["scope_url"] = href

            self.save_listing(standard_fields, custom_fields, url)
            return True
            
        except Exception as e:
            logger.error(f"Error parsing GAC lab row {row_idx}: {e}")
            return False

    def extract_custom_fields(self, soup: BeautifulSoup, url: str) -> Dict:
        return {}


def main():
    import argparse
    parser = argparse.ArgumentParser(description='GAC Middle East Scraper')
    parser.add_argument('--limit', type=int, default=10, help='Limit labs')
    parser.add_argument('--dry-run', action='store_true', help='Dry run')
    args = parser.parse_args()

    scraper = GACMiddleEastScraper(dry_run=args.dry_run)
    scraper.run(limit=args.limit)

if __name__ == "__main__":
    main()
