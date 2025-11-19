/**
 * ⚠️ CENTRALIZED CONTACT CONFIGURATION - READ THIS! ⚠️
 *
 * This is the SINGLE SOURCE OF TRUTH for all contact emails on TSTR.site
 *
 * WHY THIS EXISTS:
 * - Change email once here, updates everywhere on the site
 * - Prevents scattered hardcoded emails across 20+ files
 * - Type-safe references (TypeScript autocomplete)
 * - Easy maintenance as project scales
 *
 * HOW TO USE:
 * 1. In Astro pages: import { CONTACTS, MAILTO_LINKS } from '../lib/contacts'
 * 2. Use MAILTO_LINKS.professionalPlan for pre-configured links
 * 3. Use CONTACTS.sales for displaying email addresses
 * 4. Use getMailtoLink('sales', 'subject') for custom links
 *
 * CRITICAL RULES FOR ALL AGENTS:
 * ✅ DO: Import and use this file for ALL contact email needs
 * ❌ DON'T: Hardcode email addresses like "mailto:someone@tstr.site"
 * ✅ DO: Update this file when changing contact emails
 * ❌ DON'T: Create duplicate contact configs elsewhere
 *
 * CURRENT CONFIGURATION:
 * - All emails route to: tstr.site1@gmail.com
 * - Updated: 2025-11-19
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
