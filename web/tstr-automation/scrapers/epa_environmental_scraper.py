#!/usr/bin/env python3
"""
EPA Approved Environmental Testing Labs Scraper
Extracts EPA approved environmental testing laboratories from EPA EMC directory
Data source: https://www.epa.gov/emc/epa-approved-test-labs-and-third-party-certifiers-table
"""

import logging
import os
import re
import sys
from typing import Dict, List, Optional
from urllib.parse import urljoin

from bs4 import BeautifulSoup

# Add parent directory to path to import base_scraper
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from base_scraper import BaseNicheScraper

logger = logging.getLogger(__name__)


class EPAEnvironmentalScraper(BaseNicheScraper):
    """
    Scraper for EPA approved environmental testing labs inheriting from BaseNicheScraper
    """

    def __init__(self, dry_run: bool = False):
        super().__init__(
            category_slug="environmental-testing",
            source_name="EPA EMC Directory",
            rate_limit_seconds=1.0,
            dry_run=dry_run,
        )
        self.base_url = "https://www.epa.gov"
        self.source_url = "https://www.epa.gov/emc/epa-approved-test-labs-and-third-party-certifiers-table"
        self.labs_cache = []

    def get_listing_urls(self, limit: Optional[int] = None) -> List[str]:
        """
        Fetch the main table and return placeholder URLs for each lab
        """
        logger.info(f"Fetching EPA labs from {self.source_url}...")
        
        try:
            response = self.session.get(self.source_url)
            response.raise_for_status()
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(response.content, "html.parser")

            # Find the table with lab data
            table = soup.find("table")
            if not table:
                logger.error("No table found on EPA page")
                return []

            # Skip header row
            rows = table.find_all("tr")[1:]
            
            labs = []
            for i, row in enumerate(rows):
                if limit and len(labs) >= limit:
                    break
                    
                cells = row.find_all("td")
                if len(cells) < 6:
                    continue

                # Only include test labs
                is_test_lab = cells[4].get_text(strip=True).lower() == "yes"
                if not is_test_lab:
                    continue

                company_name = cells[0].get_text(strip=True)
                
                # Handle website link
                website_cell = cells[1]
                website = ""
                if website_cell.find("a"):
                    website = website_cell.find("a")["href"]
                    if not website.startswith("http"):
                        website = urljoin(self.base_url, website)

                # Address
                address = cells[2].get_text(strip=True)

                # Contact info
                contact_cell = cells[3]
                contact_text = contact_cell.get_text(separator="\n", strip=True)
                contact_lines = contact_text.split("\n")
                
                contact_email = ""
                contact_phone = ""
                for line in contact_lines:
                    line = line.strip()
                    if "@" in line and not contact_email:
                        email_match = re.search(r"[\w\.-]+@[\w\.-]+\.\w+", line)
                        if email_match:
                            contact_email = email_match.group()
                    elif re.search(r"\(\d{3}\)", line) or re.search(r"\d{3}-\d{3}", line):
                        contact_phone = line

                # Approval expiration
                expires = cells[6].get_text(strip=True) if len(cells) > 6 else ""

                lab_data = {
                    "index": i,
                    "business_name": company_name,
                    "website": website,
                    "address": address,
                    "phone": contact_phone,
                    "email": contact_email,
                    "approval_expires": expires,
                    "is_third_party": cells[5].get_text(strip=True).lower() == "yes"
                }
                
                labs.append(lab_data)
                
            self.labs_cache = labs
            logger.info(f"Found {len(labs)} EPA approved labs")
            
            # Return placeholder URLs using index
            return [f"{self.source_url}#epa-{lab['index']}" for lab in labs]

        except Exception as e:
            logger.error(f"Error fetching EPA labs: {e}")
            return []

    def extract_standard_fields(self, soup: BeautifulSoup, url: str) -> Dict:
        """Extract standard fields from cache"""
        index_match = re.search(r"#epa-(\d+)", url)
        if not index_match:
            return {}
            
        index = int(index_match.group(1))
        lab_data = next((lab for lab in self.labs_cache if lab["index"] == index), None)
        
        if not lab_data:
            return {}
            
        fields = {
            "business_name": lab_data["business_name"],
            "description": f"EPA approved environmental testing laboratory. Approval expires: {lab_data['approval_expires']}",
            "address": lab_data["address"],
            "phone": lab_data["phone"],
            "email": lab_data["email"],
            "website": lab_data["website"],
            "location_id": None
        }
        
        # Link location if not dry run
        if fields["address"] and self.location_parser:
            fields["location_id"] = self.location_parser.parse_and_link(
                address=fields["address"]
            )
            
        return fields

    def extract_custom_fields(self, soup: BeautifulSoup, url: str) -> Dict:
        """Extract custom fields"""
        # EPA approved labs usually focus on these
        return {
            "compliance_standards": ["EPA"],
            "field_lab_services": ["Lab Only"],
            "test_types": ["Air Quality", "Emissions Testing"]
        }

    def scrape_listing(self, url: str) -> bool:
        """Override to use cache instead of fetching"""
        try:
            standard_fields = self.extract_standard_fields(None, url)
            if not standard_fields:
                return False
                
            custom_fields = self.extract_custom_fields(None, url)
            
            listing_id = self.save_listing(standard_fields, custom_fields, url)
            if listing_id:
                self.stats["listings_scraped"] += 1
                return True
            return False
        except Exception as e:
            logger.error(f"Error scraping EPA listing {url}: {e}")
            self.stats["listings_failed"] += 1
            return False


def scrape_epa_environmental(dry_run: bool = False, limit: Optional[int] = None) -> int:
    """Wrapper for main_scraper orchestration"""
    scraper = EPAEnvironmentalScraper(dry_run=dry_run)
    scraper.run(limit=limit, dry_run=dry_run)
    return scraper.stats["listings_saved"]


def main():
    import argparse
    parser = argparse.ArgumentParser(description="EPA Environmental Scraper")
    parser.add_argument("--limit", type=int, help="Limit number of listings")
    parser.add_argument("--dry-run", action="store_true", help="Dry run mode")
    args = parser.parse_args()
    
    scraper = EPAEnvironmentalScraper(dry_run=args.dry_run)
    scraper.run(limit=args.limit, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
