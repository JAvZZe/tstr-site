import type { APIRoute } from 'astro';

/**
 * DEPRECATED. Kept only so any cached page or bookmarked integration still works.
 *
 * This endpoint used to write to `leads_rfq` and email the laboratory directly.
 * That contradicted how TSTR operates: an enquiry must reach us first so we can
 * forward it, otherwise we are not seen to facilitate and the directory has no
 * demonstrable value to the lab.
 *
 * `leads_rfq` was renamed to `leads_rfq_deprecated_20260819` on 2026-08-19 and its
 * single test row was migrated into `rfq_requests`, so the old code path would fail
 * anyway. Rather than return an error, this proxies to /api/rfq, which persists the
 * enquiry and alerts us.
 *
 * Remove once no traffic has hit this route for a full deploy cycle.
 */
export const POST: APIRoute = async ({ request, clientAddress }) => {
  let body: Record<string, unknown> = {};
  try {
    body = await request.json();
  } catch {
    return new Response(JSON.stringify({ error: 'Invalid JSON body' }), {
      status: 400,
      headers: { 'Content-Type': 'application/json' },
    });
  }

  // Map the old field names onto the RFQ contract.
  const mapped = {
    listing_id: body.listingId ?? body.listing_id ?? null,
    buyer_name: body.name ?? body.buyer_name,
    buyer_email: body.email ?? body.buyer_email,
    buyer_company: body.company ?? body.buyer_company,
    buyer_role: body.role ?? body.buyer_role,
    sector: body.industry ?? body.sector,
    service_needed:
      body.service_needed ?? `${(body.industry as string) || 'Testing'} enquiry (legacy form)`,
    message: body.message,
  };

  const url = new URL('/api/rfq', request.url);
  const forwarded = await fetch(url.toString(), {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'user-agent': request.headers.get('user-agent') || 'legacy-leads-endpoint',
      'x-forwarded-for': clientAddress || '',
    },
    body: JSON.stringify(mapped),
  });

  return new Response(await forwarded.text(), {
    status: forwarded.status,
    headers: { 'Content-Type': 'application/json' },
  });
};

export const GET: APIRoute = () =>
  new Response(
    JSON.stringify({
      error: 'Deprecated. Use POST /api/rfq.',
    }),
    { status: 410, headers: { 'Content-Type': 'application/json' } }
  );
