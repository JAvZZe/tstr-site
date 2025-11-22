/**
 * Generate internal redirect URL for outbound clicks
 *
 * Purpose:
 * - Preserves domain authority by keeping links internal until redirect
 * - Enables click analytics tracking
 * - Provides consistent URL generation across all listing pages
 *
 * @param website - The external URL to redirect to (e.g., "https://example.com")
 * @param listingId - Optional listing UUID for validation and analytics
 * @returns Internal redirect URL (e.g., "/api/out?url=https://example.com&listing=<uuid>")
 *
 * @example
 * ```astro
 * import { getRedirectUrl } from '../../lib/redirect';
 *
 * <a
 *   href={getRedirectUrl(listing.website, listing.id)}
 *   target="_blank"
 *   rel="nofollow noopener noreferrer"
 * >
 *   Visit Website
 * </a>
 * ```
 */
export function getRedirectUrl(website: string, listingId?: string): string {
  const params = new URLSearchParams();
  params.set('url', website);
  if (listingId) {
    params.set('listing', listingId);
  }
  return `/api/out?${params.toString()}`;
}
