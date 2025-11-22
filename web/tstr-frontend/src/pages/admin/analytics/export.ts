import type { APIRoute } from 'astro';
import { supabase } from '../../../lib/supabase';

export const GET: APIRoute = async ({ request }) => {
  // TODO: Add authentication when auth system is implemented
  // For now, export is publicly accessible (internal use only)

  // Fetch all clicks with listing details
  const { data: clicks, error } = await supabase
    .from('clicks')
    .select(`
      id,
      url,
      user_agent,
      referrer,
      created_at,
      listings (
        business_name,
        website,
        category:category_id(name)
      )
    `)
    .order('created_at', { ascending: false });

  if (error || !clicks) {
    return new Response('Error fetching data', { status: 500 });
  }

  // Generate CSV
  const headers = ['ID', 'Timestamp', 'Listing', 'Category', 'URL', 'User Agent', 'Referrer'];
  const rows = clicks.map(click => [
    click.id,
    new Date(click.created_at).toISOString(),
    click.listings?.business_name || 'Unknown',
    click.listings?.category?.name || 'N/A',
    click.url,
    click.user_agent || '',
    click.referrer || ''
  ]);

  const csv = [
    headers.join(','),
    ...rows.map(row => row.map(cell =>
      // Escape commas and quotes in CSV
      `"${String(cell).replace(/"/g, '""')}"`
    ).join(','))
  ].join('\n');

  // Return CSV file
  return new Response(csv, {
    status: 200,
    headers: {
      'Content-Type': 'text/csv',
      'Content-Disposition': `attachment; filename="tstr-click-analytics-${new Date().toISOString().split('T')[0]}.csv"`
    }
  });
};
