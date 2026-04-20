#!/usr/bin/env python3
"""
tstr.directory Main Scraper Orchestrator
Combines Google Maps API scraping with niche-specific scrapers
"""

import argparse
import logging
from datetime import datetime
from typing import Dict, Optional

# Import existing scrapers
from dual_scraper import DualPurposeScraper
from scrapers.a2la_materials import scrape_a2la_materials
from scrapers.epa_environmental_scraper import scrape_epa_environmental
from scrapers.oil_gas_playwright import scrape_contract_laboratory
from scrapers.tni_environmental import scrape_tni_environmental
from utils.logging_utils import json_error, json_info
from utils.retry_utils import retry_with_backoff

# Setup structured logging
logger = logging.getLogger(__name__)

class MainScraper:
    """
    Orchestrates all scraping operations for tstr.directory
    """

    def __init__(self):
        self.results = {
            "google_maps": {"listings": 0, "contacts": 0, "invalid_urls": 0},
            "oil_gas": {"listings": 0},
            "materials": {"listings": 0},
            "environmental": {"listings": 0, "tni": 0, "epa": 0},
            "total_listings": 0,
            "start_time": None,
            "end_time": None,
        }

    def run_google_maps_scraper(self, dry_run: bool = False, limit: Optional[int] = None) -> Dict:
        """
        Run the Google Maps API scraper for pharmaceutical and other categories
        """
        logger.info("=" * 70)
        logger.info("STARTING GOOGLE MAPS SCRAPER")
        logger.info("=" * 70)

        try:
            scraper = DualPurposeScraper()
            # Note: DualPurposeScraper might need refactoring to support limit/dry_run better
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

    def run_oil_gas_scraper(self, dry_run: bool = False, limit: Optional[int] = None) -> int:
        """
        Run the Oil & Gas testing scraper
        """
        logger.info("=" * 70)
        logger.info("STARTING OIL & GAS SCRAPER")
        logger.info("=" * 70)

        try:
            count = scrape_contract_laboratory(dry_run=dry_run, limit=limit)
            self.results["oil_gas"]["listings"] = count
            logger.info(f"Oil & Gas scraper completed: {count} listings")
            return count
        except Exception as e:
            logger.error(f"Oil & Gas scraper failed: {e}")
            return 0

    def run_materials_scraper(self, dry_run: bool = False, limit: Optional[int] = None) -> int:
        """
        Run the Materials testing scraper (A2LA)
        """
        logger.info("=" * 70)
        logger.info("STARTING MATERIALS SCRAPER")
        logger.info("=" * 70)

        try:
            count = scrape_a2la_materials(dry_run=dry_run, limit=limit)
            self.results["materials"]["listings"] = count
            logger.info(f"Materials scraper completed: {count} listings")
            return count
        except Exception as e:
            logger.error(f"Materials scraper failed: {e}")
            return 0

    def run_environmental_scraper(self, dry_run: bool = False, limit: Optional[int] = None, run_tni: bool = True, run_epa: bool = True) -> int:
        """
        Run the Environmental testing scrapers (TNI and EPA)
        """
        logger.info("=" * 70)
        logger.info("STARTING ENVIRONMENTAL SCRAPER")
        logger.info("=" * 70)

        total_count = 0
        
        if run_tni:
            try:
                logger.info("Running TNI Scraper...")
                tni_count = scrape_tni_environmental(dry_run=dry_run, limit=limit)
                self.results["environmental"]["tni"] = tni_count
                total_count += tni_count
                logger.info(f"TNI scraper completed: {tni_count} listings")
            except Exception as e:
                logger.error(f"TNI scraper failed: {e}")

        if run_epa:
            try:
                logger.info("Running EPA Scraper...")
                epa_count = scrape_epa_environmental(dry_run=dry_run, limit=limit)
                self.results["environmental"]["epa"] = epa_count
                total_count += epa_count
                logger.info(f"EPA scraper completed: {epa_count} listings")
            except Exception as e:
                logger.error(f"EPA scraper failed: {e}")

        self.results["environmental"]["listings"] = total_count
        return total_count

    def run(self, 
            dry_run: bool = False, 
            limit: Optional[int] = None,
            run_google: bool = True,
            run_oil_gas: bool = True,
            run_materials: bool = True,
            run_tni: bool = True,
            run_epa: bool = True) -> Dict:
        """
        Run selected scrapers in sequence
        """
        self.results["start_time"] = datetime.now()

        logger.info("🚀 STARTING tstr.directory MAIN SCRAPER")
        logger.info(f"Options: dry_run={dry_run}, limit={limit}")
        logger.info("=" * 80)

        if run_google:
            self.run_google_maps_scraper(dry_run=dry_run, limit=limit)

        if run_oil_gas:
            self.run_oil_gas_scraper(dry_run=dry_run, limit=limit)

        if run_materials:
            self.run_materials_scraper(dry_run=dry_run, limit=limit)

        if run_tni or run_epa:
            self.run_environmental_scraper(dry_run=dry_run, limit=limit, run_tni=run_tni, run_epa=run_epa)

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
        logger.info(f"Duration: {self.results['end_time'] - self.results['start_time']}")
        logger.info("=" * 80)

        return self.results


def main():
    """Main entry point for the scraper"""
    parser = argparse.ArgumentParser(description="tstr.directory Main Scraper Orchestrator")
    
    # Global options
    parser.add_argument("--dry-run", action="store_true", help="Run in dry-run mode (no database writes)")
    parser.add_argument("--limit", type=int, help="Limit number of listings per scraper")
    
    # Scraper selection
    group = parser.add_argument_group("Scraper Selection")
    group.add_argument("--all", action="store_true", help="Run all scrapers (default)")
    group.add_argument("--google", action="store_true", help="Run Google Maps scraper")
    group.add_argument("--oil-gas", action="store_true", help="Run Oil & Gas scraper")
    group.add_argument("--materials", action="store_true", help="Run Materials (A2LA) scraper")
    group.add_argument("--tni", action="store_true", help="Run TNI Environmental scraper")
    group.add_argument("--epa", action="store_true", help="Run EPA Environmental scraper")

    args = parser.parse_args()

    # Determine which scrapers to run
    # If no specific scraper is selected, run all
    all_selected = args.all or not any([args.google, args.oil_gas, args.materials, args.tni, args.epa])
    
    run_google = all_selected or args.google
    run_oil_gas = all_selected or args.oil_gas
    run_materials = all_selected or args.materials
    run_tni = all_selected or args.tni
    run_epa = all_selected or args.epa

    # Initialize and run
    main_scraper = MainScraper()
    results = main_scraper.run(
        dry_run=args.dry_run,
        limit=args.limit,
        run_google=run_google,
        run_oil_gas=run_oil_gas,
        run_materials=run_materials,
        run_tni=run_tni,
        run_epa=run_epa
    )

    # Print summary
    print("\n" + "=" * 80)
    print("SCRAPING SUMMARY")
    print("=" * 80)
    if run_google:
        print(f"Google Maps:   {results['google_maps']['listings']} listings, {results['google_maps']['contacts']} contacts")
    if run_oil_gas:
        print(f"Oil & Gas:     {results['oil_gas']['listings']} listings")
    if run_materials:
        print(f"Materials:     {results['materials']['listings']} listings")
    if run_tni or run_epa:
        print(f"Environmental: {results['environmental']['listings']} listings (TNI: {results['environmental']['tni']}, EPA: {results['environmental']['epa']})")
    
    print("-" * 40)
    print(f"TOTAL:         {results['total_listings']} listings")
    print(f"Duration:      {results['end_time'] - results['start_time']}")
    print("=" * 80)


if __name__ == "__main__":
    main()
