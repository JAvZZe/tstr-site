import type { APIRoute } from 'astro';
import { createClient } from '@supabase/supabase-js';
import { sendEmail, type EmailTemplate } from '../../lib/email';
import { requiredString, optionalString } from '../../lib/validate';

/**
 * Gated RFQ intake.
 *
 * Business model: TSTR's value proposition is LEAD GEN. Buyer requests come to US
 * first, we forward to the lab. We must be seen to facilitate — never wire the
 * buyer straight to the lab, or the perceived value (and the reason a lab pays)
 * disappears. Captured demand is the sales proof.
 */

const INTERNAL_RFQ_INBOX = 'sales@tstr.directory';

function escapeHtml(s: string): string {
  return s
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

function createRfqAlertEmail(d: {
  buyerName: string;
  buyerEmail: string;
  buyerCompany: string;
  buyerPhone: string;
  country: string;
  serviceNeeded: string;
  standard: string;
  quantity: string;
  deadline: string;
  message: string;
  labName: string;
  listingSlug: string;
}): EmailTemplate {
  const row = (label: string, value: string) =>
    value ? `<p><strong>${label}:</strong> ${escapeHtml(value)}</p>` : '';

  return {
    subject: `[TSTR RFQ] ${d.serviceNeeded} — ${d.buyerCompany || d.buyerName}${
      d.labName ? ` (for ${d.labName})` : ''
    }`,
    html: `
    <div style="font-family: sans-serif; max-width: 640px; margin: 0 auto; padding: 20px; border: 1px solid #eee; border-radius: 8px;">
      <h2 style="color: #000080; border-bottom: 2px solid #32CD32; padding-bottom: 10px;">
        New RFQ — action required
      </h2>
      <p style="color:#555;">A buyer submitted a request. Review, then forward to the lab.</p>

      <h3 style="margin-bottom:4px;">Buyer</h3>
      <div style="margin: 0 0 16px;">
        ${row('Name', d.buyerName)}
        ${row('Email', d.buyerEmail)}
        ${row('Company', d.buyerCompany)}
        ${row('Phone', d.buyerPhone)}
        ${row('Country', d.country)}
      </div>

      <h3 style="margin-bottom:4px;">Requirement</h3>
      <div style="background:#f9fafb; padding:15px; border-radius:4px; color:#333;">
        ${row('Service needed', d.serviceNeeded)}
        ${row('Standard', d.standard)}
        ${row('Quantity', d.quantity)}
        ${row('Deadline', d.deadline)}
        ${
          d.message
            ? `<p><strong>Details:</strong></p><p style="white-space:pre-wrap;">${escapeHtml(
                d.message
              )}</p>`
            : ''
        }
      </div>

      ${
        d.labName
          ? `<h3 style="margin-bottom:4px;">Requested lab</h3>
             <p>${escapeHtml(d.labName)}${
               d.listingSlug
                 ? ` — <a href="https://tstr.directory/listing/${encodeURIComponent(
                     d.listingSlug
                   )}">view listing</a>`
                 : ''
             }</p>`
          : '<p style="color:#777;"><em>General enquiry — not tied to a single listing.</em></p>'
      }
    </div>`,
    text:
      `New RFQ\n\nBuyer: ${d.buyerName} <${d.buyerEmail}>\n` +
      `Company: ${d.buyerCompany}\nPhone: ${d.buyerPhone}\nCountry: ${d.country}\n\n` +
      `Service: ${d.serviceNeeded}\nStandard: ${d.standard}\nQuantity: ${d.quantity}\n` +
      `Deadline: ${d.deadline}\n\nDetails:\n${d.message}\n\n` +
      `Lab: ${d.labName || '(general)'}\n`,
  };
}

export const POST: APIRoute = async ({ request, clientAddress }) => {
  try {
    const ct = request.headers.get('content-type') || '';
    const body: Record<string, string> = {};
    if (ct.includes('application/json')) {
      Object.assign(body, await request.json());
    } else {
      const fd = await request.formData();
      fd.forEach((v, k) => {
        body[k] = typeof v === 'string' ? v : '';
      });
    }

    // honeypot — bots fill hidden fields
    if (optionalString(body.website_hp, { max: 200 })) {
      return new Response(JSON.stringify({ success: true }), { status: 200 });
    }

    const nameV = requiredString(body.buyer_name, 'buyer_name', { max: 120 });
    const emailV = requiredString(body.buyer_email, 'buyer_email', {
      max: 200,
      email: true,
    });
    const serviceV = requiredString(body.service_needed, 'service_needed', { max: 300 });

    for (const v of [nameV, emailV, serviceV]) {
      if (!v.ok) {
        return new Response(JSON.stringify({ success: false, error: v.error }), {
          status: 400,
          headers: { 'Content-Type': 'application/json' },
        });
      }
    }

    const buyerName = nameV.ok ? nameV.data : '';
    const buyerEmail = emailV.ok ? emailV.data : '';
    const serviceNeeded = serviceV.ok ? serviceV.data : '';

    const buyerCompany = optionalString(body.buyer_company, { max: 160 });
    const buyerPhone = optionalString(body.buyer_phone, { max: 60 });
    const country = optionalString(body.country, { max: 80 });
    const standard = optionalString(body.standard, { max: 120 });
    const quantity = optionalString(body.quantity, { max: 80 });
    const deadline = optionalString(body.deadline, { max: 40 });
    const message = optionalString(body.message, { max: 4000 });
    const listingId = optionalString(body.listing_id, { max: 64 }) || null;
    const labName = optionalString(body.lab_name, { max: 200 });
    const listingSlug = optionalString(body.listing_slug, { max: 200 });

    // Persist first — never lose a lead because email failed.
    const supabaseUrl = import.meta.env.PUBLIC_SUPABASE_URL;
    const serviceKey =
      import.meta.env.SUPABASE_SERVICE_ROLE_KEY || import.meta.env.PUBLIC_SUPABASE_ANON_KEY;

    let stored = false;
    if (supabaseUrl && serviceKey) {
      const supabase = createClient(supabaseUrl, serviceKey);
      const ipHash = clientAddress
        ? Array.from(clientAddress)
            .reduce((h, c) => (h * 31 + c.charCodeAt(0)) | 0, 7)
            .toString(36)
        : null;
      const { error } = await supabase.from('rfq_requests').insert({
        listing_id: listingId,
        buyer_name: buyerName,
        buyer_email: buyerEmail,
        buyer_company: buyerCompany || null,
        buyer_phone: buyerPhone || null,
        country: country || null,
        service_needed: serviceNeeded,
        standard: standard || null,
        quantity: quantity || null,
        deadline: deadline || null,
        message: message || null,
        source: 'web',
        ip_hash: ipHash,
        user_agent: (request.headers.get('user-agent') || '').slice(0, 300),
      });
      stored = !error;
      if (error) console.error('RFQ insert failed:', error.message);
    }

    // Alert us so we can forward (gated model).
    try {
      await sendEmail(
        INTERNAL_RFQ_INBOX,
        createRfqAlertEmail({
          buyerName,
          buyerEmail,
          buyerCompany,
          buyerPhone,
          country,
          serviceNeeded,
          standard,
          quantity,
          deadline,
          message,
          labName,
          listingSlug,
        })
      );
    } catch (e) {
      console.error('RFQ alert email failed:', e);
    }

    return new Response(
      JSON.stringify({
        success: true,
        stored,
        message: "Thanks — we've received your request and will match you with the right lab.",
      }),
      { status: 200, headers: { 'Content-Type': 'application/json' } }
    );
  } catch (err) {
    const msg = err instanceof Error ? err.message : 'Unexpected error';
    return new Response(JSON.stringify({ success: false, error: msg }), {
      status: 400,
      headers: { 'Content-Type': 'application/json' },
    });
  }
};
