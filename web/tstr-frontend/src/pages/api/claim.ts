import type { APIRoute } from 'astro';
import { createClient } from '@supabase/supabase-js';
import { canAutoClaim, generateVerificationToken } from '../../lib/domain-verification';
import {
  sendEmail,
  createDraftSaveEmail,
  createVerificationEmail,
  createClaimStatusEmail,
} from '../../lib/email';
import { getServiceKey } from '../../lib/supabase-admin';

const SUPABASE_URL =
  import.meta.env.PUBLIC_SUPABASE_URL || 'https://haimjeaetrsaauitrhfy.supabase.co';

function getAdmin(locals: unknown) {
  const key = getServiceKey(locals);
  if (!key) return null;
  return createClient(SUPABASE_URL, key);
}

export const POST: APIRoute = async ({ request, locals }) => {
  try {
    const data = await request.json();
    const { mode = 'claim', listingId, resumeToken, ...claimData } = data;

    const admin = getAdmin(locals);
    if (!admin) {
      return new Response(JSON.stringify({ error: 'Service key not configured' }), {
        status: 500,
        headers: { 'Content-Type': 'application/json' },
      });
    }

    // Get authenticated user (may be null for anonymous claims)
    const {
      data: { user },
    } = await admin.auth.getUser();

    // Handle resume token for draft access
    if (resumeToken && !user) {
      const { data: draftClaim } = await admin
        .from('claims')
        .select('*')
        .eq('resume_token', resumeToken)
        .gt('draft_expires_at', new Date().toISOString())
        .single();

      if (!draftClaim) {
        return new Response(JSON.stringify({ error: 'Invalid or expired resume token' }), {
          status: 400,
          headers: { 'Content-Type': 'application/json' },
        });
      }

      return new Response(
        JSON.stringify({
          success: true,
          mode: 'resume',
          draft: draftClaim.draft_data,
          expires_at: draftClaim.draft_expires_at,
        }),
        { status: 200, headers: { 'Content-Type': 'application/json' } }
      );
    }

    // Handle draft saving
    if (mode === 'save_draft') {
      const { data: resumeToken, error: tokenError } = await admin.rpc('generate_resume_token');
      const expiresAt = new Date(Date.now() + 30 * 24 * 60 * 60 * 1000);

      if (tokenError || !resumeToken) {
        console.error('Token generation error:', tokenError);
        return new Response(JSON.stringify({ error: 'Failed to generate resume token' }), {
          status: 500,
        });
      }

      const { error } = await admin.from('claims').insert({
        provider_name: claimData.provider_name,
        contact_name: claimData.contact_name,
        business_email: claimData.business_email,
        phone: claimData.phone,
        draft_data: claimData,
        resume_token: resumeToken,
        draft_expires_at: expiresAt.toISOString(),
        status: 'pending',
      });

      if (error) {
        console.error('Draft save error:', error);
        return new Response(JSON.stringify({ error: 'Failed to save draft' }), { status: 500 });
      }

      const emailTemplate = createDraftSaveEmail(resumeToken, expiresAt.toISOString());
      const emailResult = await sendEmail(claimData.business_email, emailTemplate);

      return new Response(
        JSON.stringify({
          success: true,
          mode: 'draft_saved',
          resume_token: resumeToken,
          expires_at: expiresAt.toISOString(),
          message: emailResult.success
            ? 'Draft saved successfully. Check your email for a resume link.'
            : 'Draft saved successfully. Email delivery failed - save your resume token.',
        }),
        { status: 200, headers: { 'Content-Type': 'application/json' } }
      );
    }

    // Handle claim submission
    if (!claimData.business_email || !claimData.provider_name || !claimData.contact_name) {
      return new Response(
        JSON.stringify({
          error:
            'Missing required fields: provider_name, contact_name, and business_email are required',
        }),
        { status: 400, headers: { 'Content-Type': 'application/json' } }
      );
    }

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(claimData.business_email)) {
      return new Response(JSON.stringify({ error: 'Invalid email format' }), {
        status: 400,
        headers: { 'Content-Type': 'application/json' },
      });
    }

    // Domain verification
    let domainVerified = false;
    let verificationMethod = 'admin_approval';

    if (user) {
      domainVerified = canAutoClaim(user.email, claimData.website || '');
      if (domainVerified) verificationMethod = 'domain_match';
    } else {
      const emailDomain = claimData.business_email.split('@')[1];
      if (emailDomain && claimData.website) {
        try {
          const websiteDomain = new URL(claimData.website).hostname.replace('www.', '');
          domainVerified = emailDomain === websiteDomain;
          if (domainVerified) verificationMethod = 'domain_match';
        } catch {
          // Invalid URL, fall through to manual verification
        }
      }
    }

    // Handle existing listing claims (authenticated users)
    if (listingId && user) {
      const { data: listing } = await admin
        .from('listings')
        .select('id, name, website, claimed')
        .eq('id', listingId)
        .single();

      if (!listing) {
        return new Response(JSON.stringify({ error: 'Listing not found' }), { status: 404 });
      }

      if (listing.claimed) {
        return new Response(JSON.stringify({ error: 'This listing has already been claimed' }), {
          status: 409,
        });
      }

      const { data: existingClaim } = await admin
        .from('listing_owners')
        .select('id, status')
        .eq('user_id', user.id)
        .eq('listing_id', listingId)
        .single();

      if (existingClaim) {
        return new Response(
          JSON.stringify({
            error:
              existingClaim.status === 'pending'
                ? 'You already have a pending claim on this listing'
                : 'You are already the owner of this listing',
          }),
          { status: 409 }
        );
      }

      const listingOwnerClaim = {
        user_id: user.id,
        listing_id: listingId,
        status: domainVerified ? 'verified' : 'pending',
        verification_method: verificationMethod,
        verified_at: domainVerified ? new Date().toISOString() : null,
      };

      const { error: claimError } = await admin.from('listing_owners').insert(listingOwnerClaim);

      if (claimError) {
        console.error('Claim error:', claimError);
        return new Response(JSON.stringify({ error: 'Failed to process claim' }), { status: 500 });
      }

      if (domainVerified) {
        await admin
          .from('listings')
          .update({ claimed: true, claimed_at: new Date().toISOString() })
          .eq('id', listingId);
      }

      // Notify admin
      await sendEmail('sales@tstr.directory', {
        subject: `New Claim: ${listing.name}`,
        html: `<p>A new claim was submitted for <strong>${listing.name}</strong> by ${claimData.contact_name} (${claimData.business_email}). ${domainVerified ? 'Auto-verified.' : 'Manual review required.'}</p>`,
        text: `New claim for ${listing.name} by ${claimData.contact_name} (${claimData.business_email}). ${domainVerified ? 'Auto-verified.' : 'Manual review required.'}`,
      });

      return new Response(
        JSON.stringify({
          success: true,
          method: domainVerified ? 'auto' : 'manual',
          message: domainVerified
            ? `Successfully claimed "${listing.name}"! You are now the verified owner.`
            : `Claim submitted for "${listing.name}". We'll review it shortly.`,
          claim: {
            status: domainVerified ? 'verified' : 'pending',
            method: verificationMethod,
            verified_at: domainVerified ? new Date().toISOString() : null,
          },
        }),
        { status: 200, headers: { 'Content-Type': 'application/json' } }
      );
    }

    // Handle anonymous claims (no listingId, or no user)
    const verificationToken = generateVerificationToken();
    const expiresAt = new Date(Date.now() + 24 * 60 * 60 * 1000);

    const newClaim = {
      provider_name: claimData.provider_name,
      contact_name: claimData.contact_name,
      business_email: claimData.business_email,
      phone: claimData.phone,
      website: claimData.website,
      status: domainVerified ? 'verified' : 'pending',
      verification_token: verificationToken,
      token_expires_at: expiresAt.toISOString(),
    };

    const { data: insertedClaim, error } = await admin
      .from('claims')
      .insert(newClaim)
      .select()
      .single();

    if (error) {
      console.error('Claim submission error:', error);
      return new Response(JSON.stringify({ error: 'Failed to submit claim' }), { status: 500 });
    }

    // Send verification email if manual
    if (!domainVerified) {
      const emailTemplate = createVerificationEmail(
        claimData.provider_name,
        verificationToken,
        expiresAt.toISOString()
      );
      await sendEmail(claimData.business_email, emailTemplate);
    }

    // Notify admin
    await sendEmail('sales@tstr.directory', {
      subject: `New Claim: ${claimData.provider_name}`,
      html: `<p>A new claim was submitted for <strong>${claimData.provider_name}</strong> by ${claimData.contact_name} (${claimData.business_email}). ${domainVerified ? 'Auto-verified.' : 'Manual review required.'}</p>`,
      text: `New claim for ${claimData.provider_name} by ${claimData.contact_name} (${claimData.business_email}). ${domainVerified ? 'Auto-verified.' : 'Manual review required.'}`,
    });

    return new Response(
      JSON.stringify({
        success: true,
        method: domainVerified ? 'auto' : 'manual',
        message: domainVerified
          ? 'Claim verified automatically! Your listing will be processed shortly.'
          : 'Claim submitted successfully. A verification email has been sent.',
        claim: {
          id: insertedClaim.id,
          status: domainVerified ? 'verified' : 'pending',
          method: verificationMethod,
        },
      }),
      { status: 200, headers: { 'Content-Type': 'application/json' } }
    );
  } catch (error) {
    console.error('Unified claim API error:', error);
    return new Response(JSON.stringify({ error: 'Internal server error' }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' },
    });
  }
};
