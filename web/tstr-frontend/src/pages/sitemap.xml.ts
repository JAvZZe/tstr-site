import type { APIRoute } from 'astro';
import { supabase } from '../lib/supabase';

export const GET: APIRoute = async () => {
  const baseUrl = 'https://tstr.site';
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

  // Fetch all categories
  const { data: categories } = await supabase
    .from('categories')
    .select('slug');

  const categoryPages = (categories || []).map(cat => ({
    url: `/browse?category=${encodeURIComponent(cat.slug)}`,
    priority: '0.8',
    changefreq: 'daily'
  }));

  // Combine all pages
  const allPages = [
    ...staticPages,
    ...standardPages,
    ...standardSearchPages.slice(0, 50), // Limit to top 50
    ...categoryPages
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
