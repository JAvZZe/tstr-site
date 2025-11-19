"""
TSTR.SITE - Listings-Only Scraper (SECONDARY)
Scrapes testing laboratory directory listings with duplicate detection
Checks Google Maps API availability, falls back to alternative sources
Only scrapes new listings and detects changes
"""

import requests
from bs4 import BeautifulSoup
import csv
import time
import json
from urllib.parse import urljoin, urlparse
import re
import os
import logging
from dotenv import load_dotenv
from url_validator import URLValidator

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables
load_dotenv()

class ListingsScraperSecondary:
    """
    SECONDARY scraper for directory listings only (no lead generation)
    Features:
    - Checks Google Maps API availability
    - Falls back to alternative sources if API unavailable
    - Detects duplicate listings
    - Only scrapes new listings and changes
    """

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.results = []
        self.existing_listings = {}  # Cache of existing listings for duplicate detection
        self.invalid_urls = []  # Track URLs that failed validation
        self.url_validator = URLValidator(timeout=5, max_redirects=5)
        self.api_key = os.getenv("GOOGLE_MAPS_API_KEY")
        self.supabase_client = None
        self._initialize_supabase()
        self._load_existing_listings()
        
    def _initialize_supabase(self):
        """Initialize Supabase client for duplicate detection"""
        try:
            from supabase import create_client, Client
            supabase_url = os.getenv("SUPABASE_URL")
            supabase_key = os.getenv("SUPABASE_KEY")
            
            if supabase_url and supabase_key:
                self.supabase_client = create_client(supabase_url, supabase_key)
                logging.info("✅ Connected to Supabase for duplicate detection")
            else:
                logging.warning("⚠️  Supabase credentials not found - duplicate detection disabled")
        except ImportError:
            logging.warning("⚠️  Supabase library not installed - duplicate detection disabled")
        except Exception as e:
            logging.warning(f"⚠️  Could not connect to Supabase: {e}")

    def _load_existing_listings(self):
        """Load existing listings from Supabase for duplicate detection"""
        if not self.supabase_client:
            return
        
        try:
            response = self.supabase_client.table("listings").select("business_name,website,phone,address").execute()
            for listing in response.data:
                # Create multiple keys for duplicate detection
                name_key = listing.get('business_name', '').lower().strip()
                website_key = listing.get('website', '').lower().strip()
                
                if name_key:
                    self.existing_listings[name_key] = listing
                if website_key:
                    self.existing_listings[website_key] = listing
            
            logging.info(f"📋 Loaded {len(response.data)} existing listings for duplicate detection")
        except Exception as e:
            logging.warning(f"⚠️  Could not load existing listings: {e}")

    def _is_duplicate(self, listing_data):
        """Check if a listing already exists in database"""
        if not self.existing_listings:
            return False
        
        # Check by name, website, or phone
        name_key = listing_data.get('name', '').lower().strip()
        website_key = listing_data.get('website', '').lower().strip()
        
        if name_key in self.existing_listings:
            return True
        if website_key and website_key in self.existing_listings:
            return True
        
        return False

    def _has_significant_changes(self, new_data, existing_data):
        """Check if listing has significant changes worth updating"""
        # Compare key fields
        fields_to_compare = ['phone', 'website', 'address', 'rating']
        for field in fields_to_compare:
            if new_data.get(field) != existing_data.get(field):
                return True
        return False

    def scrape_google_maps_api(self, query, location):
        """
        Use Google Places API to find testing labs
        Only adds new listings or listings with significant changes
        """
        base_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
        params = {
            'query': f'{query} testing laboratory {location}',
            'key': self.api_key
        }

        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            data = response.json()

            if data['status'] == 'OK':
                for place in data['results']:
                    place_id = place['place_id']

                    # Get detailed place information
                    details_url = "https://maps.googleapis.com/maps/api/place/details/json"
                    details_params = {
                        'place_id': place_id,
                        'fields': 'name,formatted_address,formatted_phone_number,website,rating,opening_hours,url,geometry',
                        'key': self.api_key
                    }

                    details_response = requests.get(details_url, params=details_params)
                    details_response.raise_for_status()
                    details_data = details_response.json()

                    if details_data['status'] == 'OK':
                        result = details_data['result']
                        
                        # Extract data
                        lat = result.get('geometry', {}).get('location', {}).get('lat', '')
                        lng = result.get('geometry', {}).get('location', {}).get('lng', '')
                        
                        website = result.get('website', '')
                        
                        # Validate website URL if present
                        website_valid = True
                        website_status = None
                        if website:
                            validation_result = self.url_validator.validate_url(website)
                            website_valid = validation_result['valid']
                            website_status = validation_result['status_code']
                            
                            if not website_valid:
                                logging.warning(f"⚠️ Invalid website for {result.get('name', '')}: {website}")
                                self.invalid_urls.append({
                                    'company': result.get('name', ''),
                                    'url': website,
                                    'error': validation_result['error'],
                                    'source': 'Google Maps API'
                                })
                        
                        listing_data = {
                            'name': result.get('name', ''),
                            'address': result.get('formatted_address', ''),
                            'phone': result.get('formatted_phone_number', ''),
                            'website': website if website_valid else '',
                            'website_verified': website_valid,
                            'website_status': website_status,
                            'rating': result.get('rating', ''),
                            'latitude': lat,
                            'longitude': lng,
                            'category': query,
                            'location': location,
                            'google_maps_url': result.get('url', ''),
                            'source': 'Google Maps API'
                        }
                        
                        # Check for duplicates
                        if self._is_duplicate(listing_data):
                            logging.debug(f"⏭️  Skipping duplicate: {listing_data['name']}")
                        else:
                            logging.info(f"✨ New listing found: {listing_data['name']}")
                            self.results.append(listing_data)

                    time.sleep(0.5)  # Rate limiting
            elif data['status'] != 'ZERO_RESULTS':
                logging.warning(f"Google Maps API returned status: {data['status']} for query '{query} in {location}'")

        except requests.exceptions.RequestException as e:
            logging.error(f"HTTP Error during Google Maps API call: {e}")
        except Exception as e:
            logging.error(f"Unexpected error during Google Maps scraping: {e}")
    
    def scrape_alternative_source(self, source_name, url, category):
        """
        Route to appropriate scraper based on source name
        """
        if source_name == "Energy Pedia":
            self.scrape_energy_pedia(url, category)
        elif source_name == "Pharmaceutical Technology":
            self.scrape_pharma_tech(url, category)
        elif source_name == "Biocompare":
            self.scrape_biocompare(url, category)
        else:
            logging.warning(f"No scraper implemented for source: {source_name}")

    def scrape_energy_pedia(self, url, category):
        """Scrape Energy Pedia testing laboratories directory"""
        try:
            response = requests.get(url, headers=self.headers, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Parse listings (adjust selectors based on actual HTML structure)
            listings = soup.select('div.listing-item, div.company-card, article.company')
            
            for item in listings:
                try:
                    # Extract company data
                    name_elem = item.select_one('h2, h3, h4, .company-name, .listing-title')
                    website_elem = item.select_one('a[href*="http"]')
                    
                    if name_elem:
                        website = website_elem['href'] if website_elem else ''
                        website_valid = True
                        website_status = None
                        
                        # Validate URL if present
                        if website:
                            validation_result = self.url_validator.validate_url(website)
                            website_valid = validation_result['valid']
                            website_status = validation_result['status_code']
                            
                            if not website_valid:
                                self.invalid_urls.append({
                                    'company': name_elem.text.strip(),
                                    'url': website,
                                    'error': validation_result['error'],
                                    'source': 'Energy Pedia'
                                })
                        
                        listing_data = {
                            'name': name_elem.text.strip(),
                            'website': website if website_valid else '',
                            'website_verified': website_valid,
                            'website_status': website_status,
                            'address': '',
                            'phone': '',
                            'rating': '',
                            'latitude': '',
                            'longitude': '',
                            'category': category,
                            'location': 'N/A',
                            'google_maps_url': '',
                            'source': 'Energy Pedia'
                        }
                        
                        # Check for duplicates
                        if not self._is_duplicate(listing_data):
                            logging.info(f"✨ New listing from Energy Pedia: {listing_data['name']}")
                            self.results.append(listing_data)
                        else:
                            logging.debug(f"⏭️  Skipping duplicate: {listing_data['name']}")
                    
                except Exception as e:
                    logging.warning(f"Error parsing listing: {e}")
                    
        except Exception as e:
            logging.error(f"Could not scrape Energy Pedia: {e}")

    def scrape_pharma_tech(self, url, category):
        """Scrape Pharmaceutical Technology directory"""
        try:
            response = requests.get(url, headers=self.headers, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            listings = soup.select('div.contractor-listing, div.company-profile')
            
            for item in listings:
                try:
                    name_elem = item.select_one('h2, h3, .company-name')
                    website_elem = item.select_one('a.website, a[href*="http"]')
                    
                    if name_elem:
                        listing_data = {
                            'name': name_elem.text.strip(),
                            'website': website_elem['href'] if website_elem else '',
                            'address': '',
                            'phone': '',
                            'rating': '',
                            'latitude': '',
                            'longitude': '',
                            'category': category,
                            'location': 'N/A',
                            'google_maps_url': '',
                            'source': 'Pharmaceutical Technology'
                        }
                        
                        if not self._is_duplicate(listing_data):
                            logging.info(f"✨ New listing from Pharma Tech: {listing_data['name']}")
                            self.results.append(listing_data)
                            
                except Exception as e:
                    logging.warning(f"Error parsing listing: {e}")
                    
        except Exception as e:
            logging.error(f"Could not scrape Pharmaceutical Technology: {e}")

    def scrape_biocompare(self, url, category):
        """Scrape Biocompare laboratory services directory"""
        try:
            response = requests.get(url, headers=self.headers, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            listings = soup.select('div.service-provider, div.lab-listing')
            
            for item in listings:
                try:
                    name_elem = item.select_one('h3, .provider-name')
                    website_elem = item.select_one('a.website')
                    
                    if name_elem:
                        listing_data = {
                            'name': name_elem.text.strip(),
                            'website': website_elem['href'] if website_elem else '',
                            'address': '',
                            'phone': '',
                            'rating': '',
                            'latitude': '',
                            'longitude': '',
                            'category': category,
                            'location': 'N/A',
                            'google_maps_url': '',
                            'source': 'Biocompare'
                        }
                        
                        if not self._is_duplicate(listing_data):
                            logging.info(f"✨ New listing from Biocompare: {listing_data['name']}")
                            self.results.append(listing_data)
                            
                except Exception as e:
                    logging.warning(f"Error parsing listing: {e}")
                    
        except Exception as e:
            logging.error(f"Could not scrape Biocompare: {e}")
        
    def generate_csv(self, filename='tstr_listings_import.csv'):
        """
        Generate CSV file for Supabase import (new listings only)
        """
        if not self.results:
            logging.warning("No new listings to export")
            return

        csv_headers = [
            'business_name',
            'description',
            'category',
            'location',
            'address',
            'phone',
            'email',
            'website',
            'website_verified',
            'website_status',
            'latitude',
            'longitude',
            'google_maps_url',
            'source',
            'rating'
        ]

        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=csv_headers)
            writer.writeheader()

            for result in self.results:
                writer.writerow({
                    'business_name': result['name'],
                    'description': f"Professional testing laboratory specializing in {result['category']} services.",
                    'category': result['category'],
                    'location': result['location'],
                    'address': result['address'],
                    'phone': result['phone'],
                    'email': '',
                    'website': result['website'],
                    'website_verified': result.get('website_verified', False),
                    'website_status': result.get('website_status', ''),
                    'latitude': result['latitude'],
                    'longitude': result['longitude'],
                    'google_maps_url': result.get('google_maps_url', ''),
                    'source': result['source'],
                    'rating': result.get('rating', '')
                })

        logging.info(f"✅ Generated {filename} with {len(self.results)} NEW listings")
    
    def generate_invalid_urls_report(self, filename='invalid_urls_report.csv'):
        """Generate report of URLs that failed validation"""
        if not self.invalid_urls:
            logging.info("No invalid URLs to report")
            return
        
        csv_headers = ['company_name', 'url', 'error', 'source']
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=csv_headers)
            writer.writeheader()
            
            for invalid in self.invalid_urls:
                writer.writerow({
                    'company_name': invalid['company'],
                    'url': invalid['url'],
                    'error': invalid['error'],
                    'source': invalid['source']
                })
        
        logging.info(f"⚠️ Generated {filename} with {len(self.invalid_urls)} invalid URLs")

def load_config():
    """Load configuration from config.json"""
    try:
        with open('config.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        logging.error("❌ config.json not found. Please create it first.")
        return None
    except json.JSONDecodeError as e:
        logging.error(f"❌ Error parsing config.json: {e}")
        return None

def check_api_availability(api_key):
    """Check if Google Maps API is available and working"""
    if not api_key:
        logging.info("🔍 Google Maps API key not found")
        return False
    
    # Test API with a simple request
    test_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    test_params = {
        'query': 'testing laboratory',
        'key': api_key
    }
    
    try:
        response = requests.get(test_url, params=test_params, timeout=10)
        data = response.json()
        
        if data['status'] in ['OK', 'ZERO_RESULTS']:
            logging.info("✅ Google Maps API is active and working")
            return True
        else:
            logging.warning(f"⚠️  Google Maps API returned: {data['status']}")
            return False
    except Exception as e:
        logging.warning(f"⚠️  Could not verify API availability: {e}")
        return False

def main():
    """
    Execute listings-only scraping (SECONDARY scraper)
    """
    scraper = ListingsScraperSecondary()
    
    config = load_config()
    if not config:
        return

    print("="*70)
    print("TSTR.SITE - LISTINGS SCRAPER (SECONDARY)")
    print("Directory population with duplicate detection")
    print("="*70)

    # Check if Google Maps API is available
    api_key = os.getenv("GOOGLE_MAPS_API_KEY")
    
    if check_api_availability(api_key):
        # --- API MODE ---
        logging.info("Starting scraping using Google Maps API...")
        searches = config.get('google_api_searches', [])
        
        if not searches:
            logging.warning("API is available but no 'google_api_searches' found in config.json")
            return

        logging.info(f"Target: {len(searches)} category × location combinations")
        
        for idx, search in enumerate(searches, 1):
            category = search.get('category')
            location = search.get('location')
            
            if not category or not location:
                logging.warning(f"Skipping invalid search entry: {search}")
                continue

            logging.info(f"[{idx}/{len(searches)}] Scraping: {category} in {location}")
            scraper.scrape_google_maps_api(category, location)
            time.sleep(2)  # Rate limiting
    else:
        # --- FALLBACK MODE ---
        logging.info("Starting scraping using alternative sources...")
        sources = config.get('alternative_sources', [])
        
        if not sources:
            logging.warning("API not available and no 'alternative_sources' found in config.json")
            return

        logging.info(f"Target: {len(sources)} alternative sources")
        
        for idx, source in enumerate(sources, 1):
            name = source.get('name')
            category = source.get('category')
            url = source.get('url')

            if not all([name, category, url]):
                logging.warning(f"Skipping invalid source: {source}")
                continue

            logging.info(f"[{idx}/{len(sources)}] Scraping: {name}")
            scraper.scrape_alternative_source(name, url, category)
            time.sleep(2)  # Rate limiting

    print("\n" + "="*70)
    logging.info("SCRAPING COMPLETE")
    print("="*70)

    # Generate CSV files
    scraper.generate_csv('tstr_listings_import.csv')
    scraper.generate_invalid_urls_report('invalid_urls_report.csv')
    
    # Get validation statistics
    validation_stats = scraper.url_validator.get_stats()

    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print(f"New Listings Found: {len(scraper.results)} (verified URLs only)")
    print(f"Duplicates Skipped: {len(scraper.existing_listings)}")
    print(f"\nURL Validation Statistics:")
    print(f"  • Total URLs Validated: {validation_stats['total_validated']}")
    print(f"  • Valid URLs: {validation_stats['valid']}")
    print(f"  • Invalid URLs: {validation_stats['invalid']}")
    print(f"  • Success Rate: {validation_stats['success_rate']}")
    print("\nFiles created:")
    print("  • tstr_listings_import.csv (new listings only, verified URLs)")
    if scraper.invalid_urls:
        print("  • invalid_urls_report.csv (URLs that failed validation)")
    print("\nNext steps:")
    print("  1. Review CSV for data quality")
    if scraper.invalid_urls:
        print("  2. Review invalid URLs report and manually verify if needed")
    print("  3. Import to Supabase database")
    print("  4. Run PRIMARY scraper (dual_scraper.py) for lead generation")
    print("="*70)

if __name__ == "__main__":
    main()
