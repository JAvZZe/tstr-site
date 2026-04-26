/**
 * Monetization Library — TSTR.directory
 * Centralized logic for feature gating based on subscription tiers and listing data.
 */

export type MapTier = 'none' | 'static' | 'premium' | 'enterprise';

/**
 * Checks if a listing has access to interactive map features.
 * Matches logic in ListingMap.astro and database constraints.
 */
export function hasInteractiveMapAccess(tier: string | null | undefined): boolean {
  if (!tier) return false;
  
  // Normalize tier strings from various migrations/conventions
  const normalized = tier.toLowerCase();
  
  return normalized === 'premium' || normalized === 'enterprise';
}

/**
 * Returns the effective map tier, ensuring we fallback gracefully.
 */
export function getEffectiveMapTier(tier: string | null | undefined): MapTier {
  if (!tier) return 'static';
  
  const normalized = tier.toLowerCase();
  if (normalized === 'premium' || normalized === 'enterprise') return 'premium';
  if (normalized === 'none') return 'none';
  
  return 'static';
}
