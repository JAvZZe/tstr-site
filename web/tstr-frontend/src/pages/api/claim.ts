import type { APIRoute } from 'astro'
import { supabase } from '../../lib/supabase'
import { canAutoClaim, generateVerificationToken } from '../../lib/domain-verification'

export const POST: APIRoute = async ({ request }) => {
  try {
    const data = await request.json()
    const { mode = 'claim', listingId, resumeToken, ...claimData } = data

    // Get authenticated user (may be null for anonymous claims)
    const { data: { user } } = await supabase.auth.getUser()

    // Handle resume token for draft access
    if (resumeToken && !user) {
      const { data: draftClaim } = await supabase
        .from('claims')
        .select('*')
        .eq('resume_token', resumeToken)
        .gt('draft_expires_at', new Date().toISOString())
        .single()

      if (!draftClaim) {
        return new Response(JSON.stringify({
          error: 'Invalid or expired resume token'
        }), {
          status: 400,
          headers: { 'Content-Type': 'application/json' }
        })
      }

      // Return draft data for form population
      return new Response(JSON.stringify({
        success: true,
        mode: 'resume',
        draft: draftClaim.draft_data,
        expires_at: draftClaim.draft_expires_at
      }), {
        status: 200,
        headers: { 'Content-Type': 'application/json' }
      })
    }

    // Handle draft saving
    if (mode === 'save_draft') {
      const resumeToken = await supabase.rpc('generate_resume_token')
      const expiresAt = new Date(Date.now() + 30 * 24 * 60 * 60 * 1000) // 30 days

      const { data: draft, error } = await supabase
        .from('claims')
        .insert({
          provider_name: claimData.provider_name,
          contact_name: claimData.contact_name,
          business_email: claimData.business_email,
          phone: claimData.phone,
          draft_data: claimData,
          resume_token: resumeToken,
          draft_expires_at: expiresAt.toISOString(),
          verification_status: 'pending'
        })
        .select()
        .single()

      if (error) {
        console.error('Draft save error:', error)
        return new Response(JSON.stringify({
          error: 'Failed to save draft'
        }), {
          status: 500,
          headers: { 'Content-Type': 'application/json' }
        })
      }

      // TODO: Send email with resume link
      console.log(`Draft saved. Resume token: ${resumeToken}`)

      return new Response(JSON.stringify({
        success: true,
        mode: 'draft_saved',
        resume_token: resumeToken,
        expires_at: expiresAt.toISOString(),
        message: 'Draft saved successfully. Check your email for a resume link.'
      }), {
        status: 200,
        headers: { 'Content-Type': 'application/json' }
      })
    }

    // Handle claim submission (authenticated or anonymous)
    if (!claimData.business_email || !claimData.provider_name || !claimData.contact_name) {
      return new Response(JSON.stringify({
        error: 'Missing required fields: provider_name, contact_name, and business_email are required'
      }), {
        status: 400,
        headers: { 'Content-Type': 'application/json' }
      })
    }

    // Email validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    if (!emailRegex.test(claimData.business_email)) {
      return new Response(JSON.stringify({
        error: 'Invalid email format'
      }), {
        status: 400,
        headers: { 'Content-Type': 'application/json' }
      })
    }

    // Check domain verification for ALL claims
    let domainVerified = false
    let verificationMethod = 'manual_review'

    if (user) {
      // For authenticated users, check against their email domain
      domainVerified = canAutoClaim(user.email, claimData.website || '')
      if (domainVerified) {
        verificationMethod = 'domain_match'
      }
    } else {
      // For anonymous claims, check business email domain
      // This is a simplified check - in production, you'd verify domain ownership
      const emailDomain = claimData.business_email.split('@')[1]
      if (emailDomain && claimData.website) {
        const websiteDomain = new URL(claimData.website).hostname.replace('www.', '')
        domainVerified = emailDomain === websiteDomain
        if (domainVerified) {
          verificationMethod = 'domain_match'
        }
      }
    }

    // Handle existing listing claims (authenticated users only)
    if (listingId && user) {
      const { data: listing } = await supabase
        .from('listings')
        .select('id, name, website, claimed')
        .eq('id', listingId)
        .single()

      if (!listing) {
        return new Response(JSON.stringify({
          error: 'Listing not found'
        }), {
          status: 404,
          headers: { 'Content-Type': 'application/json' }
        })
      }

      if (listing.claimed) {
        return new Response(JSON.stringify({
          error: 'This listing has already been claimed'
        }), {
          status: 409,
          headers: { 'Content-Type': 'application/json' }
        })
      }

      // Check existing claim
      const { data: existingClaim } = await supabase
        .from('listing_owners')
        .select('id, status')
        .eq('user_id', user.id)
        .eq('listing_id', listingId)
        .single()

      if (existingClaim) {
        return new Response(JSON.stringify({
          error: existingClaim.status === 'pending'
            ? 'You already have a pending claim on this listing'
            : 'You are already the owner of this listing'
        }), {
          status: 409,
          headers: { 'Content-Type': 'application/json' }
        })
      }

      // Insert listing owner claim
      const claimData = {
        user_id: user.id,
        listing_id: listingId,
        status: domainVerified ? 'verified' : 'pending',
        verification_method: verificationMethod,
        verified_at: domainVerified ? new Date().toISOString() : null
      }

      const { error: claimError } = await supabase
        .from('listing_owners')
        .insert(claimData)

      if (claimError) {
        console.error('Claim error:', claimError)
        return new Response(JSON.stringify({
          error: 'Failed to process claim'
        }), {
          status: 500,
          headers: { 'Content-Type': 'application/json' }
        })
      }

      if (domainVerified) {
        // Mark listing as claimed
        await supabase
          .from('listings')
          .update({
            claimed: true,
            claimed_at: new Date().toISOString()
          })
          .eq('id', listingId)
      }

      return new Response(JSON.stringify({
        success: true,
        method: domainVerified ? 'auto' : 'manual',
        message: domainVerified
          ? `Successfully claimed "${listing.name}"! You are now the verified owner.`
          : `Claim submitted for "${listing.name}". ${domainVerified ? 'Verified automatically.' : 'Manual verification required.'}`,
        claim: {
          status: domainVerified ? 'verified' : 'pending',
          method: verificationMethod,
          verified_at: domainVerified ? new Date().toISOString() : null
        }
      }), {
        status: 200,
        headers: { 'Content-Type': 'application/json' }
      })
    }

    // Handle new claim submissions (anonymous or authenticated)
    const verificationToken = domainVerified ? null : generateVerificationToken()
    const expiresAt = new Date(Date.now() + 24 * 60 * 60 * 1000) // 24 hours

    const newClaim = {
      provider_name: claimData.provider_name,
      contact_name: claimData.contact_name,
      business_email: claimData.business_email,
      phone: claimData.phone,
      website: claimData.website,
      verification_status: domainVerified ? 'verified' : 'pending',
      verification_method: verificationMethod,
      verified_at: domainVerified ? new Date().toISOString() : null,
      domain_verified: domainVerified,
      ...(verificationToken && {
        verification_token: verificationToken,
        token_expires_at: expiresAt.toISOString()
      })
    }

    const { data: insertedClaim, error } = await supabase
      .from('claims')
      .insert(newClaim)
      .select()
      .single()

    if (error) {
      console.error('Claim submission error:', error)
      return new Response(JSON.stringify({
        error: 'Failed to submit claim'
      }), {
        status: 500,
        headers: { 'Content-Type': 'application/json' }
      })
    }

    // TODO: Send verification email if manual verification required
    if (!domainVerified) {
      console.log(`Verification needed for ${claimData.provider_name}. Token: ${verificationToken}`)
    }

    return new Response(JSON.stringify({
      success: true,
      method: domainVerified ? 'auto' : 'manual',
      message: domainVerified
        ? 'Claim verified automatically! Your listing will be processed shortly.'
        : 'Claim submitted successfully. A verification email has been sent.',
      claim: {
        id: insertedClaim.id,
        status: domainVerified ? 'verified' : 'pending',
        method: verificationMethod,
        ...(verificationToken && {
          token: verificationToken, // Remove in production
          expires_at: expiresAt.toISOString()
        })
      }
    }), {
      status: 200,
      headers: { 'Content-Type': 'application/json' }
    })

  } catch (error) {
    console.error('Unified claim API error:', error)
    return new Response(JSON.stringify({
      error: 'Internal server error'
    }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' }
    })
  }
}