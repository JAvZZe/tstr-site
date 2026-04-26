from base_scraper import BaseNicheScraper
import pprint
class MockScraper(BaseNicheScraper):
    def extract_standard_fields(self, soup, url): return {}
    def extract_custom_fields(self, soup, url): return {}
    def get_listing_urls(self, limit): return []

scraper = MockScraper('materials-testing', 'A2LA')
print("Custom Fields for Category:")
pprint.pprint(scraper.custom_fields)
