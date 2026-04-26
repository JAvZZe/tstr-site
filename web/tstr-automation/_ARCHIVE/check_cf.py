from base_scraper import BaseNicheScraper
import pprint

scraper = type('Dummy', (BaseNicheScraper,), {
    'extract_standard_fields': lambda s, soup, url: {}, 
    'extract_custom_fields': lambda s, soup, url: {}, 
    'get_listing_urls': lambda s, limit: []
})('materials-testing', 'A2LA')

data = scraper.supabase.from_('listings').select('id, business_name').eq('category_id', scraper.category_id).execute().data
for listing in data:
    cf_data = scraper.supabase.from_('listing_custom_fields').select('*').eq('listing_id', listing['id']).execute().data
    if cf_data:
        print(f"Found custom fields for {listing['business_name']}:")
        pprint.pprint(cf_data)
