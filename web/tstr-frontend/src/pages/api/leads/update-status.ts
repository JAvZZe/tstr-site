import type { APIRoute } from 'astro'
import { supabase } from '../../../lib/supabase'

export const POST: APIRoute = async ({ request }) => {
  try {
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

    // Get request data
    const { leadId, status, notes } = await request.json()

    if (!leadId || !status) {
      return new Response(JSON.stringify({
        error: 'Missing required fields: leadId, status'
      }), {
        status: 400,
        headers: { 'Content-Type': 'application/json' }
      })
    }

    // Validate status
    const validStatuses = ['new', 'contacted', 'qualified', 'converted', 'lost']
    if (!validStatuses.includes(status)) {
      return new Response(JSON.stringify({
        error: 'Invalid status. Must be one of: ' + validStatuses.join(', ')
      }), {
        status: 400,
        headers: { 'Content-Type': 'application/json' }
      })
    }

    // Update the lead status using the database function
    const { error } = await supabase.rpc('update_lead_status', {
      p_lead_id: leadId,
      p_status: status,
      p_owner_notes: notes || null
    })

    if (error) {
      console.error('Update lead status error:', error)
      return new Response(JSON.stringify({
        error: 'Failed to update lead status'
      }), {
        status: 500,
        headers: { 'Content-Type': 'application/json' }
      })
    }

    return new Response(JSON.stringify({
      success: true,
      message: 'Lead status updated successfully'
    }), {
      status: 200,
      headers: { 'Content-Type': 'application/json' }
    })

  } catch (error: unknown) {
    const errorMsg = error instanceof Error ? error.message : String(error)
    console.error('Update lead status API error:', error)
    return new Response(JSON.stringify({
      error: 'Internal server error',
      details: errorMsg
    }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' }
    })
  }
}