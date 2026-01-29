#!/usr/bin/env python3
"""
tstr.directory Main Scraper Orchestrator
Combines Google Maps API scraping with niche-specific scrapers
"""

import logging
from utils.logging_utils import json_info, json_error
from utils.retry_utils import retry_with_backoff
from datetime import datetime
from typing import Dict

# Import existing scrapers
from dual_scraper import DualPurposeScraper
from scrapers.oil_gas_playwright import scrape_contract_laboratory
from scrapers.a2la_materials import scrape_a2la_materials
from scrapers.tni_environmental import scrape_tni_environmental

# Setup structured logging
logger = logging.getLogger(__name__)
# Use json_info/json_error for structured logs


class MainScraper:
    """
    Orchestrates all scraping operations for tstr.directory
    """

    def __init__(self):
        self.results = {
            "google_maps": {"listings": 0, "contacts": 0, "invalid_urls": 0},
            "oil_gas": {"listings": 0},
            "materials": {"listings": 0},
            "environmental": {"listings": 0},
            "total_listings": 0,
            "start_time": None,
            "end_time": None,
        }

    def run_google_maps_scraper(self) -> Dict:
        """
        Run the Google Maps API scraper for pharmaceutical and other categories
        """
        logger.info("=" * 70)
        logger.info("STARTING GOOGLE MAPS SCRAPER")
        logger.info("=" * 70)

        try:
            scraper = DualPurposeScraper()
            results = retry_with_backoff(scraper.run_all_searches)
        
            self.results["google_maps"] = {
                "listings": len(results.get("listings", [])),
                "contacts": len(results.get("contacts", [])),
                "invalid_urls": len(results.get("invalid_urls", [])),
            }
        
            json_info(f"Google Maps scraper completed: {self.results['google_maps']}")
            return results
        
        except Exception as e:
            json_error(f"Google Maps scraper failed: {e}")
            return {}

    def run_oil_gas_scraper(self, dry_run: bool = False, limit: int = None) -> int:
        """
        Run the Oil & Gas testing scraper
        """
        logger.info("=" * 70)
        logger.info("STARTING OIL & GAS SCRAPER")
        logger.info("=" * 70)

        try:
            listings = scrape_contract_laboratory(dry_run=dry_run, limit=limit)
            count = len(listings)
            self.results["oil_gas"]["listings"] = count
            logger.info(f"Oil & Gas scraper completed: {count} listings")
            return count
        except Exception as e:
            logger.error(f"Oil & Gas scraper failed: {e}")
            return 0

    def run_materials_scraper(self) -> int:
        """
        Run the Materials testing scraper (A2LA)
        """
        logger.info("=" * 70)
        logger.info("STARTING MATERIALS SCRAPER")
        logger.info("=" * 70)

        try:
            count = scrape_a2la_materials()
            self.results["materials"]["listings"] = count
            logger.info(f"Materials scraper completed: {count} listings")
            return count
        except Exception as e:
            logger.error(f"Materials scraper failed: {e}")
            return 0

    def run_environmental_scraper(self) -> int:
        """
        Run the Environmental testing scraper (TNI)
        """
        logger.info("=" * 70)
        logger.info("STARTING ENVIRONMENTAL SCRAPER")
        logger.info("=" * 70)

        try:
            count = scrape_tni_environmental()
            self.results["environmental"]["listings"] = count
            logger.info(f"Environmental scraper completed: {count} listings")
            return count
        except Exception as e:
            logger.error(f"Environmental scraper failed: {e}")
            return 0

    def run_all_scrapers(self, dry_run: bool = False) -> Dict:
        """
        Run all scrapers in sequence
        """
        self.results["start_time"] = datetime.now()

        logger.info("🚀 STARTING tstr.directory MAIN SCRAPER")
        logger.info("=" * 80)

        # Run Google Maps scraper (pharma, etc.)
        self.run_google_maps_scraper()

        # Run niche-specific scrapers
        self.run_oil_gas_scraper(dry_run=dry_run)
        self.run_materials_scraper()
        self.run_environmental_scraper()

        # Calculate totals
        self.results["total_listings"] = sum(
            [
                self.results["google_maps"]["listings"],
                self.results["oil_gas"]["listings"],
                self.results["materials"]["listings"],
                self.results["environmental"]["listings"],
            ]
        )

        self.results["end_time"] = datetime.now()

        logger.info("=" * 80)
        logger.info("✅ SCRAPING COMPLETED")
        logger.info(f"Total listings scraped: {self.results['total_listings']}")
        logger.info(
            f"Duration: {self.results['end_time'] - self.results['start_time']}"
        )
        logger.info("=" * 80)

        return self.results


def main():
    """
    Main entry point for the scraper
    """
    import argparse

    parser = argparse.ArgumentParser(description="tstr.directory Main Scraper")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run in dry-run mode (no database writes)",
    )
    parser.add_argument(
        "--limit", type=int, help="Limit number of listings per scraper (for testing)"
    )

    args = parser.parse_args()

    # Initialize main scraper
    main_scraper = MainScraper()

    # Run all scrapers
    results = main_scraper.run_all_scrapers(dry_run=args.dry_run)

    # Print summary
    print("\n" + "=" * 80)
    print("SCRAPING SUMMARY")
    print("=" * 80)
    print(
        f"Google Maps: {results['google_maps']['listings']} listings, {results['google_maps']['contacts']} contacts"
    )
    print(f"Oil & Gas: {results['oil_gas']['listings']} listings")
    print(f"Materials: {results['materials']['listings']} listings")
    print(f"Environmental: {results['environmental']['listings']} listings")
    print(f"Total: {results['total_listings']} listings")
    print(f"Duration: {results['end_time'] - results['start_time']}")
    print("=" * 80)


if __name__ == "__main__":
    main()
