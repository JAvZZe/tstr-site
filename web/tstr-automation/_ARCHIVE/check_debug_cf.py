from base_scraper import BaseNicheScraper

scraper = type('Dummy', (BaseNicheScraper,), {
    'extract_standard_fields': lambda s, soup, url: {}, 
    'extract_custom_fields': lambda s, soup, url: {}, 
    'get_listing_urls': lambda s, limit: []
})('materials-testing', 'A2LA')

print("Loaded custom fields config:")
for field_key, field_config in scraper.custom_fields.items():
    print(f"Key: {field_key} -> Type: {field_config.get('field_type')} -> Label: {field_config.get('field_label')}")
