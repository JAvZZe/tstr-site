import { Resend } from 'resend'

let resend: Resend | null = null

function getResendClient(): Resend {
  if (!resend) {
    const apiKey = process.env.RESEND_API_KEY
    if (!apiKey) {
      throw new Error('RESEND_API_KEY environment variable is not set')
    }
    resend = new Resend(apiKey)
  }
  return resend
}

export interface EmailTemplate {
  subject: string
  html: string
  text?: string
}

export const sendEmail = async (
  to: string,
  template: EmailTemplate
): Promise<{ success: boolean; error?: string }> => {
  try {
    const resendClient = getResendClient()
    const { data, error } = await resendClient.emails.send({
      from: process.env.RESEND_FROM_EMAIL || 'noreply@tstr.directory',
      to: [to],
      subject: template.subject,
      html: template.html,
      text: template.text,
    })

    if (error) {
      console.error('Email send error:', error)
      return { success: false, error: error.message }
    }

    return { success: true }
  } catch (err) {
    console.error('Email service error:', err)
    return { success: false, error: 'Email service unavailable' }
  }
}

export const createDraftSaveEmail = (resumeToken: string, expiresAt: string): EmailTemplate => ({
  subject: 'Resume Your TSTR.directory Claim',
  html: `
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
      <div style="text-align: center; margin-bottom: 30px;">
        <h1 style="color: #2563EB; margin: 0;">TSTR.directory</h1>
        <p style="color: #6B7280; margin: 5px 0;">Testing Services Directory</p>
      </div>

      <div style="background-color: #F9FAFB; padding: 30px; border-radius: 8px; margin-bottom: 30px;">
        <h2 style="color: #1F2937; margin-top: 0;">Resume Your Claim</h2>
        <p style="color: #4B5563; line-height: 1.6;">
          You've saved a draft claim on TSTR.directory. Click the link below to resume where you left off:
        </p>

        <div style="text-align: center; margin: 30px 0;">
          <a href="https://tstr.directory/claim?resume=${resumeToken}"
             style="background-color: #2563EB; color: white; padding: 14px 28px; text-decoration: none; border-radius: 6px; font-weight: 600; display: inline-block;">
            Resume Your Claim
          </a>
        </div>

        <div style="background-color: white; padding: 20px; border-radius: 6px; border-left: 4px solid #2563EB;">
          <p style="margin: 0; color: #374151; font-size: 14px;">
            <strong>Expires:</strong> ${new Date(expiresAt).toLocaleDateString('en-US', {
              weekday: 'long',
              year: 'numeric',
              month: 'long',
              day: 'numeric'
            })}
          </p>
          <p style="margin: 10px 0 0 0; color: #6B7280; font-size: 14px;">
            Save this email for your records. If you didn't save this draft, you can safely ignore this message.
          </p>
        </div>
      </div>

      <div style="text-align: center; color: #9CA3AF; font-size: 12px;">
        <p>This is an automated message from TSTR.directory. Please do not reply to this email.</p>
      </div>
    </div>
  `,
  text: `Resume your TSTR.directory claim: https://tstr.directory/claim?resume=${resumeToken}

Expires: ${new Date(expiresAt).toLocaleDateString()}

This is an automated message from TSTR.directory. If you didn't save this draft, you can safely ignore this email.`
})

export const createVerificationEmail = (
  providerName: string,
  verificationToken: string,
  expiresAt: string
): EmailTemplate => ({
  subject: 'Verify Your TSTR.directory Claim',
  html: `
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
      <div style="text-align: center; margin-bottom: 30px;">
        <h1 style="color: #2563EB; margin: 0;">TSTR.directory</h1>
        <p style="color: #6B7280; margin: 5px 0;">Testing Services Directory</p>
      </div>

      <div style="background-color: #F9FAFB; padding: 30px; border-radius: 8px; margin-bottom: 30px;">
        <h2 style="color: #1F2937; margin-top: 0;">Verify Your Claim</h2>
        <p style="color: #4B5563; line-height: 1.6;">
          A claim has been submitted for <strong>${providerName}</strong> on TSTR.directory.
          To verify ownership and complete the claim process, please use the verification code below:
        </p>

        <div style="text-align: center; margin: 30px 0;">
          <div style="background-color: white; border: 2px solid #2563EB; border-radius: 8px; padding: 20px; display: inline-block;">
            <div style="font-family: monospace; font-size: 24px; font-weight: bold; color: #2563EB; letter-spacing: 2px;">
              ${verificationToken}
            </div>
          </div>
        </div>

        <div style="background-color: #FEF3C7; padding: 20px; border-radius: 6px; border-left: 4px solid #F59E0B;">
          <p style="margin: 0; color: #92400E; font-size: 14px;">
            <strong>Important:</strong> This code expires on ${new Date(expiresAt).toLocaleDateString('en-US', {
              weekday: 'long',
              year: 'numeric',
              month: 'long',
              day: 'numeric'
            })}. For security reasons, verification codes are only valid for 24 hours.
          </p>
        </div>
      </div>

      <div style="background-color: #F3F4F6; padding: 20px; border-radius: 6px; margin-bottom: 20px;">
        <h3 style="color: #374151; margin-top: 0;">What happens next?</h3>
        <ol style="color: #4B5563; line-height: 1.6;">
          <li>Enter the verification code on the claim page</li>
          <li>Your claim will be reviewed by our team</li>
          <li>You'll receive confirmation once approved</li>
          <li>Your listing will be marked as verified</li>
        </ol>
      </div>

      <div style="text-align: center; color: #9CA3AF; font-size: 12px;">
        <p>This is an automated message from TSTR.directory. Please do not reply to this email.</p>
        <p>If you didn't submit this claim, you can safely ignore this message.</p>
      </div>
    </div>
  `,
  text: `Verify your TSTR.directory claim for ${providerName}

Verification Code: ${verificationToken}

Expires: ${new Date(expiresAt).toLocaleDateString()}

What happens next:
1. Enter the verification code on the claim page
2. Your claim will be reviewed by our team
3. You'll receive confirmation once approved
4. Your listing will be marked as verified

This is an automated message from TSTR.directory. If you didn't submit this claim, you can safely ignore this message.`
})

export const generateVerificationToken = (): string => {
  // Generate a 6-character alphanumeric token
  const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
  let token = ''
  for (let i = 0; i < 6; i++) {
    token += chars.charAt(Math.floor(Math.random() * chars.length))
  }
  return token
}