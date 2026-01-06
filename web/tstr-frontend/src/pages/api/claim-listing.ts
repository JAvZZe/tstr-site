import type { APIRoute } from 'astro'
import { supabase } from '../../lib/supabase'
import { canAutoClaim, generateVerificationToken } from '../../lib/domain-verification'
import { sendEmail, createVerificationEmail } from '../../lib/email'

export const POST: APIRoute = async ({ request }) => {
  try {
    // Get request data
    const { listingId } = await request.json()

    if (!listingId) {
      return new Response(JSON.stringify({
        error: 'Missing listing ID'
      }), {
        status: 400,
        headers: { 'Content-Type': 'application/json' }
      })
    }

    // Get authenticated user
    const { data: { user }, error: authError } = await supabase.auth.getUser()

    if (authError || !user) {
      return new Response(JSON.stringify({
        error: 'Authentication required'
      }), {
        status: 401,
        headers: { 'Content-Type': 'application/json' }
      })
    }

    // Get listing details
    const { data: listing, error: listingError } = await supabase
      .from('listings')
      .select('id, name, website, contact_email, claimed, claimed_at')
      .eq('id', listingId)
      .single()

    if (listingError || !listing) {
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

    // Check if user already has a claim on this listing
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

    // Check if auto-claim is possible
    const canAuto = canAutoClaim(user.email, listing.website)

    if (canAuto) {
      // Auto-approve claim
      const { error: claimError } = await supabase
        .from('listing_owners')
        .insert({
          user_id: user.id,
          listing_id: listingId,
          status: 'verified',
          verification_method: 'domain_match',
          verified_at: new Date().toISOString()
        })

      if (claimError) {
        console.error('Auto-claim error:', claimError)
        return new Response(JSON.stringify({
          error: 'Failed to claim listing automatically'
        }), {
          status: 500,
          headers: { 'Content-Type': 'application/json' }
        })
      }

      // Mark listing as claimed
      const { error: updateError } = await supabase
        .from('listings')
        .update({
          claimed: true,
          claimed_at: new Date().toISOString()
        })
        .eq('id', listingId)

      if (updateError) {
        console.error('Listing update error:', updateError)
        // Don't fail the whole operation if this update fails
      }

      return new Response(JSON.stringify({
        success: true,
        method: 'auto',
        message: `Successfully claimed "${listing.name}"! You are now the verified owner.`,
        claim: {
          status: 'verified',
          method: 'domain_match',
          verified_at: new Date().toISOString()
        }
      }), {
        status: 200,
        headers: { 'Content-Type': 'application/json' }
      })

    } else {
      // Manual verification required
      const verificationToken = generateVerificationToken()
      const expiresAt = new Date(Date.now() + 24 * 60 * 60 * 1000) // 24 hours

      const { error: claimError } = await supabase
        .from('listing_owners')
        .insert({
          user_id: user.id,
          listing_id: listingId,
          status: 'pending',
          verification_method: 'email_verification',
          verification_token: verificationToken,
          token_expires_at: expiresAt.toISOString()
        })

      if (claimError) {
        console.error('Manual claim error:', claimError)
        return new Response(JSON.stringify({
          error: 'Failed to initiate claim process'
        }), {
          status: 500,
          headers: { 'Content-Type': 'application/json' }
        })
      }

      // Send verification email to listing contact
      const emailTemplate = createVerificationEmail(
        listing.name,
        verificationToken,
        expiresAt.toISOString()
      )
      const emailResult = await sendEmail(listing.contact_email || user.email, emailTemplate)

      if (!emailResult.success) {
        console.error('Verification email failed:', emailResult.error)
      }

      return new Response(JSON.stringify({
        success: true,
        method: 'manual',
        message: emailResult.success
          ? `Claim initiated for "${listing.name}". A verification email has been sent to the listing contact.`
          : `Claim initiated for "${listing.name}". Email delivery failed - please contact support.`,
        claim: {
          status: 'pending',
          method: 'email_verification',
          token: verificationToken, // Remove in production
          expires_at: expiresAt.toISOString()
        }
      }), {
        status: 200,
        headers: { 'Content-Type': 'application/json' }
      })
    }

  } catch (error) {
    console.error('Claim listing API error:', error)
    return new Response(JSON.stringify({
      error: 'Internal server error'
    }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' }
    })
  }
}