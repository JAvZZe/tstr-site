import type { APIRoute } from 'astro';
import { createClient } from '@supabase/supabase-js';

export const prerender = false;

const RESEND_API_KEY = import.meta.env.RESEND_API_KEY;
const SUPABASE_URL = import.meta.env.SUPABASE_URL;
const SUPABASE_SERVICE_ROLE_KEY = import.meta.env.SUPABASE_SERVICE_ROLE_KEY;
const INTERNAL_API_SECRET = import.meta.env.INTERNAL_API_SECRET;

// Rate limit: max 50 emails per call
const MAX_BATCH_SIZE = 50;

export const POST: APIRoute = async ({ request }) => {
  // Validate internal API secret to prevent abuse
  const authHeader = request.headers.get('Authorization');
  if (!authHeader || authHeader !== `Bearer ${INTERNAL_API_SECRET}`) {
    return new Response(JSON.stringify({ error: 'Unauthorized' }), {
      status: 401,
      headers: { 'Content-Type': 'application/json' },
    });
  }

  if (!RESEND_API_KEY) {
    return new Response(JSON.stringify({ error: 'Resend API key not configured' }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' },
    });
  }

  let body: {
    listingId?: string;
    batch?: boolean;
    limit?: number;
    category?: string;
  };

  try {
    body = await request.json();
  } catch {
    return new Response(JSON.stringify({ error: 'Invalid JSON body' }), {
      status: 400,
      headers: { 'Content-Type': 'application/json' },
    });
  }

  const supabase = createClient(SUPABASE_URL!, SUPABASE_SERVICE_ROLE_KEY!);

  // --- Single listing outreach ---
  if (body.listingId && !body.batch) {
    const { data: listing, error } = await supabase
      .from('listings')
      .select('id, business_name, email, claimed, outreach_sent_at')
      .eq('id', body.listingId)
      .eq('status', 'active')
      .single();

    if (error || !listing) {
      return new Response(JSON.stringify({ error: 'Listing not found or inactive' }), {
        status: 404,
        headers: { 'Content-Type': 'application/json' },
      });
    }

    if (listing.claimed) {
      return new Response(JSON.stringify({ error: 'Listing already claimed' }), {
        status: 400,
        headers: { 'Content-Type': 'application/json' },
      });
    }

    if (!listing.email) {
      return new Response(JSON.stringify({ error: 'Listing has no email address' }), {
        status: 400,
        headers: { 'Content-Type': 'application/json' },
      });
    }

    const result = await sendOutreachEmail(listing.email, listing.business_name, listing.id);
    if (!result.success) {
      return new Response(JSON.stringify({ error: result.error }), {
        status: 500,
        headers: { 'Content-Type': 'application/json' },
      });
    }

    // Record that outreach was sent
    await supabase
      .from('listings')
      .update({ outreach_sent_at: new Date().toISOString() })
      .eq('id', listing.id);

    return new Response(JSON.stringify({ success: true, sent: 1 }), {
      status: 200,
      headers: { 'Content-Type': 'application/json' },
    });
  }

  // --- Batch outreach ---
  if (body.batch) {
    const limit = Math.min(body.limit || 10, MAX_BATCH_SIZE);

    let query = supabase
      .from('listings')
      .select('id, business_name, email, claimed, outreach_sent_at')
      .eq('status', 'active')
      .eq('claimed', false)
      .not('email', 'is', null)
      .is('outreach_sent_at', null)
      .limit(limit);

    if (body.category) {
      query = query.eq('category_slug', body.category);
    }

    const { data: listings, error } = await query;

    if (error) {
      return new Response(JSON.stringify({ error: error.message }), {
        status: 500,
        headers: { 'Content-Type': 'application/json' },
      });
    }

    if (!listings || listings.length === 0) {
      return new Response(JSON.stringify({ success: true, sent: 0, message: 'No eligible listings found' }), {
        status: 200,
        headers: { 'Content-Type': 'application/json' },
      });
    }

    const results = await Promise.allSettled(
      listings.map(async (listing) => {
        const result = await sendOutreachEmail(listing.email!, listing.business_name, listing.id);
        if (result.success) {
          await supabase
            .from('listings')
            .update({ outreach_sent_at: new Date().toISOString() })
            .eq('id', listing.id);
        }
        return { listingId: listing.id, ...result };
      })
    );

    const succeeded = results.filter(r => r.status === 'fulfilled' && (r.value as {success: boolean}).success).length;
    const failed = results.length - succeeded;

    return new Response(JSON.stringify({
      success: true,
      sent: succeeded,
      failed,
      total: listings.length,
    }), {
      status: 200,
      headers: { 'Content-Type': 'application/json' },
    });
  }

  return new Response(JSON.stringify({ error: 'Provide listingId or batch:true' }), {
    status: 400,
    headers: { 'Content-Type': 'application/json' },
  });
};

async function sendOutreachEmail(
  email: string,
  businessName: string,
  listingId: string
): Promise<{ success: boolean; error?: string }> {
  const claimUrl = `https://tstr.directory/claim?listingId=${listingId}`;

  const html = `
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
      <div style="text-align: center; margin-bottom: 30px;">
        <h1 style="color: #000080; margin: 0;">TSTR.directory</h1>
        <p style="color: #6B7280; margin: 5px 0;">Testing Services Directory</p>
      </div>

      <div style="background-color: #F9FAFB; padding: 30px; border-radius: 8px; margin-bottom: 30px;">
        <h2 style="color: #1F2937; margin-top: 0;">Your capabilities are getting noticed</h2>
        <p style="color: #4B5563; line-height: 1.6;">Hi ${businessName},</p>
        <p style="color: #4B5563; line-height: 1.6;">
          Your testing services are listed on <a href="https://tstr.directory" style="color: #000080;">TSTR.directory</a> &mdash; the global directory for hydrogen and industrial testing labs.
          Potential customers are searching for services like yours right now.
        </p>

        <div style="background-color: #EFF6FF; border-left: 4px solid #000080; padding: 20px; margin: 20px 0; border-radius: 4px;">
          <h3 style="color: #1E40AF; margin-top: 0;">Claim your listing to unlock:</h3>
          <ul style="color: #1E40AF; margin: 0; padding-left: 20px; line-height: 2;">
            <li>Verified badge &mdash; builds trust with decision-makers</li>
            <li>Lead notifications when buyers contact you</li>
            <li>Analytics on how many people view your profile</li>
            <li>Ability to edit and enhance your listing</li>
          </ul>
        </div>

        <div style="text-align: center; margin: 30px 0;">
          <a href="${claimUrl}"
             style="background-color: #000080; color: white; padding: 14px 28px; text-decoration: none; border-radius: 6px; font-weight: 600; display: inline-block;">
            Claim Your Free Listing
          </a>
        </div>

        <p style="color: #6B7280; font-size: 14px; text-align: center;">Takes less than 2 minutes. No credit card required.</p>
      </div>

      <div style="text-align: center; color: #9CA3AF; font-size: 12px;">
        <p>TSTR.directory &mdash; The global directory for testing services.</p>
        <p>You're receiving this because your business is listed on our directory. <a href="https://tstr.directory/unsubscribe?listingId=${listingId}" style="color: #9CA3AF;">Unsubscribe</a></p>
      </div>
    </div>
  `;

  try {
    const res = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${RESEND_API_KEY}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        from: 'noreply@tstr.directory',
        to: email,
        subject: `${businessName} \u2014 your TSTR.directory listing is getting views`,
        html,
        text: `Hi ${businessName},\n\nYour testing services are listed on TSTR.directory. Claim your listing to unlock lead notifications and a verified badge.\n\nClaim now: ${claimUrl}\n\nTSTR.directory \u2014 The global directory for testing services.`,
      }),
    });

    if (!res.ok) {
      const err = await res.text();
      console.error('Resend error:', err);
      return { success: false, error: `Resend API error: ${res.status}` };
    }

    return { success: true };
  } catch (e) {
    const msg = e instanceof Error ? e.message : String(e);
    return { success: false, error: msg };
  }
}
