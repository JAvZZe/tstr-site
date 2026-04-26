from base_scraper import BaseNicheScraper
scraper = type('Dummy', (BaseNicheScraper,), {
    'extract_standard_fields': lambda s, soup, url: {}, 
    'extract_custom_fields': lambda s, soup, url: {}, 
    'get_listing_urls': lambda s, limit: []
})('materials-testing', 'A2LA')
res = scraper.supabase.from_('listings').select('business_name, website, source_script').limit(2000).execute()
a2la_count = 0
scripts = set()
for r in res.data:
    scripts.add(r.get('source_script'))
    if r.get('source_script') == 'A2LA':
        a2la_count += 1
        if a2la_count <= 5:
            print(f"A2LA Listing: {r['business_name']} | Website: {r['website']}")
print(f"Total A2LA Listings found: {a2la_count}")
print(f"Active Source Scripts: {scripts}")
