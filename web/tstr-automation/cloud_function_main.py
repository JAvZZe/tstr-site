"""
Google Cloud Function Entry Points
Wraps existing scrapers for cloud deployment
"""

import functions_framework
import json
import logging
from datetime import datetime

# Import existing scrapers
try:
    from dual_scraper import DualPurposeScraper, load_config as load_dual_config
    from scraper import ListingsScraperSecondary, load_config as load_secondary_config
except ImportError:
    # For local testing
    import sys
    sys.path.append('.')
    from dual_scraper import DualPurposeScraper, load_dual_config
    from scraper import ListingsScraperSecondary, load_secondary_config

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@functions_framework.http
def run_primary_scraper(request):
    """
    HTTP Cloud Function for primary scraper (dual_scraper.py)
    
    Triggers:
    - Cloud Scheduler (daily at 2am)
    - Manual HTTP request
    
    Returns:
    - JSON with scraping results and statistics
    """
    try:
        logger.info("="*70)
        logger.info("STARTING PRIMARY SCRAPER (CLOUD FUNCTION)")
        logger.info("="*70)
        
        # Initialize scraper
        scraper = DualPurposeScraper()
        
        # Load config
        searches = load_dual_config()
        if not searches:
            return {
                'status': 'error',
                'message': 'Could not load config.json'
            }, 500
        
        logger.info(f"Loaded {len(searches)} search configurations")
        
        # Run scraping
        for idx, search in enumerate(searches, 1):
            category = search.get('category')
            location = search.get('location')
            
            if not category or not location:
                logger.warning(f"Skipping invalid search: {search}")
                continue
            
            logger.info(f"[{idx}/{len(searches)}] Scraping: {category} in {location}")
            scraper.scrape_google_maps_api(category, location)
        
        # Generate reports (these will be saved to Cloud Storage if needed)
        logger.info("Generating reports...")
        scraper.generate_directory_csv('tstr_directory_import.csv')
        scraper.generate_sales_contacts_csv('tstr_sales_leads.csv')
        scraper.generate_invalid_urls_report('invalid_urls_report.csv')
        
        # Get statistics
        validation_stats = scraper.url_validator.get_stats()
        
        # Prepare response
        response = {
            'status': 'success',
            'timestamp': datetime.now().isoformat(),
            'results': {
                'directory_listings': len(scraper.directory_listings),
                'sales_contacts': len(scraper.sales_contacts),
                'invalid_urls': len(scraper.invalid_urls)
            },
            'validation_stats': validation_stats,
            'message': f"Scraped {len(scraper.directory_listings)} listings successfully"
        }
        
        logger.info("="*70)
        logger.info("PRIMARY SCRAPER COMPLETED")
        logger.info(f"Results: {json.dumps(response['results'], indent=2)}")
        logger.info("="*70)
        
        return response, 200
        
    except Exception as e:
        logger.error(f"Error in primary scraper: {e}", exc_info=True)
        return {
            'status': 'error',
            'message': str(e),
            'timestamp': datetime.now().isoformat()
        }, 500


@functions_framework.http
def run_secondary_scraper(request):
    """
    HTTP Cloud Function for secondary scraper (scraper.py)
    
    Triggers:
    - Cloud Scheduler (weekly)
    - Manual HTTP request
    
    Returns:
    - JSON with scraping results and statistics
    """
    try:
        logger.info("="*70)
        logger.info("STARTING SECONDARY SCRAPER (CLOUD FUNCTION)")
        logger.info("="*70)
        
        # Initialize scraper
        scraper = ListingsScraperSecondary()
        
        # Load config
        config = load_secondary_config()
        if not config:
            return {
                'status': 'error',
                'message': 'Could not load config.json'
            }, 500
        
        # Check if Google Maps API is available
        api_key = scraper.api_key
        
        if api_key:
            # Run with Google Maps API
            logger.info("Using Google Maps API")
            searches = config.get('google_api_searches', [])
            
            for idx, search in enumerate(searches, 1):
                category = search.get('category')
                location = search.get('location')
                
                if not category or not location:
                    continue
                
                logger.info(f"[{idx}/{len(searches)}] Scraping: {category} in {location}")
                scraper.scrape_google_maps_api(category, location)
        else:
            # Fallback to alternative sources
            logger.info("Using alternative sources (no API key)")
            sources = config.get('alternative_sources', [])
            
            for idx, source in enumerate(sources, 1):
                name = source.get('name')
                category = source.get('category')
                url = source.get('url')
                
                if not all([name, category, url]):
                    continue
                
                logger.info(f"[{idx}/{len(sources)}] Scraping: {name}")
                scraper.scrape_alternative_source(name, url, category)
        
        # Generate reports
        logger.info("Generating reports...")
        scraper.generate_csv('tstr_listings_import.csv')
        scraper.generate_invalid_urls_report('invalid_urls_report.csv')
        
        # Get statistics
        validation_stats = scraper.url_validator.get_stats()
        
        # Prepare response
        response = {
            'status': 'success',
            'timestamp': datetime.now().isoformat(),
            'results': {
                'new_listings': len(scraper.results),
                'duplicates_skipped': len(scraper.existing_listings),
                'invalid_urls': len(scraper.invalid_urls)
            },
            'validation_stats': validation_stats,
            'message': f"Found {len(scraper.results)} new listings"
        }
        
        logger.info("="*70)
        logger.info("SECONDARY SCRAPER COMPLETED")
        logger.info(f"Results: {json.dumps(response['results'], indent=2)}")
        logger.info("="*70)
        
        return response, 200
        
    except Exception as e:
        logger.error(f"Error in secondary scraper: {e}", exc_info=True)
        return {
            'status': 'error',
            'message': str(e),
            'timestamp': datetime.now().isoformat()
        }, 500


@functions_framework.http
def run_cleanup(request):
    """
    HTTP Cloud Function for database cleanup
    
    Validates existing URLs in database and moves invalid ones to research
    
    Triggers:
    - Manual HTTP request
    - Cloud Scheduler (monthly)
    
    Returns:
    - JSON with cleanup results
    """
    try:
        logger.info("="*70)
        logger.info("STARTING DATABASE CLEANUP (CLOUD FUNCTION)")
        logger.info("="*70)
        
        from cleanup_invalid_urls import URLCleanup
        
        # Initialize cleanup
        cleanup = URLCleanup()
        
        # Fetch all listings
        listings = cleanup.fetch_all_listings()
        
        if not listings:
            return {
                'status': 'success',
                'message': 'No listings found in database'
            }, 200
        
        # Validate all URLs
        cleanup.validate_listings(listings)
        
        # Generate reports
        cleanup.generate_report()
        
        # Get mode from request (default: move to research)
        request_json = request.get_json(silent=True)
        mode = request_json.get('mode', '2') if request_json else '2'
        
        # Execute cleanup based on mode
        if mode == '1':
            # Mark invalid
            count = cleanup.mark_invalid_urls()
            action = f"Marked {count} URLs as invalid"
        elif mode == '2':
            # Move to research
            count = cleanup.move_to_pending_research()
            action = f"Moved {count} URLs to pending research"
        else:
            # Report only
            count = 0
            action = "Report generated, no changes made"
        
        # Prepare response
        response = {
            'status': 'success',
            'timestamp': datetime.now().isoformat(),
            'results': {
                'total_checked': len(listings),
                'valid': len(cleanup.valid_listings),
                'invalid': len(cleanup.invalid_listings),
                'action_taken': action
            },
            'validation_stats': cleanup.url_validator.get_stats()
        }
        
        logger.info("="*70)
        logger.info("DATABASE CLEANUP COMPLETED")
        logger.info(f"Results: {json.dumps(response['results'], indent=2)}")
        logger.info("="*70)
        
        return response, 200
        
    except Exception as e:
        logger.error(f"Error in cleanup: {e}", exc_info=True)
        return {
            'status': 'error',
            'message': str(e),
            'timestamp': datetime.now().isoformat()
        }, 500


# For local testing
if __name__ == "__main__":
    from flask import Flask, request as flask_request
    
    app = Flask(__name__)
    
    @app.route('/primary', methods=['GET', 'POST'])
    def test_primary():
        return run_primary_scraper(flask_request)
    
    @app.route('/secondary', methods=['GET', 'POST'])
    def test_secondary():
        return run_secondary_scraper(flask_request)
    
    @app.route('/cleanup', methods=['GET', 'POST'])
    def test_cleanup():
        return run_cleanup(flask_request)
    
    print("Starting local test server...")
    print("Test endpoints:")
    print("  - http://localhost:8080/primary")
    print("  - http://localhost:8080/secondary")
    print("  - http://localhost:8080/cleanup")
    
    app.run(host='0.0.0.0', port=8080, debug=True)
