import type { APIRoute } from 'astro'
import { supabase } from '../../../lib/supabase'

export const POST: APIRoute = async ({ request }) => {
  try {
    // Get authenticated user
    const { data: { user }, error: authError } = await supabase.auth.getUser()

    if (authError || !user) {
      return new Response(JSON.stringify({
        success: false,
        message: 'Authentication required'
      }), {
        status: 401,
        headers: { 'Content-Type': 'application/json' }
      })
    }

    // Parse request data
    const { listingId, business_name, description, address, phone, email, website } = await request.json()

    if (!listingId) {
      return new Response(JSON.stringify({
        success: false,
        message: 'Listing ID is required'
      }), {
        status: 400,
        headers: { 'Content-Type': 'application/json' }
      })
    }

    // Verify ownership - user must be a verified owner of this listing
    const { data: ownership, error: ownershipError } = await supabase
      .from('listing_owners')
      .select('status, verification_method')
      .eq('user_id', user.id)
      .eq('listing_id', listingId)
      .eq('status', 'verified')
      .single()

    if (ownershipError || !ownership) {
      return new Response(JSON.stringify({
        success: false,
        message: 'You do not have permission to edit this listing'
      }), {
        status: 403,
        headers: { 'Content-Type': 'application/json' }
      })
    }

    // Validate required fields
    if (!business_name || business_name.trim().length === 0) {
      return new Response(JSON.stringify({
        success: false,
        message: 'Business name is required'
      }), {
        status: 400,
        headers: { 'Content-Type': 'application/json' }
      })
    }

    // Prepare update data with sanitization
    const updateData: Record<string, unknown> = {
      business_name: business_name.trim(),
      updated_at: new Date().toISOString()
    }

    // Optional fields
    if (description !== undefined) {
      updateData.description = description ? description.trim() : null
    }

    if (address !== undefined) {
      updateData.address = address ? address.trim() : null
    }

    if (phone !== undefined) {
      updateData.phone = phone ? phone.trim() : null
    }

    if (email !== undefined) {
      updateData.email = email ? email.trim().toLowerCase() : null
    }

    if (website !== undefined) {
      updateData.website = website ? website.trim() : null
    }

    // Update the listing
    const { data: updatedListing, error: updateError } = await supabase
      .from('listings')
      .update(updateData)
      .eq('id', listingId)
      .select('id, business_name, updated_at')
      .single()

    if (updateError) {
      console.error('Listing update error:', updateError)
      return new Response(JSON.stringify({
        success: false,
        message: 'Failed to update listing'
      }), {
        status: 500,
        headers: { 'Content-Type': 'application/json' }
      })
    }

    // Log the change for audit purposes (store in a simple audit log)
    // For now, we'll log to console. In production, this could be stored in a database table
    console.log(`AUDIT: User ${user.id} (${user.email}) updated listing ${listingId} (${updatedListing.business_name}) at ${new Date().toISOString()}`)

    // You could also send a notification email to admins about the change
    // This would be implemented in a separate service

    return new Response(JSON.stringify({
      success: true,
      message: 'Listing updated successfully',
      listing: updatedListing
    }), {
      status: 200,
      headers: { 'Content-Type': 'application/json' }
    })

  } catch (error) {
    console.error('Listing update API error:', error)
    return new Response(JSON.stringify({
      success: false,
      message: 'Internal server error'
    }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' }
    })
  }
}