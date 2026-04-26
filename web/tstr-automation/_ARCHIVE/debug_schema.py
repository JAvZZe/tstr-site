from base_scraper import BaseNicheScraper
scraper = type('Dummy', (BaseNicheScraper,), {
    'extract_standard_fields': lambda s, soup, url: {}, 
    'extract_custom_fields': lambda s, soup, url: {}, 
    'get_listing_urls': lambda s, limit: []
})('materials-testing', 'A2LA')
res = scraper.supabase.from_('listings').select('*').limit(1).execute()
if res.data:
    print(f"Columns: {list(res.data[0].keys())}")
else:
    print("No data found to check columns.")
