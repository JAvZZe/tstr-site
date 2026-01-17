import type { APIRoute } from 'astro';
import { Resend } from 'resend';

const resend = new Resend(import.meta.env.RESEND_API_KEY);

// Routing map
const EMAIL_ROUTING: Record<string, string> = {
    'quotation': 'sales@tstr.directory',
    'sales': 'sales@tstr.directory',
    'support': 'support@tstr.directory',
    'partnership': 'admin@tstr.directory',
    'general': 'admin@tstr.directory',
    'other': 'admin@tstr.directory',
};

export const POST: APIRoute = async ({ request }) => {
    try {
        const formData = await request.formData();
        const name = formData.get('name')?.toString() || '';
        const email = formData.get('email')?.toString() || '';
        const company = formData.get('company')?.toString() || '';
        const inquiryType = formData.get('inquiryType')?.toString() || 'general';
        const message = formData.get('message')?.toString() || '';

        // Validation
        if (!name || !email || !message) {
            return new Response(JSON.stringify({ error: 'Name, email, and message are required' }), {
                status: 400,
                headers: { 'Content-Type': 'application/json' }
            });
        }

        // Get destination email
        const toEmail = EMAIL_ROUTING[inquiryType] || 'admin@tstr.directory';

        // Format inquiry type for display
        const typeLabels: Record<string, string> = {
            'quotation': 'Request Quotation',
            'sales': 'Sales Inquiry',
            'support': 'Technical Support',
            'partnership': 'Partnership Opportunity',
            'general': 'General Inquiry',
            'other': 'Other',
        };

        // Send email via Resend
        const { error } = await resend.emails.send({
            from: 'TSTR.directory <noreply@tstr.directory>',
            to: toEmail,
            replyTo: email,
            subject: `[TSTR Contact] ${typeLabels[inquiryType] || 'Inquiry'} from ${name}`,
            html: `
        <div style="font-family: sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #eee; border-radius: 8px;">
          <h2 style="color: #000080; border-bottom: 2px solid #32CD32; padding-bottom: 10px;">New Contact Form Submission</h2>
          <div style="margin: 20px 0;">
            <p><strong>Type:</strong> ${typeLabels[inquiryType] || inquiryType}</p>
            <p><strong>Name:</strong> ${name}</p>
            <p><strong>Email:</strong> <a href="mailto:${email}" style="color: #000080;">${email}</a></p>
            <p><strong>Company:</strong> ${company || 'Not provided'}</p>
          </div>
          <div style="background: #f9fafb; padding: 15px; border-radius: 4px; color: #333;">
            <p><strong>Message:</strong></p>
            <p style="white-space: pre-wrap;">${message}</p>
          </div>
          <p style="margin-top: 20px; font-size: 12px; color: #666; text-align: center;">Sent from TSTR.directory Contact Form</p>
        </div>
      `,
        });

        if (error) {
            console.error('Resend error:', error);
            return new Response(JSON.stringify({ error: 'Failed to send message' }), {
                status: 500,
                headers: { 'Content-Type': 'application/json' }
            });
        }

        return new Response(JSON.stringify({ success: true }), {
            status: 200,
            headers: { 'Content-Type': 'application/json' }
        });
    } catch (err) {
        console.error('Contact form error:', err);
        return new Response(JSON.stringify({ error: 'Server error' }), {
            status: 500,
            headers: { 'Content-Type': 'application/json' }
        });
    }
};
