/**
 * IndexNow Integration Utility
 * Used to programmatically notify Bing/Google of new content.
 */

export async function notifyIndexNow(urls: string[]) {
  if (!urls || urls.length === 0) return;

  try {
    // We ping our own internal service to handle the POST logic and key validation
    // This allows us to trigger indexing from both client-side and server-side contexts easily
    const response = await fetch('https://tstr.directory/api/seo/ping-indexnow', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ urls })
    });

    const result = await response.json();
    return result;
  } catch (error) {
    console.error('Failed to notify IndexNow:', error);
    return { error: error.message };
  }
}

/**
 * Generates the full PSEO URL matrix for a listing
 */
export function generatePSEOUrlsForListing(listing: any, categories: any[], capabilities: any[]) {
    const urls: string[] = [];
    const baseUrl = 'https://tstr.directory';
    
    // 1. Company detail page
    urls.push(`${baseUrl}/company/${listing.slug}`);

    // 2. 3D Matrix Pages (testing/[industry]/[standard]-in-[region])
    if (listing.region) {
        const regionSlug = listing.region.toLowerCase().replace(/\s+/g, '-');
        
        categories.forEach(cat => {
            capabilities.forEach(cap => {
                if (cat.slug && cap.standard?.slug) {
                    urls.push(`${baseUrl}/testing/${cat.slug}/${cap.standard.slug}-in-${regionSlug}`);
                }
            });
        });
    }

    return urls;
}
