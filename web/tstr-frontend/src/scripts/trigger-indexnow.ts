import { createClient } from '@supabase/supabase-js';
import dotenv from 'dotenv';
import { generatePSEOUrlsForListing } from '../lib/indexnow.ts';

dotenv.config();

const supabaseUrl = process.env.PUBLIC_SUPABASE_URL || '';
const supabaseKey = process.env.SUPABASE_SERVICE_ROLE_KEY || '';
const supabase = createClient(supabaseUrl, supabaseKey);

async function run() {
  console.log('🚀 Triggering IndexNow for PSEO pages...');

  // 1. Fetch all active listings
  const { data: listings, error: lError } = await supabase
    .from('listings')
    .select(`
      id, 
      slug, 
      region,
      listing_categories(category:category_id(slug)),
      listing_capabilities(standard:standard_id(slug))
    `)
    .eq('status', 'active');

  if (lError) {
    console.error('Error fetching listings:', lError);
    return;
  }

  console.log(`🔍 Found ${listings.length} active listings.`);

  let allUrls: string[] = [];

  // 2. Generate URLs for each listing
  listings.forEach((listing: any) => {
    const categories = listing.listing_categories?.map((c: any) => c.category) || [];
    const capabilities = listing.listing_capabilities || [];
    
    const urls = generatePSEOUrlsForListing(listing, categories, capabilities);
    allUrls.push(...urls);
  });

  // Remove duplicates
  allUrls = [...new Set(allUrls)];
  console.log(`🔗 Generated ${allUrls.length} unique PSEO URLs.`);

  // 3. Batch and notify IndexNow (Max 10,000 URLs per request)
  const batchSize = 1000;
  // Use local server for dev, or the production site
  const baseUrl = process.env.NODE_ENV === 'production' 
    ? 'https://tstr.directory' 
    : (process.env.APP_URL || 'http://localhost:4321');

  console.log(`🌍 Using Base URL for ping: ${baseUrl}`);

  for (let i = 0; i < allUrls.length; i += batchSize) {
    const batch = allUrls.slice(i, i + batchSize);
    console.log(`📡 Pinging IndexNow for batch ${Math.floor(i / batchSize) + 1} (${batch.length} URLs)...`);

    try {
      const pingUrl = `${baseUrl}/api/seo/ping-indexnow`;
      const response = await fetch(pingUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ urls: batch })
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Failed to ping ${pingUrl}: ${response.status} ${response.statusText} - ${errorText}`);
      }

      const result = await response.json();
      console.log('✅ Result:', result);
    } catch (err) {
      console.error('❌ Failed to ping batch:', err.message);
    }
  }

  console.log('🏁 IndexNow synchronization complete.');
}

run().catch(console.error);
