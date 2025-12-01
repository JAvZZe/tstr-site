import type { APIRoute } from 'astro'
import { supabase } from '../../lib/supabase'

export const POST: APIRoute = async ({ request }) => {
  try {
    const { token, code } = await request.json()

    if (!token || !code) {
      return new Response(JSON.stringify({
        error: 'Missing verification token or code'
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

    // Find the pending claim
    const { data: claim, error: claimError } = await supabase
      .from('listing_owners')
      .select('*')
      .eq('verification_token', token)
      .eq('user_id', user.id)
      .eq('status', 'pending')
      .single()

    if (claimError || !claim) {
      return new Response(JSON.stringify({
        error: 'Invalid or expired verification token'
      }), {
        status: 400,
        headers: { 'Content-Type': 'application/json' }
      })
    }

    // Check if token is expired
    if (new Date(claim.token_expires_at) < new Date()) {
      return new Response(JSON.stringify({
        error: 'Verification token has expired. Please request a new claim.'
      }), {
        status: 400,
        headers: { 'Content-Type': 'application/json' }
      })
    }

    // Verify code (in development, accept any 6-digit code)
    // TODO: Implement proper OTP verification in production
    const isValidCode = /^\d{6}$/.test(code) || code === '123456' // Development fallback

    if (!isValidCode) {
      return new Response(JSON.stringify({
        error: 'Invalid verification code'
      }), {
        status: 400,
        headers: { 'Content-Type': 'application/json' }
      })
    }

    // Approve the claim
    const { error: updateError } = await supabase
      .from('listing_owners')
      .update({
        status: 'verified',
        verified_at: new Date().toISOString(),
        verification_token: null,
        token_expires_at: null
      })
      .eq('id', claim.id)

    if (updateError) {
      console.error('Claim verification update error:', updateError)
      return new Response(JSON.stringify({
        error: 'Failed to verify claim'
      }), {
        status: 500,
        headers: { 'Content-Type': 'application/json' }
      })
    }

    // Mark listing as claimed
    const { error: listingError } = await supabase
      .from('listings')
      .update({
        claimed: true,
        claimed_at: new Date().toISOString()
      })
      .eq('id', claim.listing_id)

    if (listingError) {
      console.error('Listing claim update error:', listingError)
      // Don't fail the whole operation if this update fails
    }

    // Get listing details for response
    const { data: listing } = await supabase
      .from('listings')
      .select('name')
      .eq('id', claim.listing_id)
      .single()

    return new Response(JSON.stringify({
      success: true,
      message: `Successfully verified ownership of "${listing?.name || 'listing'}"!`,
      claim: {
        id: claim.id,
        listing_id: claim.listing_id,
        status: 'verified',
        verified_at: new Date().toISOString()
      }
    }), {
      status: 200,
      headers: { 'Content-Type': 'application/json' }
    })

  } catch (error) {
    console.error('Verify claim API error:', error)
    return new Response(JSON.stringify({
      error: 'Internal server error'
    }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' }
    })
  }
}