import type { APIRoute } from 'astro';
import { supabase } from '../../../lib/supabase';

export const prerender = false;

export const GET: APIRoute = async ({ params }) => {
  const listingId = params.id;

  if (!listingId) {
    return new Response('Missing listing ID', { status: 400 });
  }

  const { data, error } = await supabase
    .from('listings')
    .select('business_name, trust_score, claimed, status')
    .eq('id', listingId)
    .single();

  if (error || !data || data.status !== 'active') {
    const notFoundSvg = `<svg xmlns="http://www.w3.org/2000/svg" width="180" height="60">
      <rect width="180" height="60" rx="8" fill="#9CA3AF"/>
      <text x="90" y="35" text-anchor="middle" fill="white" font-size="13" font-family="Arial, sans-serif">Listing Not Found</text>
    </svg>`;

    return new Response(notFoundSvg, {
      status: 404,
      headers: {
        'Content-Type': 'image/svg+xml',
        'Cache-Control': 'public, max-age=300',
      },
    });
  }

  const isVerified = data.claimed === true;
  const score = typeof data.trust_score === 'number' ? data.trust_score : 0;

  const bgColor = isVerified
    ? score >= 70 ? '#15803d' : '#16a34a'
    : '#4B5563';
  const accentColor = isVerified ? '#86efac' : '#D1D5DB';
  const label = isVerified ? 'TSTR Verified' : 'Listed on TSTR';
  const icon = isVerified ? '\u2713' : '\u25cf';

  const barMaxWidth = 120;
  const barWidth = Math.round((score / 100) * barMaxWidth);
  const barColor = score >= 70 ? '#4ade80' : score >= 40 ? '#facc15' : '#f87171';

  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="200" height="70" role="img" aria-label="${label}: ${score}/100">
  <title>${label}: Trust Score ${score}/100</title>
  <rect width="200" height="70" rx="10" fill="${bgColor}"/>
  <rect x="1" y="1" width="198" height="34" rx="9" fill="rgba(255,255,255,0.08)"/>
  <text x="14" y="24" fill="${accentColor}" font-size="13" font-family="Arial, sans-serif" font-weight="bold">${icon}</text>
  <text x="30" y="24" fill="white" font-size="13" font-family="Arial, sans-serif" font-weight="bold">${label}</text>
  <text x="14" y="40" fill="rgba(255,255,255,0.65)" font-size="9" font-family="Arial, sans-serif">tstr.directory</text>
  <text x="186" y="40" fill="rgba(255,255,255,0.65)" font-size="9" font-family="Arial, sans-serif" text-anchor="end">Score: ${score}/100</text>
  <rect x="14" y="47" width="${barMaxWidth}" height="6" rx="3" fill="rgba(255,255,255,0.2)"/>
  <rect x="14" y="47" width="${barWidth}" height="6" rx="3" fill="${barColor}"/>
</svg>`;

  return new Response(svg, {
    headers: {
      'Content-Type': 'image/svg+xml',
      'Cache-Control': 'public, max-age=86400',
      'X-Content-Type-Options': 'nosniff',
    },
  });
};
