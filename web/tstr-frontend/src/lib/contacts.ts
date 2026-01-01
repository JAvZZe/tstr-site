/**
 * ⚠️ CENTRALIZED SITE CONFIGURATION - READ THIS! ⚠️
 *
 * This is the SINGLE SOURCE OF TRUTH for:
 * - Contact emails
 * - Disclaimers and legal text
 * - Site-wide content strings
 * - Any text that appears in multiple places
 *
 * WHY THIS EXISTS:
 * - Change text once here, updates everywhere on the site
 * - Prevents scattered hardcoded content across 20+ files
 * - Type-safe references (TypeScript autocomplete)
 * - Easy maintenance as project scales
 *
 * HOW TO USE:
 * 1. In Astro pages: import { CONTACTS, MAILTO_LINKS, CONTENT } from '../lib/contacts'
 * 2. Use CONTENT.disclaimer for standard disclaimer text
 * 3. Use MAILTO_LINKS.professionalPlan for pre-configured links
 * 4. Use CONTACTS.sales for displaying email addresses
 *
 * CRITICAL RULES FOR ALL AGENTS:
 * ✅ DO: Import and use this file for ALL site-wide content
 * ❌ DON'T: Hardcode content like disclaimers, emails, or repeated text
 * ✅ DO: Update this file when changing site-wide content
 * ❌ DON'T: Create duplicate content configs elsewhere
 *
 * CURRENT CONFIGURATION:
 * - All emails route to: tstr.site1@gmail.com
 * - Updated: 2025-11-19 - Added CONTENT section for disclaimers
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
  verificationPricing: getMailtoLink('sales', 'Verification Service Pricing Request'),
} as const

/**
 * Site-wide content strings
 * Use these for any text that appears in multiple places or may change over time
 */
export const CONTENT = {
  // Disclaimers and legal text
  // Note: disclaimerLink is rendered as a separate bold link element in components
  disclaimer: `Disclaimer: Certifications and capabilities listed are extracted from public databases and have not been independently verified by TSTR.directory. We recommend verifying all credentials directly with the testing laboratory and relevant accreditation bodies before engaging services.`,
  
  disclaimerLink: {
    text: 'Click here to commission us to verify credentials for you.',
    href: '/pricing#verification', // Links to verification pricing section
  },

  disclaimerShort: `Information extracted from public databases. Verify credentials directly with laboratories before engaging services.`,

  // Site taglines and descriptions
  tagline: 'Specialist Testing Services, Products and Solutions Directory',

  description: 'Global directory of testing laboratories serving specialized industries: Oil & Gas, Environmental, Materials Testing, Pharmaceuticals, and more.',

  // Common CTAs
  cta: {
    listYourLab: 'List Your Lab',
    getStartedFree: 'Get Started Free',
    contactSales: 'Contact Sales',
    learnMore: 'Learn More',
    upgradePlan: 'Upgrade Plan',
    requestVerification: 'Request Verification',
  },

  // Footer text
  copyright: `© ${new Date().getFullYear()} TSTR Hub. All rights reserved.`,
  
  footerTagline: 'Connecting industries with certified testers worldwide',
  
   footerLinks: [
     { href: '/terms', label: 'Terms of Service' },
     { href: '/privacy', label: 'Privacy Policy' },
     { href: '/pricing', label: 'Pricing' },
     { href: '/submit', label: 'List Your Company' },
     { href: 'https://linkedin.com/company/tstr-hub', label: 'LinkedIn', icon: 'linkedin' },
   ],
} as const
