import type { APIRoute } from 'astro'
import { supabase } from '../../../lib/supabase'
import { sendEmail, createEFTPaymentEmail } from '../../../lib/email'

export const POST: APIRoute = async ({ request }) => {
    try {
        const authHeader = request.headers.get('Authorization')
        if (!authHeader?.startsWith('Bearer ')) {
            return new Response(JSON.stringify({ error: 'Missing authorization header' }), { status: 401 })
        }

        const token = authHeader.split(' ')[1]
        const { data: { user }, error: authError } = await supabase.auth.getUser(token)

        if (authError || !user) {
            return new Response(JSON.stringify({ error: 'Unauthorized' }), { status: 401 })
        }

        const { plan, amount } = await request.json()

        if (!plan || !amount) {
            return new Response(JSON.stringify({ error: 'Missing plan or amount' }), { status: 400 })
        }

        // Generate Reference (EFT-Timestamp-Random3) to ensure uniqueness
        const timestamp = Date.now().toString().slice(-4);
        const random = Math.floor(Math.random() * 1000).toString().padStart(3, '0');
        const reference = `EFT-${timestamp}-${random}`;

        // Send Email
        const emailTemplate = createEFTPaymentEmail(reference, amount, plan)
        // We trust supabase.auth.getUser to return a verified email for the user
        // However, user.email might be undefined if not returned by provider, but for email/password it is there.
        if (!user.email) {
            return new Response(JSON.stringify({ error: 'User email not found' }), { status: 400 })
        }

        const emailResult = await sendEmail(user.email, emailTemplate)

        if (!emailResult.success) {
            console.error('EFT Email failed:', emailResult.error)
            return new Response(JSON.stringify({ error: 'Failed to send payment instructions email. Please try again.' }), { status: 500 })
        }

        return new Response(JSON.stringify({
            success: true,
            reference,
            bankDetails: {
                bankName: 'First Business Zero',
                accountNumber: '63190154070',
                branchCode: '250655',
                swiftCode: 'FIRNZAJJ'
            }
        }), { status: 200 })

    } catch (error) {
        console.error('EFT API Error:', error)
        return new Response(JSON.stringify({ error: 'Internal server error' }), { status: 500 })
    }
}
