#!/usr/bin/env python3
# ruff: noqa: E402
"""
ScopeMatch.eu Pan-European Aggregator Scraper
Standardized to use BaseNicheScraper architecture.
Utilizes the ScopeMatch API (v1) to fetch verified ISO 17025 labs.
Coverage: UK (UKAS), Germany (DAkkS), France (COFRAC), Netherlands (RvA), Italy (ACCREDIA), Spain (ENAC).
"""

import os
import sys
import logging
import time
from typing import Dict, List, Optional

import requests

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from base_scraper import BaseNicheScraper

logger = logging.getLogger(__name__)


class ScopeMatchScraper(BaseNicheScraper):
    """
    Scraper for European labs using the ScopeMatch.eu API
    """

    def __init__(self, country: Optional[str] = None, dry_run: bool = False):
        super().__init__(
            category_slug="materials-testing", # Primary category for these labs
            source_name="ScopeMatch.eu",
            rate_limit_seconds=3.0,
            dry_run=dry_run
        )
        self.api_base = "https://scopematch.eu/api/v1"
        self.country = country # Filter by country (e.g., 'DE', 'GB')

    def fetch_api(self, url: str, params: Optional[Dict] = None) -> Optional[Dict]:
        """
        Fetch from API with retry on 429
        """
        retries = 3
        backoff = 5
        
        for i in range(retries):
            try:
                response = requests.get(url, params=params, timeout=20)
                if response.status_code == 429:
                    logger.warning(f"Rate limited (429). Retrying in {backoff}s... (Attempt {i+1}/{retries})")
                    time.sleep(backoff)
                    backoff *= 2
                    continue
                response.raise_for_status()
                return response.json()
            except Exception:
                if i < retries - 1:
                    continue
                raise
        return None

    def get_listing_urls(self, limit: Optional[int] = None) -> List[str]:
        """
        Fetch lab detail API URLs from the paginated list endpoint
        """
        detail_urls = []
        page = 1
        per_page = 25
        
        params = {
            "per_page": per_page,
            "status": "active"
        }
        if self.country:
            params["country"] = self.country

        logger.info(f"Fetching lab list from ScopeMatch API (Country: {self.country or 'All'})")

        while True:
            if limit and len(detail_urls) >= limit:
                break
                
            params["page"] = page
            data = self.fetch_api(f"{self.api_base}/labs", params=params)
            if not data:
                break
                
            labs = data.get("data", [])
            if not labs:
                break
                
            for lab in labs:
                if limit and len(detail_urls) >= limit:
                    break
                # The 'self' link in the list response is the detail API endpoint
                detail_url = lab.get("_links", {}).get("self")
                if detail_url:
                    detail_urls.append(detail_url)
            
            logger.info(f"Collected {len(detail_urls)} labs (Page {page})")
            
            if page >= data.get("meta", {}).get("total_pages", 0):
                break
                
            page += 1
            time.sleep(self.rate_limit_seconds)
                
        return detail_urls

    def scrape_listing(self, api_url: str) -> bool:
        """
        Fetch and parse lab details from the API
        """
        logger.info(f"Fetching detail from API: {api_url}")
        
        try:
            lab = self.fetch_api(api_url)
            if not lab:
                return False
            
            # 1. Prepare Standard Fields
            name = lab.get("name")
            street = lab.get("street_address", "")
            city = lab.get("city", "")
            postcode = lab.get("postcode", "")
            country = lab.get("country", "")
            
            # Construct full address for location parsing
            address_parts = [p for p in [street, city, postcode, country] if p]
            full_address = ", ".join(address_parts)
            
            standard_fields = {
                "business_name": name,
                "description": f"ISO 17025 Accredited Laboratory verified by {lab.get('accreditation_body')}.",
                "address": full_address,
                "website": lab.get("website_url") or lab.get("_links", {}).get("html"),
                "phone": lab.get("phone") or "",
                "email": lab.get("email") or "",
                "latitude": lab.get("latitude"),
                "longitude": lab.get("longitude"),
                "region": "eu",
                "source_script": "scopematch_eu.py"
            }
            
            # Parse and link location
            if full_address and self.location_parser:
                standard_fields["location_id"] = self.location_parser.parse_and_link(full_address)
            
            # 2. Prepare Custom Fields
            custom_fields = {
                "cert_number": lab.get("accreditation_number"),
                "accreditation_body": lab.get("accreditation_body"),
                "scope_url": lab.get("scope_document_url"),
                "source_slug": lab.get("slug")
            }
            
            # 3. Save to Database
            self.save_listing(standard_fields, custom_fields, lab.get("_links", {}).get("html"))
            return True
            
        except Exception as e:
            logger.error(f"Error processing lab {api_url}: {e}")
            return False

    def extract_custom_fields(self, soup, url):
        # API-based scraper doesn't use soup
        return {}


def main():
    import argparse
    parser = argparse.ArgumentParser(description='ScopeMatch European Scraper')
    parser.add_argument('--country', type=str, help='2-letter country code (DE, GB, FR, IT, ES, NL)')
    parser.add_argument('--limit', type=int, default=5, help='Limit labs')
    parser.add_argument('--dry-run', action='store_true', help='Dry run')
    args = parser.parse_args()

    scraper = ScopeMatchScraper(country=args.country, dry_run=args.dry_run)
    scraper.run(limit=args.limit)

if __name__ == "__main__":
    main()
