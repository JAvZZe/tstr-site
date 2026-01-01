import type { APIRoute } from 'astro';
import { supabase } from '../lib/supabase';

export const prerender = true;

export const GET: APIRoute = async () => {
  const baseUrl = 'https://tstr.directory';
  const currentDate = new Date().toISOString().split('T')[0];

  // Static pages
  const staticPages = [
    { url: '', priority: '1.0', changefreq: 'daily' },
    { url: '/browse', priority: '0.9', changefreq: 'daily' },
    { url: '/search/standards', priority: '0.9', changefreq: 'weekly' },
    { url: '/hydrogen-testing', priority: '0.9', changefreq: 'weekly' },
    { url: '/standards', priority: '0.9', changefreq: 'weekly' },
    { url: '/submit', priority: '0.8', changefreq: 'monthly' },
    { url: '/pricing', priority: '0.7', changefreq: 'monthly' },
    { url: '/privacy', priority: '0.5', changefreq: 'yearly' },
  ];

  // Standard-specific pages (high priority for SEO)
  const standardPages = [
    { url: '/standards/iso-19880-3', priority: '0.9', changefreq: 'weekly' },
    { url: '/standards/iso-19880-5', priority: '0.9', changefreq: 'weekly' },
    { url: '/standards/iso-11114-4', priority: '0.9', changefreq: 'weekly' },
  ];

  // Fetch all active standards for dynamic standard pages
  const { data: standards } = await supabase
    .from('standards')
    .select('code')
    .eq('is_active', true);

  const standardSearchPages = (standards || []).map(std => ({
    url: `/search/standards?standard=${encodeURIComponent(std.code)}`,
    priority: '0.8',
    changefreq: 'weekly'
  }));

  // Fetch categories with active listing counts (exclude empty categories)
  const { data: categoryData } = await supabase
    .from('categories')
    .select(`
      slug,
      listings:listings!category_id(count)
    `);

  // Filter out categories with 0 listings
  const categories = (categoryData || [])
    .filter(cat => cat.listings && cat.listings[0]?.count > 0)
    .map(cat => ({ slug: cat.slug }));

  // Category overview pages (/category)
  const categoryPages = categories.map(cat => ({
    url: `/${cat.slug}`,
    priority: '0.9',
    changefreq: 'weekly'
  }));

  // Legacy category query param pages
  const categoryBrowsePages = categories.map(cat => ({
    url: `/browse?category=${encodeURIComponent(cat.slug)}`,
    priority: '0.7',
    changefreq: 'daily'
  }));

  // Fetch all active listings to build category+region pages
  const { data: listings } = await supabase
    .from('listings')
    .select(`
      region,
      category:category_id (slug)
    `)
    .eq('status', 'active');

  // Build unique category/region combinations
  const categoryRegionPairs = new Set<string>();
  listings?.forEach(listing => {
    if (listing.category?.slug && listing.region) {
      categoryRegionPairs.add(`${listing.category.slug}/${listing.region.toLowerCase()}`);
    }
  });

  const categoryRegionPages = Array.from(categoryRegionPairs).map(pair => ({
    url: `/${pair}`,
    priority: '0.8',
    changefreq: 'weekly'
  }));

  // Environmental testing subcategory pages
  const environmentalSubcategories = [
    'air-quality',
    'water-quality',
    'soil-testing',
    'noise-vibration',
    'esg-sustainability'
  ];

  const subcategoryPages = environmentalSubcategories.map(subcat => ({
    url: `/environmental-testing/${subcat}`,
    priority: '0.8',
    changefreq: 'weekly'
  }));

  // Combine all pages
  const allPages = [
    ...staticPages,
    ...standardPages,
    ...categoryPages,
    ...categoryRegionPages,
    ...subcategoryPages,
    ...standardSearchPages.slice(0, 50), // Limit to top 50
    ...categoryBrowsePages
  ];

  // Generate XML
  const sitemap = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${allPages.map(page => `  <url>
    <loc>${baseUrl}${page.url}</loc>
    <lastmod>${currentDate}</lastmod>
    <changefreq>${page.changefreq}</changefreq>
    <priority>${page.priority}</priority>
  </url>`).join('\n')}
</urlset>`;

  return new Response(sitemap, {
    headers: {
      'Content-Type': 'application/xml',
      'Cache-Control': 'public, max-age=3600'
    }
  });
};
