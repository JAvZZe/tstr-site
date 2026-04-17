import type { APIRoute } from 'astro';
import { supabase } from '../../lib/supabase'; 
import { sendEmail } from '../../lib/email';   

export const POST: APIRoute = async ({ request }) => {
  try {
    const body = await request.json();

    // 1. Input validation
    const { listingId, name, email, company, industry, role, message } = body;
    console.log('Received lead. listingId:', listingId);
    
    if (!name || !email || !message || !industry || !role) {
      console.log('Missing mandatory fields');
      return new Response(JSON.stringify({ error: 'Missing required fields' }), { status: 400 });
    }

    let recipientEmail = "support@tstr.directory"; // Default admin email
    let labName = "TSTR Global Support";

    // 2. Fetch listing name + email if listingId provided
    if (listingId) {
      const { data: listing, error: listingError } = await supabase
        .from('listings')
        .select('business_name, email')
        .eq('id', listingId)
        .single();

      if (listingError) {
        console.error('Error fetching listing:', listingError);
        // Fallback to admin if listing fetch fails
      } else if (listing?.email) {
        recipientEmail = listing.email;
        labName = listing.business_name;
      }
    }

    console.log('Routing lead to:', recipientEmail);

    // 3. Insert lead
    const { data: lead, error: dbError } = await supabase
      .from('leads_rfq')
      .insert({ 
        listing_id: listingId || null, 
        buyer_name: name, 
        buyer_email: email, 
        buyer_company: company, 
        buyer_industry: industry, 
        buyer_role: role, 
        message 
      })
      .select('id')
      .single();

    if (dbError) throw dbError;

    // 4. Send email
    sendEmail(recipientEmail, {
      subject: `New ${listingId ? 'RFQ' : 'General Enquiry'} from ${company || name} via TSTR.directory`,
      html: `
        <div style="font-family: sans-serif; color: #333;">
          <h2 style="color: #000080;">New Request for Quote</h2>
          <p>You have received a new ${listingId ? 'lead for <strong>' + labName + '</strong>' : 'general technical enquiry'} on TSTR.directory.</p>
          <hr style="border: 0; border-top: 1px solid #eee; margin: 1.5rem 0;" />
          <p><strong>From:</strong> ${name} (${email})</p>
          <p><strong>Company:</strong> ${company || 'Not provided'}</p>
          <p><strong>Industry:</strong> ${industry}</p>
          <p><strong>Role:</strong> ${role}</p>
          <div style="background: #f9fafb; padding: 1.5rem; border-radius: 8px; margin-top: 1rem;">
            <p style="margin-top: 0; font-weight: bold;">Message:</p>
            <p style="white-space: pre-wrap;">${message}</p>
          </div>
          <p style="margin-top: 2rem; font-size: 0.9rem; color: #666;">
            Reply directly to the customer's email to continue the conversation.
          </p>
        </div>
      `,
      text: `New Lead from ${name} (${email})\nCompany: ${company}\nRole: ${role} | Industry: ${industry}\n\nMessage:\n${message}`
    }).then(result => {
      if (result.success && lead?.id && listingId) {
        supabase.from('leads_rfq').update({ notified_lab: true }).eq('id', lead.id).then(()=>{});
      }
    });

    return new Response(JSON.stringify({ success: true }), { status: 200 });
  } catch (error: unknown) {
    console.error('Lead submission error:', error);
    const msg = error instanceof Error ? error.message : 'Unknown error';
    return new Response(JSON.stringify({ error: msg }), { status: 500 });
  }
};
