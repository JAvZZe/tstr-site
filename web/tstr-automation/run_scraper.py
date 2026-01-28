#!/usr/bin/env python3
"""
tstr.directory OCI Scraper Runner
Daily cron job that runs all scrapers
"""

import os
import sys
import logging
from datetime import datetime

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main_scraper import MainScraper

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("scraper.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


def main():
    """
    Main entry point for OCI cron job
    """
    logger.info("=" * 80)
    logger.info("STARTING tstr.directory OCI SCRAPER (CRON JOB)")
    logger.info(f"Time: {datetime.now()}")
    logger.info("=" * 80)

    try:
        # Initialize main scraper
        scraper = MainScraper()

        # Run all scrapers (production mode, no dry run)
        results = scraper.run_all_scrapers(dry_run=False)

        # Log final results
        logger.info("=" * 80)
        logger.info("CRON JOB COMPLETED SUCCESSFULLY")
        logger.info(f"Total listings scraped: {results['total_listings']}")
        logger.info(f"Duration: {results['end_time'] - results['start_time']}")
        logger.info("=" * 80)

        # Exit with success
        sys.exit(0)

    except Exception as e:
        logger.error(f"CRON JOB FAILED: {e}")
        logger.error("Full traceback:", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
