// Domain verification utilities for LinkedIn OAuth and rights management
// Implements corporate domain verification model

/**
 * Extract domain from URL
 * @param {string} url - The URL to extract domain from
 * @returns {string|null} - The extracted domain or null if invalid
 */
export function extractDomain(url) {
  if (!url) return null

  try {
    // Ensure URL has protocol
    const urlWithProtocol = url.startsWith('http') ? url : `https://${url}`
    const urlObj = new URL(urlWithProtocol)

    // Remove www prefix and return hostname
    return urlObj.hostname.replace(/^www\./, '').toLowerCase()
  } catch (error) {
    console.warn('Invalid URL for domain extraction:', url, error)
    return null
  }
}

/**
 * Extract domain from email address
 * @param {string} email - The email address
 * @returns {string|null} - The domain part or null if invalid
 */
export function extractEmailDomain(email) {
  if (!email || !email.includes('@')) return null
  return email.split('@')[1].toLowerCase()
}

/**
 * Check if user can auto-claim a listing based on domain matching
 * @param {string} userEmail - User's email address
 * @param {string} listingWebsite - Listing's website URL
 * @returns {boolean} - True if auto-claim is possible
 */
export function canAutoClaim(userEmail, listingWebsite) {
  const userDomain = extractEmailDomain(userEmail)
  const listingDomain = extractDomain(listingWebsite)

  if (!userDomain || !listingDomain) return false

  // Exact match
  if (userDomain === listingDomain) return true

  // Handle common TLD variations (remove .com, .org, etc. and compare)
  const normalizedUser = userDomain.replace(/\.(com|org|net|edu|gov)$/i, '')
  const normalizedListing = listingDomain.replace(/\.(com|org|net|edu|gov)$/i, '')

  return normalizedUser === normalizedListing
}

/**
 * Generate a verification token for manual claims
 * @returns {string} - Random verification token
 */
export function generateVerificationToken() {
  return Math.random().toString(36).substring(2, 15) +
         Math.random().toString(36).substring(2, 15)
}

/**
 * Check if a verification token is still valid
 * @param {string} expiresAt - ISO date string
 * @returns {boolean} - True if token is still valid
 */
export function isTokenValid(expiresAt) {
  if (!expiresAt) return false
  return new Date(expiresAt) > new Date()
}

/**
 * Validate email domain format
 * @param {string} email - Email to validate
 * @returns {boolean} - True if email has valid domain format
 */
export function isValidEmailDomain(email) {
  if (!email || !email.includes('@')) return false

  const domain = extractEmailDomain(email)
  if (!domain) return false

  // Basic domain validation (has at least one dot, no spaces)
  return domain.includes('.') && !domain.includes(' ') && domain.length > 3
}

/**
 * Get claim status display information
 * @param {string} status - The claim status
 * @returns {object} - Display information with color and text
 */
export function getClaimStatusInfo(status) {
  switch (status) {
    case 'verified':
      return {
        text: 'Verified Owner',
        color: 'green',
        icon: '✓'
      }
    case 'pending':
      return {
        text: 'Claim Pending',
        color: 'yellow',
        icon: '⏳'
      }
    case 'rejected':
      return {
        text: 'Claim Rejected',
        color: 'red',
        icon: '✗'
      }
    default:
      return {
        text: 'Not Claimed',
        color: 'gray',
        icon: '?'
      }
  }
}

/**
 * Format verification method for display
 * @param {string} method - The verification method
 * @returns {string} - Human-readable method description
 */
export function formatVerificationMethod(method) {
  switch (method) {
    case 'domain_match':
      return 'Automatic (Domain Match)'
    case 'email_verification':
      return 'Email Verification'
    case 'admin_approval':
      return 'Admin Approval'
    default:
      return 'Unknown'
  }
}