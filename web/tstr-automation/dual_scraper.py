"""
tstr.directory - Dual-Purpose Scraper
1. Scrape testing labs for directory listings (company info)
2. Scrape decision-maker contacts for sales outreach (names, emails, LinkedIn)
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
from url_validator import URLValidator

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DualPurposeScraper:
    """
    Collects both:
    1. Company data for directory population
    2. Decision-maker contacts for sales outreach
    """
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.directory_listings = []
        self.sales_contacts = []
        self.invalid_urls = []  # Track URLs that failed validation
        self.url_validator = URLValidator(timeout=5, max_redirects=5)
        self.api_key = os.getenv("GOOGLE_MAPS_API_KEY")
        if not self.api_key:
            raise ValueError("API key not found. Please set the GOOGLE_MAPS_API_KEY environment variable.")
        
    def scrape_google_maps_api(self, query, location):
        """
        Use Google Places API for company listings
        """
        base_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
        
        params = {
            'query': f'{query} testing laboratory {location}',
            'key': self.api_key
        }
        
        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()  # Raise an exception for bad status codes
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
                        company_name = result.get('name', '')
                        website = result.get('website', '')
                        
                        # Extract lat/lng
                        lat = result.get('geometry', {}).get('location', {}).get('lat', '')
                        lng = result.get('geometry', {}).get('location', {}).get('lng', '')

                        # Validate website URL before adding listing
                        website_valid = True
                        website_status = None
                        if website:
                            logging.info(f"Validating website: {website}")
                            validation_result = self.url_validator.validate_url(website)
                            website_valid = validation_result['valid']
                            website_status = validation_result['status_code']
                            
                            if not website_valid:
                                logging.warning(f"⚠️ Invalid website URL for {company_name}: {website} - {validation_result['error']}")
                                self.invalid_urls.append({
                                    'company': company_name,
                                    'url': website,
                                    'error': validation_result['error'],
                                    'source': 'Google Maps API'
                                })
                        
                        # Only add listing if website is valid or no website provided
                        if website_valid or not website:
                            self.directory_listings.append({
                                'name': company_name,
                                'address': result.get('formatted_address', ''),
                                'phone': result.get('formatted_phone_number', ''),
                                'website': website if website_valid else '',
                                'website_status': website_status,
                                'website_verified': website_valid,
                                'rating': result.get('rating', ''),
                                'latitude': lat,
                                'longitude': lng,
                                'category': query,
                                'location': location,
                                'google_maps_url': result.get('url', ''),
                                'source': 'Google Maps API'
                            })
                        
                            # If website exists and is valid, scrape for decision-maker contacts
                            if website and website_valid:
                                time.sleep(1)  # Rate limiting
                                self.scrape_website_for_contacts(website, company_name, query)
                        else:
                            logging.warning(f"⏭️ Skipping listing {company_name} - invalid website URL")
                        
                    time.sleep(0.5)  # Rate limiting between API calls
            elif data['status'] != 'ZERO_RESULTS':
                logging.warning(f"Google Maps API returned status: {data['status']} for query '{query} in {location}'")

        except requests.exceptions.RequestException as e:
            logging.error(f"HTTP Error during Google Maps API call: {e}")
        except Exception as e:
            logging.error(f"An unexpected error occurred during Google Maps scraping: {e}")
    
    def scrape_website_for_contacts(self, website, company_name, category):
        """
        Scrape company website for decision-maker contacts using more robust parsing.
        Target pages: About Us, Team, Contact, Leadership
        """
        try:
            target_pages = ['/about', '/about-us', '/team', '/leadership', '/contact', '/contact-us']
            # Always check homepage
            urls_to_check = {website.rstrip('/')}
            for page in target_pages:
                urls_to_check.add(website.rstrip('/') + page)

            contacts_found = []
            
            for url in urls_to_check:
                try:
                    response = requests.get(url, headers=self.headers, timeout=10)
                    response.raise_for_status()
                    soup = BeautifulSoup(response.content, 'html.parser')

                    # 1. Find mailto links (most reliable)
                    emails = {a['href'].replace('mailto:', '') for a in soup.find_all('a', href=re.compile(r'^mailto:'))}
                    
                    # 2. Find emails in text as a fallback
                    emails.update(re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', soup.get_text()))

                    # 3. Find LinkedIn profiles
                    linkedin_profiles = {a['href'] for a in soup.find_all('a', href=re.compile(r'linkedin\.com/in/'))}

                    # 4. Find names and titles (more context-aware)
                    names_and_titles = []
                    # Look for job titles and try to find a name nearby
                    job_titles = ['CEO', 'CTO', 'CFO', 'COO', 'Director', 'Manager', 'President', 'VP', 'Vice President']
                    for title in job_titles:
                        # Find elements containing the job title
                        title_elements = soup.find_all(string=re.compile(r'\b' + title + r'\b', re.IGNORECASE))
                        for element in title_elements:
                            # Search in the parent element for a plausible name (two capitalized words)
                            parent = element.find_parent()
                            if parent:
                                potential_names = re.findall(r'\b([A-Z][a-z]+(?:\s[A-Z][a-z]+)+)\b', parent.get_text())
                                if potential_names:
                                    # Assume the first found name is the right one for this context
                                    names_and_titles.append({'name': potential_names[0].strip(), 'title': title})

                    if emails or names_and_titles or linkedin_profiles:
                        contacts_found.append({
                            'page': url,
                            'emails': list(emails)[:5],
                            'names_titles': names_and_titles[:5],
                            'linkedin': list(linkedin_profiles)[:3]
                        })
                    
                    time.sleep(1)
                except requests.exceptions.RequestException:
                    continue
                except Exception:
                    continue

            if contacts_found:
                best_contact = self.extract_best_contact(contacts_found, company_name)
                if best_contact:
                    self.sales_contacts.append({
                        'company': company_name,
                        'website': website,
                        'category': category,
                        'contact_name': best_contact.get('name', ''),
                        'title': best_contact.get('title', ''),
                        'email': best_contact.get('email', ''),
                        'linkedin': best_contact.get('linkedin', ''),
                        'confidence': best_contact.get('confidence', 'low')
                    })
                    
        except Exception as e:
            logging.warning(f"Could not scrape website {website}: {e}")
    
    def extract_best_contact(self, contacts_data, company_name):
        """
        Analyze scraped contacts and identify the best decision-maker.
        Prioritizes contacts where name, title, and email/linkedin are found together.
        """
        all_emails = set()
        all_linkedin = set()
        all_names_titles = []

        for page_data in contacts_data:
            all_emails.update(page_data.get('emails', []))
            all_linkedin.update(page_data.get('linkedin', []))
            all_names_titles.extend(page_data.get('names_titles', []))

        # Filter out generic emails
        filtered_emails = {e for e in all_emails if not any(x in e.lower() for x in ['info@', 'contact@', 'support@', 'sales@'])}

        if not filtered_emails and not all_names_titles:
            return None

        # High confidence: A name and title pair is found, and we have a non-generic email.
        if all_names_titles and filtered_emails:
            contact = all_names_titles[0] # Take the first identified person
            return {
                'name': contact['name'],
                'title': contact['title'],
                'email': list(filtered_emails)[0],
                'linkedin': list(all_linkedin)[0] if all_linkedin else '',
                'confidence': 'high'
            }

        # Medium confidence: We have a name/title but only a generic email or no email.
        if all_names_titles:
            contact = all_names_titles[0]
            return {
                'name': contact['name'],
                'title': contact['title'],
                'email': list(all_emails)[0] if all_emails else '',
                'linkedin': list(all_linkedin)[0] if all_linkedin else '',
                'confidence': 'medium'
            }
            
        # Low confidence: We only have emails.
        if filtered_emails:
            return {
                'name': '',
                'title': 'Decision Maker (unverified)',
                'email': list(filtered_emails)[0],
                'linkedin': '',
                'confidence': 'low'
            }

        return None
    
    def generate_directory_csv(self, filename='directory_listings.csv'):
        """
        Generate CSV for WordPress Directorist import
        """
        if not self.directory_listings:
            logging.info("No directory listings to export")
            return
            
        csv_headers = [
            'listing_title',
            'listing_content', 
            'listing_category',
            'listing_location',
            'address',
            'phone',
            'email',
            'website',
            'website_verified',
            'website_status',
            'listing_img',
            'latitude',
            'longitude'
        ]
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=csv_headers)
            writer.writeheader()
            
            for result in self.directory_listings:
                writer.writerow({
                    'listing_title': result['name'],
                    'listing_content': f"Professional testing laboratory specializing in {result['category']} services. Rated {result.get('rating', 'N/A')} stars.",
                    'listing_category': result['category'],
                    'listing_location': result['location'],
                    'address': result['address'],
                    'phone': result['phone'],
                    'email': '',  # Usually not in Maps API
                    'website': result['website'],
                    'website_verified': result.get('website_verified', False),
                    'website_status': result.get('website_status', ''),
                    'listing_img': '',
                    'latitude': result['latitude'],
                    'longitude': result['longitude']
                })
        
        logging.info(f"✓ Generated {filename} with {len(self.directory_listings)} listings")
    
    def generate_sales_contacts_csv(self, filename='sales_leads.csv'):
        """
        Generate CSV of decision-maker contacts for outreach
        """
        if not self.sales_contacts:
            logging.info("No sales contacts to export")
            return
            
        csv_headers = [
            'company_name',
            'website',
            'category',
            'contact_name',
            'title',
            'email',
            'linkedin_url',
            'confidence',
            'outreach_status',
            'notes'
        ]
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=csv_headers)
            writer.writeheader()
            
            for contact in self.sales_contacts:
                writer.writerow({
                    'company_name': contact['company'],
                    'website': contact['website'],
                    'category': contact['category'],
                    'contact_name': contact['contact_name'],
                    'title': contact['title'],
                    'email': contact['email'],
                    'linkedin_url': contact['linkedin'],
                    'confidence': contact['confidence'],
                    'outreach_status': 'Not Contacted',
                    'notes': ''
                })
        
        logging.info(f"✓ Generated {filename} with {len(self.sales_contacts)} sales leads")
    
    def generate_invalid_urls_report(self, filename='invalid_urls_report.csv'):
        """
        Generate report of URLs that failed validation
        """
        if not self.invalid_urls:
            logging.info("No invalid URLs to report")
            return
        
        csv_headers = [
            'company_name',
            'url',
            'error',
            'source'
        ]
        
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
    """Loads the search configuration from config.json."""
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
            if 'searches' not in config:
                raise ValueError("Config file must contain a 'searches' key.")
            return config['searches']
    except FileNotFoundError:
        logging.error("Error: config.json not found. Please create it.")
        return None
    except json.JSONDecodeError:
        logging.error("Error: Could not decode config.json. Please check for syntax errors.")
        return None
    except ValueError as e:
        logging.error(f"Configuration Error: {e}")
        return None

def check_api_availability(api_key):
    """
    Checks if the Google Maps API is available and the key is valid.
    Makes a single, low-cost request to the API.
    """
    if not api_key:
        return False
    
    test_url = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        'place_id': 'ChIJN1t_tDeuEmsRUsoyG83frY4', # A known valid Place ID (Google Sydney)
        'key': api_key
    }
    try:
        response = requests.get(test_url, params=params, timeout=5)
        if response.status_code == 200:
            logging.info("Google Maps API is available.")
            return True
        else:
            logging.warning(f"Google Maps API check failed with status {response.status_code}. Falling back to alternative sources.")
            return False
    except requests.exceptions.RequestException as e:
        logging.error(f"Google Maps API check failed: {e}. Falling back to alternative sources.")
        return False

def scrape_energy_pedia(url, category, scraper_instance):
    """
    Scrapes business listings from the Energy Pedia directory.
    This is an example implementation for the fallback mechanism.
    """
    logging.info(f"Scraping Energy Pedia for category: {category}")
    try:
        response = requests.get(url, headers=scraper_instance.headers, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # NOTE: This is based on the assumed structure of the website.
        # This part needs to be adjusted if the website's HTML is different.
        listings = soup.select('.card.directory-entry') # Assuming listings are in cards with this class

        for item in listings:
            company_name_element = item.select_one('h5.card-title a')
            website_element = item.select_one('a[href*="http"]') # A link that is likely the website
            
            company_name = company_name_element.text.strip() if company_name_element else None
            website = website_element['href'] if website_element else None
            
            if company_name and website:
                logging.info(f"Found company: {company_name}")
                
                # Validate URL before adding
                validation_result = scraper_instance.url_validator.validate_url(website)
                
                if validation_result['valid']:
                    # Add to directory listings (with less data than API)
                    scraper_instance.directory_listings.append({
                        'name': company_name,
                        'address': '', # Not easily available on the listing page
                        'phone': '',
                        'website': website,
                        'website_status': validation_result['status_code'],
                        'website_verified': True,
                        'rating': '',
                        'latitude': '',
                        'longitude': '',
                        'category': category,
                        'location': 'N/A',
                        'google_maps_url': '',
                        'source': 'Energy Pedia'
                    })
                    
                    # Scrape the company's website for contacts
                    time.sleep(1)
                    scraper_instance.scrape_website_for_contacts(website, company_name, category)
                else:
                    logging.warning(f"⚠️ Invalid URL for {company_name}: {website} - {validation_result['error']}")
                    scraper_instance.invalid_urls.append({
                        'company': company_name,
                        'url': website,
                        'error': validation_result['error'],
                        'source': 'Energy Pedia'
                    })

    except requests.exceptions.RequestException as e:
        logging.error(f"Could not scrape Energy Pedia URL {url}: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred while scraping Energy Pedia: {e}")


def main():
    """
    Execute dual-purpose scraping
    """
    try:
        scraper = DualPurposeScraper()
    except ValueError as e:
        logging.error(f"Configuration Error: {e}")
        logging.error("Please set the GOOGLE_MAPS_API_KEY environment variable if you intend to use the API.")
        # Don't exit, allow fallback to work
    
    config = load_config()
    if not config:
        return

    print("="*70)
    print("tstr.directory - DUAL-PURPOSE SCRAPER")
    print("="*70)
    
    # Check if Google Maps API is available and configured
    api_key = os.getenv("GOOGLE_MAPS_API_KEY")
    if check_api_availability(api_key):
        # --- API MODE ---
        logging.info("Starting scraping process using Google Maps API...")
        searches = config.get('google_api_searches', [])
        if not searches:
            logging.warning("API is available, but no 'google_api_searches' found in config.json.")
            return
            
        logging.info(f"Targets: {len(searches)} categories × locations from config.json")
        for idx, search in enumerate(searches, 1):
            category = search.get('category')
            location = search.get('location')
            if not category or not location:
                logging.warning(f"Skipping invalid search entry at index {idx-1}: {search}")
                continue
            
            logging.info(f"[{idx}/{len(searches)}] Scraping: {category} in {location}")
            scraper.scrape_google_maps_api(category, location)
            time.sleep(2)
    else:
        # --- FALLBACK MODE ---
        logging.info("Starting scraping process using alternative sources (direct web scraping)...")
        sources = config.get('alternative_sources', [])
        if not sources:
            logging.warning("API not available and no 'alternative_sources' found in config.json.")
            return

        logging.info(f"Targets: {len(sources)} alternative sources from config.json")
        for idx, source in enumerate(sources, 1):
            name = source.get('name')
            category = source.get('category')
            url = source.get('url')

            if not all([name, category, url]):
                logging.warning(f"Skipping invalid alternative source at index {idx-1}: {source}")
                continue
            
            logging.info(f"[{idx}/{len(sources)}] Scraping source: {name}")
            if name == "Energy Pedia":
                scrape_energy_pedia(url, category, scraper)
            # Add other scrapers here with 'elif name == "Other Source":'
            else:
                logging.warning(f"No scraper implemented for source: {name}")
            time.sleep(2)

    print("\n" + "="*70)
    logging.info("SCRAPING COMPLETE")
    print("="*70)
    
    # Generate CSV files
    logging.info("Generating CSV files...")
    scraper.generate_directory_csv('tstr_directory_import.csv')
    scraper.generate_sales_contacts_csv('tstr_sales_leads.csv')
    scraper.generate_invalid_urls_report('invalid_urls_report.csv')
    
    # Get URL validation statistics
    validation_stats = scraper.url_validator.get_stats()
    
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print(f"Directory Listings: {len(scraper.directory_listings)} (verified URLs only)")
    print(f"Sales Leads Found: {len(scraper.sales_contacts)}")
    print(f"\nURL Validation Statistics:")
    print(f"  • Total URLs Validated: {validation_stats['total_validated']}")
    print(f"  • Valid URLs: {validation_stats['valid']}")
    print(f"  • Invalid URLs: {validation_stats['invalid']}")
    print(f"  • Success Rate: {validation_stats['success_rate']}")
    print(f"  • Cached Results: {validation_stats['cached']}")
    print("\nFiles created:")
    print("  1. tstr_directory_import.csv (verified listings only)")
    print("  2. tstr_sales_leads.csv (use for email outreach)")
    if scraper.invalid_urls:
        print("  3. invalid_urls_report.csv (URLs that failed validation)")
    print("\nNext steps:")
    print("  1. Upload directory CSV to WordPress Directorist")
    print("  2. Review sales leads CSV")
    if scraper.invalid_urls:
        print("  3. Review invalid URLs report and manually verify if needed")
    print("  4. Start outreach to high-confidence leads")
    print("="*70)

if __name__ == "__main__":
    main()
