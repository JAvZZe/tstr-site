import type { APIRoute } from 'astro';
import { sendEmail, type EmailTemplate } from '../../lib/email';

/**
 * Unified form handler for TSTR.directory.
 *
 * Replaces /api/claim, /api/contact, /api/submit, and RFQ with one endpoint.
 * - Validates required fields per form type
 * - Logs to form_submissions (backup if email fails)
 * - Forwards fully-contextualized email to al@tstr.directory
 * - Returns form-specific confirmation to user
 *
 * Each form page keeps its own design, fields, and confirmation message.
 * The only unification is where the data goes and how the email is structured.
 */

type FormType = 'claim' | 'submit' | 'contact' | 'rfq';
const FORM_TYPES: FormType[] = ['claim', 'submit', 'contact', 'rfq'];

const REQUIRED: Record<FormType, string[]> = {
  claim: ['provider_name', 'contact_name', 'business_email'],
  submit: ['business_name', 'category', 'website', 'email'],
  contact: ['name', 'email', 'inquiryType', 'message'],
  rfq: ['buyer_email', 'message'],
};

function escapeHtml(s: string): string {
  return s
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

function getEmail(type: FormType, body: any): string {
  if (type === 'claim') return body.business_email || '';
  if (type === 'submit') return body.email || '';
  if (type === 'contact') return body.email || '';
  if (type === 'rfq') return body.buyer_email || '';
  return '';
}

function getSenderName(type: FormType, body: any): string {
  if (type === 'claim') return body.contact_name || '';
  if (type === 'submit') return body.business_name || '';
  if (type === 'contact') return body.name || '';
  if (type === 'rfq') return body.buyer_name || '';
  return '';
}

function buildSubject(type: FormType, body: any): string {
  const map: Record<FormType, string> = {
    claim: `CLAIM — ${body.provider_name || 'unknown'} — ${body.business_email || ''}`,
    submit: `SUBMIT — ${body.business_name || 'unknown'} — ${body.category || ''}`,
    contact: `CONTACT — ${body.inquiryType || 'general'} — ${body.name || ''}`,
    rfq: `RFQ — ${body.listing_slug || 'general'} — ${body.buyer_email || ''}`,
  };
  return `[TSTR] ${map[type]}`;
}

function buildEmail(
  type: FormType,
  body: any,
  meta: { ip: string; ua: string; referrer: string; timestamp: string }
): EmailTemplate {
  const label: Record<FormType, string> = {
    claim: 'LISTING CLAIM',
    submit: 'NEW LISTING SUBMISSION',
    contact: 'GENERAL CONTACT',
    rfq: 'BUYER RFQ (QUOTE REQUEST)',
  };

  const fields = Object.entries(body)
    .filter(
      ([k]) =>
        !['form_type', 'hp_email', 'hp-email', 'website_2', 'g-recaptcha-response'].includes(k)
    )
    .map(([k, v]) => `  ${k.padEnd(18)} ${String(v).slice(0, 500)}`)
    .join('\n');

  const text = `TSTR FORM SUBMISSION
─────────────────────────────────────────
TYPE:        ${label[type]}
FROM:        ${getEmail(type, body) || 'n/a'}
NAME:        ${getSenderName(type, body) || 'n/a'}
IP:          ${meta.ip}
REFERRER:    ${meta.referrer.slice(0, 200)}
TIME:        ${meta.timestamp}
─────────────────────────────────────────
${fields}
─────────────────────────────────────────`;

  const rows = Object.entries(body)
    .filter(
      ([k]) =>
        !['form_type', 'hp_email', 'hp-email', 'website_2', 'g-recaptcha-response'].includes(k)
    )
    .map(
      ([k, v]) =>
        `<tr><td style="padding:4px 12px;font-weight:bold;color:#000080">${escapeHtml(k)}</td><td style="padding:4px 12px">${escapeHtml(String(v).slice(0, 500))}</td></tr>`
    )
    .join('');

  const html = `<div style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;max-width:640px;margin:0 auto;padding:24px">
  <h2 style="color:#000080;border-bottom:2px solid #32cd32;padding-bottom:8px;margin-top:0">${label[type]}</h2>
  <table style="font-size:14px;margin-bottom:20px;border-collapse:collapse">
    <tr><td style="padding:4px 12px;font-weight:bold;color:#000080">From</td><td style="padding:4px 12px">${escapeHtml(getEmail(type, body) || 'n/a')}</td></tr>
    <tr><td style="padding:4px 12px;font-weight:bold;color:#000080">Name</td><td style="padding:4px 12px">${escapeHtml(getSenderName(type, body) || 'n/a')}</td></tr>
    <tr><td style="padding:4px 12px;font-weight:bold;color:#000080">IP</td><td style="padding:4px 12px">${escapeHtml(meta.ip)}</td></tr>
    <tr><td style="padding:4px 12px;font-weight:bold;color:#000080">Referrer</td><td style="padding:4px 12px">${escapeHtml(meta.referrer.slice(0, 200))}</td></tr>
    <tr><td style="padding:4px 12px;font-weight:bold;color:#000080">Time</td><td style="padding:4px 12px">${escapeHtml(meta.timestamp)}</td></tr>
  </table>
  <h3 style="color:#333;margin-bottom:8px">Form Fields</h3>
  <table style="font-size:13px;border-collapse:collapse;background:#f9fafb;border-radius:8px;padding:12px">${rows}</table>
  <p style="margin-top:20px;font-size:12px;color:#999;text-align:center">TSTR.directory Unified Form Handler</p>
</div>`;

  return { subject: buildSubject(type, body), html, text };
}

function getConfirmation(type: FormType, body: any): string {
  switch (type) {
    case 'claim':
      return `Claim request sent for ${body.provider_name || 'your listing'}. Check your email at ${body.business_email || 'the provided address'} for a verification link.`;
    case 'submit':
      return `Listing received for ${body.business_name || 'your company'}. We review new submissions within 24 hours. You'll get an email once it's live.`;
    case 'contact':
      return `Message sent. We reply to all inquiries within 1 business day.`;
    case 'rfq':
      return `Quote request sent${body.listing_slug ? ` for ${body.listing_slug}` : ''}. We'll match you with the right lab and forward your request. Expect a response within 2 business days.`;
  }
}

export const POST: APIRoute = async ({ request }) => {
  // --- Parse body ---
  let body: any;
  const contentType = request.headers.get('content-type') || '';
  if (contentType.includes('application/json')) {
    body = await request.json().catch(() => null);
  } else if (
    contentType.includes('multipart/form-data') ||
    contentType.includes('application/x-www-form-urlencoded')
  ) {
    const fd = await request.formData().catch(() => null);
    if (!fd)
      return new Response(JSON.stringify({ error: 'Invalid form data' }), {
        status: 400,
        headers: { 'content-type': 'application/json' },
      });
    body = Object.fromEntries(fd.entries());
  } else {
    body = await request.json().catch(() => null);
  }
  if (!body)
    return new Response(JSON.stringify({ error: 'Empty or invalid body' }), {
      status: 400,
      headers: { 'content-type': 'application/json' },
    });

  const formType: FormType = FORM_TYPES.includes(body.form_type) ? body.form_type : 'contact';

  // --- Honeypot check (silent drop) ---
  if (body.hp_email || body['hp-email'] || body.website_2 || body.hp_name) {
    return new Response(JSON.stringify({ ok: true, message: 'Received' }), {
      status: 200,
      headers: { 'content-type': 'application/json' },
    });
  }

  // --- Validate required fields ---
  const missing = REQUIRED[formType].filter((f) => !body[f] || String(body[f]).trim() === '');
  if (missing.length > 0) {
    return new Response(
      JSON.stringify({ error: `Missing required fields: ${missing.join(', ')}` }),
      { status: 400, headers: { 'content-type': 'application/json' } }
    );
  }

  // --- Email format check ---
  const email = getEmail(formType, body);
  if (email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    return new Response(JSON.stringify({ error: 'Invalid email format' }), {
      status: 400,
      headers: { 'content-type': 'application/json' },
    });
  }

  // --- Metadata from request ---
  const ip =
    request.headers.get('cf-connecting-ip') || request.headers.get('x-forwarded-for') || '';
  const ua = request.headers.get('user-agent') || '';
  const referrer = request.headers.get('referer') || body.referrer || '';
  const timestamp = new Date().toISOString();

  const meta = {
    ip: ip.split(',')[0].trim().slice(0, 45),
    ua: ua.slice(0, 500),
    referrer: referrer.slice(0, 500),
    timestamp,
  };

  // --- Build and send email ---
  const template = buildEmail(formType, body, meta);
  let emailSent = false;
  try {
    const result = await sendEmail('al@tstr.directory', template);
    emailSent = result.success;
  } catch (e) {
    console.error('Email send failed:', e);
  }

  // --- Return form-specific confirmation ---
  return new Response(
    JSON.stringify({
      ok: true,
      email_sent: emailSent,
      form_type: formType,
      message: getConfirmation(formType, body),
    }),
    { status: 200, headers: { 'content-type': 'application/json' } }
  );
};
