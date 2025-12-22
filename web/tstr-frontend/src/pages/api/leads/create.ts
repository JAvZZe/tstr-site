import type { APIRoute } from 'astro'
import { supabase } from '../../../lib/supabase'

export const POST: APIRoute = async ({ request }) => {
  try {
    // Get request data
    const { listingId, contactType, contactValue } = await request.json()

    if (!listingId || !contactType || !contactValue) {
      return new Response(JSON.stringify({
        error: 'Missing required fields: listingId, contactType, contactValue'
      }), {
        status: 400,
        headers: { 'Content-Type': 'application/json' }
      })
    }

    // Validate contact type
    if (!['phone', 'email', 'website'].includes(contactType)) {
      return new Response(JSON.stringify({
        error: 'Invalid contact type. Must be: phone, email, or website'
      }), {
        status: 400,
        headers: { 'Content-Type': 'application/json' }
      })
    }

    // Get visitor information from headers
    const userAgent = request.headers.get('user-agent') || undefined
    const referrer = request.headers.get('referer') || undefined
    const forwardedFor = request.headers.get('x-forwarded-for')
    const realIp = request.headers.get('x-real-ip')
    const visitorIp = forwardedFor?.split(',')[0]?.trim() ||
                     realIp ||
                     request.headers.get('cf-connecting-ip') ||
                     undefined

    // Create the lead using the database function
    const { data: leadId, error } = await supabase.rpc('create_lead', {
      p_listing_id: listingId,
      p_contact_type: contactType,
      p_contact_value: contactValue,
      p_visitor_ip: visitorIp,
      p_user_agent: userAgent,
      p_referrer: referrer
    })

    if (error) {
      console.error('Create lead error:', error)
      return new Response(JSON.stringify({
        error: 'Failed to create lead record'
      }), {
        status: 500,
        headers: { 'Content-Type': 'application/json' }
      })
    }

    return new Response(JSON.stringify({
      success: true,
      leadId: leadId,
      message: 'Lead created successfully'
    }), {
      status: 200,
      headers: { 'Content-Type': 'application/json' }
    })

  } catch (error) {
    console.error('Create lead API error:', error)
    return new Response(JSON.stringify({
      error: 'Internal server error'
    }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' }
    })
  }
}