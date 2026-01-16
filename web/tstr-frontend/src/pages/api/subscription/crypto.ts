import type { APIRoute } from 'astro'
import { supabase } from '../../../lib/supabase'
import { sendEmail, createCryptoPaymentEmail } from '../../../lib/email'

const BTC_WALLET_ADDRESS = '17B2BCJfDyNeMoFZ2mbAVHnmL8CwogQFeB'

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

        // Generate Reference (BTC-Timestamp-Random3) to ensure uniqueness
        const timestamp = Date.now().toString().slice(-4);
        const random = Math.floor(Math.random() * 1000).toString().padStart(3, '0');
        const reference = `BTC-${timestamp}-${random}`;

        // Send Email
        const emailTemplate = createCryptoPaymentEmail(reference, amount, plan, BTC_WALLET_ADDRESS)

        if (!user.email) {
            return new Response(JSON.stringify({ error: 'User email not found' }), { status: 400 })
        }

        const emailResult = await sendEmail(user.email, emailTemplate)

        if (!emailResult.success) {
            console.error('Crypto Email failed:', emailResult.error)
            return new Response(JSON.stringify({
                error: `Email failed: ${emailResult.error || 'Unknown error'}. Please verify your account email is correct.`
            }), { status: 500 })
        }

        return new Response(JSON.stringify({
            success: true,
            reference,
            walletAddress: BTC_WALLET_ADDRESS
        }), { status: 200 })

    } catch (error) {
        console.error('Crypto API Error:', error)
        return new Response(JSON.stringify({ error: 'Internal server error' }), { status: 500 })
    }
}
