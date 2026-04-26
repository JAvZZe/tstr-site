from base_scraper import BaseNicheScraper
import pprint

scraper = type('Dummy', (BaseNicheScraper,), {
    'extract_standard_fields': lambda s, soup, url: {}, 
    'extract_custom_fields': lambda s, soup, url: {}, 
    'get_listing_urls': lambda s, limit: []
})('materials-testing', 'A2LA')

data = scraper.supabase.from_('listings').select('id, business_name').eq('category_id', scraper.category_id).execute().data
ids = [d['id'] for d in data]

# Batch query custom fields
all_cf = []
for i in range(0, len(ids), 100):
    batch_ids = ids[i:i+100]
    res = scraper.supabase.from_('listing_custom_fields').select('*').in_('listing_id', batch_ids).execute().data
    all_cf.extend(res)

if all_cf:
    print(f"Found {len(all_cf)} custom field entries across {len(set(d['listing_id'] for d in all_cf))} listings.")
    pprint.pprint(all_cf[:20])
else:
    print("No custom fields found for any listing in this category.")
