from base_scraper import BaseNicheScraper
import os
import logging

class MockScraper(BaseNicheScraper):
    def extract_standard_fields(self, soup, url): return {}
    def extract_custom_fields(self, soup, url): return {}
    def get_listing_urls(self, limit): return []

scraper = MockScraper('materials-testing', 'A2LA')
logging.basicConfig(level=logging.INFO)

# Get a real location ID
locs = scraper.supabase.from_('locations').select('id').limit(1).execute().data
real_loc_id = locs[0]['id'] if locs else None

listing_data = {
    'business_name': 'DEBUG LAB INTERNAL KEYS ' + str(os.urandom(4).hex()),
    'address': '123 Test St',
    'city': 'Frederick',
    'state': 'MD',
    'zip_code': '21703',
    'phone': '301-644-3248',
    'website': 'https://www.a2la.org',
    'location_id': real_loc_id
}

# Use INTERNAL keys
custom_fields = {
    'material_types': ['Metals', 'Plastics'],
    'test_procedures': ['Tensile Testing', 'Fatigue Testing'],
    'custom_test_dev': True,
    'rd_capabilities': 'Advanced R&D for Aerospace materials'
}

source_url = 'https://search.a2la.org/pages/certificate.aspx?Id=DEBUG_KEYS_TEST_NEW'

print("Attempting to save NEW listing with INTERNAL keys...")
res = scraper.save_listing(listing_data, custom_fields, source_url)
print(f"Save result (listing_id): {res}")

if res:
    print("Verifying saved custom fields...")
    cf_data = scraper.supabase.from_('listing_custom_fields').select('*, custom_fields(field_label)').eq('listing_id', res).execute().data
    for row in cf_data:
        label = row.get('custom_fields', {}).get('field_label', 'Unknown')
        print(f"Field: {label} -> Value: {row['value']}")
