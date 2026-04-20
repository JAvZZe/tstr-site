# ruff: noqa: E402
"""
Cleanup Script: Validate Existing URLs in Database
Checks all existing listings and identifies/handles invalid URLs
"""

import os
from dotenv import load_dotenv
# Load environment variables from .env file in the same directory as this script
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))



# Load environment variables from .env file in the same directory as this script


import csv
import logging
from datetime import datetime


from url_validator import URLValidator

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables

class URLCleanup:
    """Validates existing URLs in database and handles invalid ones"""
    
    def __init__(self):
        self.url_validator = URLValidator(timeout=5, max_redirects=5)
        self.supabase_client = None
        self.valid_listings = []
        self.invalid_listings = []
        self._initialize_supabase()
    
    def _initialize_supabase(self):
        """Initialize Supabase client"""
        try:
            from supabase import create_client
            supabase_url = os.getenv("SUPABASE_URL")
            supabase_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
            
            if not supabase_url or not supabase_key:
                raise ValueError("Supabase credentials not found in environment variables")
            
            self.supabase_client = create_client(supabase_url, supabase_key)
            logging.info("✅ Connected to Supabase")
        except ImportError:
            logging.error("❌ Supabase library not installed. Run: pip install supabase")
            raise
        except Exception as e:
            logging.error(f"❌ Could not connect to Supabase: {e}")
            raise
    
    def fetch_all_listings(self):
        """Fetch all listings from database"""
        try:
            response = self.supabase_client.table("listings").select("*").execute()
            logging.info(f"📋 Fetched {len(response.data)} listings from database")
            return response.data
        except Exception as e:
            logging.error(f"❌ Error fetching listings: {e}")
            return []
    
    def validate_listings(self, listings):
        """Validate URLs for all listings"""
        print("\n" + "="*70)
        print("VALIDATING EXISTING URLS")
        print("="*70)
        
        total = len(listings)
        for idx, listing in enumerate(listings, 1):
            business_name = listing.get('business_name', 'Unknown')
            website = listing.get('website', '')
            
            if not website:
                logging.info(f"[{idx}/{total}] {business_name} - No website URL")
                self.valid_listings.append({
                    **listing,
                    'validation_status': 'no_url',
                    'validation_error': None
                })
                continue
            
            logging.info(f"[{idx}/{total}] Validating: {business_name}")
            logging.info(f"            URL: {website}")
            
            # Validate URL
            result = self.url_validator.validate_url(website)
            
            if result['valid']:
                logging.info(f"            ✓ Valid ({result['status_code']})")
                self.valid_listings.append({
                    **listing,
                    'validation_status': 'valid',
                    'validation_error': None,
                    'status_code': result['status_code']
                })
            else:
                logging.warning(f"            ✗ Invalid - {result['error']}")
                self.invalid_listings.append({
                    **listing,
                    'validation_status': 'invalid',
                    'validation_error': result['error'],
                    'status_code': result.get('status_code')
                })
        
        print("\n" + "="*70)
        logging.info("VALIDATION COMPLETE")
        print("="*70)
    
    def generate_report(self):
        """Generate CSV report of validation results"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Valid listings report
        if self.valid_listings:
            valid_file = f"valid_listings_{timestamp}.csv"
            with open(valid_file, 'w', newline='', encoding='utf-8') as f:
                fieldnames = ['id', 'business_name', 'website', 'status_code', 'validation_status']
                writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
                writer.writeheader()
                for listing in self.valid_listings:
                    writer.writerow(listing)
            logging.info(f"✅ Valid listings report: {valid_file}")
        
        # Invalid listings report
        if self.invalid_listings:
            invalid_file = f"invalid_listings_{timestamp}.csv"
            with open(invalid_file, 'w', newline='', encoding='utf-8') as f:
                fieldnames = ['id', 'business_name', 'website', 'validation_error', 'validation_status']
                writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
                writer.writeheader()
                for listing in self.invalid_listings:
                    writer.writerow(listing)
            logging.info(f"⚠️ Invalid listings report: {invalid_file}")
        
        return timestamp
    
    def mark_invalid_urls(self):
        """Mark invalid URLs in database (adds flag, keeps data)"""
        if not self.invalid_listings:
            logging.info("No invalid URLs to mark")
            return 0
        
        count = 0
        for listing in self.invalid_listings:
            try:
                self.supabase_client.table("listings").update({
                    'url_valid': False,
                    'url_validation_error': listing['validation_error']
                }).eq('id', listing['id']).execute()
                count += 1
            except Exception as e:
                logging.error(f"Error marking listing {listing['id']}: {e}")
        
        logging.info(f"✅ Marked {count} listings as having invalid URLs")
        return count
    
    def _ensure_pending_research_table(self):
        """Ensure pending_research table exists"""
        try:
            # Try to query the table to see if it exists
            self.supabase_client.table("pending_research").select("id").limit(1).execute()
            logging.info("✓ pending_research table exists")
        except Exception as e:
            logging.warning(f"⚠️  pending_research table may not exist: {e}")
            logging.info("📝 Please create the table using: create_pending_research_table.sql")
            logging.info("   Visit: https://app.supabase.com/project/haimjeaetrsaauitrhfy/sql")
            raise ValueError("pending_research table does not exist. Please create it first.")
    
    def move_to_pending_research(self):
        """Move listings with invalid URLs to 'pending_research' table"""
        if not self.invalid_listings:
            logging.info("No invalid URLs to move")
            return 0
        
        # Ensure table exists
        self._ensure_pending_research_table()
        
        count = 0
        moved_ids = []
        
        for listing in self.invalid_listings:
            try:
                # Add to pending_research table
                research_data = {
                    'business_name': listing['business_name'],
                    'website': listing['website'],
                    'validation_error': listing['validation_error'],
                    'original_id': listing['id'],
                    'category': listing.get('category'),
                    'location_id': listing.get('location_id'),
                    'address': listing.get('address'),
                    'phone': listing.get('phone'),
                    'email': listing.get('email'),
                    'description': listing.get('description'),
                    'status': 'pending_research',
                    'notes': 'Moved from listings due to invalid URL - needs research'
                }
                
                self.supabase_client.table("pending_research").insert(research_data).execute()
                moved_ids.append(listing['id'])
                logging.info(f"📋 Moved to research: {listing['business_name']}")
                count += 1
            except Exception as e:
                logging.error(f"Error moving listing {listing['id']}: {e}")
                continue
        
        # Now delete from main listings table
        if moved_ids:
            try:
                for listing_id in moved_ids:
                    self.supabase_client.table("listings").delete().eq('id', listing_id).execute()
                logging.info(f"✅ Successfully moved {count} listings to pending_research table")
            except Exception as e:
                logging.error(f"Error removing from listings: {e}")
        
        return count
    
    def print_summary(self):
        """Print summary of validation results"""
        stats = self.url_validator.get_stats()
        
        print("\n" + "="*70)
        print("VALIDATION SUMMARY")
        print("="*70)
        print(f"Total Listings Checked: {len(self.valid_listings) + len(self.invalid_listings)}")
        print(f"✅ Valid URLs: {len(self.valid_listings)}")
        print(f"❌ Invalid URLs: {len(self.invalid_listings)}")
        print(f"Success Rate: {stats['success_rate']}")
        
        if self.invalid_listings:
            print(f"\n❌ INVALID LISTINGS ({len(self.invalid_listings)}):")
            for listing in self.invalid_listings[:10]:  # Show first 10
                print(f"  • {listing['business_name']}")
                print(f"    URL: {listing['website']}")
                print(f"    Error: {listing['validation_error']}")
            
            if len(self.invalid_listings) > 10:
                print(f"  ... and {len(self.invalid_listings) - 10} more")
        
        print("="*70)


def main():
    """Main execution"""
    print("="*70)
    print("URL CLEANUP SCRIPT")
    print("Validates existing URLs in database")
    print("="*70)
    
    # Initialize cleanup
    cleanup = URLCleanup()
    
    # Fetch all listings
    listings = cleanup.fetch_all_listings()
    
    if not listings:
        logging.error("No listings found in database")
        return
    
    # Validate all URLs
    cleanup.validate_listings(listings)
    
    # Print summary
    cleanup.print_summary()
    
    # Generate reports
    timestamp = cleanup.generate_report()
    
    # Ask user what to do
    print("\n" + "="*70)
    print("CLEANUP OPTIONS")
    print("="*70)
    print("1. Mark invalid URLs (adds 'url_valid=False' flag, keeps in listings)")
    print("2. Move to research (moves to 'pending_research' table for later)")
    print("3. Report only (no changes to database)")
    print("="*70)
    
    if not cleanup.invalid_listings:
        print("\n✅ All URLs are valid! No cleanup needed.")
        return
    
    # Check for command line argument
    import sys
    if len(sys.argv) > 1:
        choice = sys.argv[1]
        print(f"\nAuto-selected option: {choice}")
    else:
        choice = input("\nEnter your choice (1/2/3): ").strip()
    
    if choice == "1":
        print("\n🔄 Marking invalid URLs in database...")
        count = cleanup.mark_invalid_urls()
        print(f"✅ Done! Marked {count} listings as invalid.")
        print("   Listings are still in database but flagged.")
    elif choice == "2":
        print(f"\n📋 Moving {len(cleanup.invalid_listings)} listings to pending_research table...")
        count = cleanup.move_to_pending_research()
        print(f"✅ Done! Moved {count} listings to pending research.")
        print("   You can review and fix URLs later, then move back to listings.")
    elif choice == "3":
        print("\n✅ Report generated. No changes made to database.")
    else:
        print("❌ Invalid choice. No changes made.")
    
    print("\n" + "="*70)
    print("FILES CREATED:")
    print(f"  • valid_listings_{timestamp}.csv")
    if cleanup.invalid_listings:
        print(f"  • invalid_listings_{timestamp}.csv")
    print("="*70)


if __name__ == "__main__":
    main()
