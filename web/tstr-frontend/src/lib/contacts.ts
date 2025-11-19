/**
 * Central contact configuration for TSTR.site
 * Update email addresses here and they'll reflect across the entire site
 */

export const CONTACTS = {
  // Sales inquiries (pricing plans, subscriptions)
  sales: 'tstr.site1@gmail.com',

  // General support (account issues, technical help)
  support: 'tstr.site1@gmail.com',

  // Partnership opportunities (integrations, co-marketing)
  partnerships: 'tstr.site1@gmail.com',

  // General enquiries (questions, feedback)
  enquiries: 'tstr.site1@gmail.com',

  // Legal/compliance matters
  legal: 'tstr.site1@gmail.com',
} as const

/**
 * Helper function to generate mailto links
 */
export function getMailtoLink(
  type: keyof typeof CONTACTS,
  subject?: string,
  body?: string
): string {
  const email = CONTACTS[type]
  const params = new URLSearchParams()

  if (subject) params.set('subject', subject)
  if (body) params.set('body', body)

  const queryString = params.toString()
  return `mailto:${email}${queryString ? `?${queryString}` : ''}`
}

/**
 * Pre-configured mailto links for common actions
 */
export const MAILTO_LINKS = {
  professionalPlan: getMailtoLink('sales', 'Professional Plan Inquiry'),
  premiumPlan: getMailtoLink('sales', 'Premium Plan Inquiry'),
  enterprisePlan: getMailtoLink('sales', 'Enterprise Plan Inquiry'),
  generalInquiry: getMailtoLink('enquiries', 'General Inquiry'),
  support: getMailtoLink('support', 'Support Request'),
  partnership: getMailtoLink('partnerships', 'Partnership Opportunity'),
  claimListing: getMailtoLink('support', 'Claim My Listing'),
  reportIssue: getMailtoLink('support', 'Report an Issue'),
} as const
