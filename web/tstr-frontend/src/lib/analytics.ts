/**
 * Consent-aware, env-gated third-party analytics loader.
 *
 * - Reads PUBLIC_ANALYTICS_ID from the build env (set in Cloudflare Pages / .env).
 * - Only loads AFTER the visitor has accepted analytics in the cookie banner
 *   (flag stored in localStorage as "tstr-consent": "all" | "necessary").
 * - Respects the browser "Do Not Track" signal.
 * - Does NOT load anything if PUBLIC_ANALYTICS_ID is empty (privacy-first default).
 *
 * This complements the existing internal click-analytics (api/out.ts) which tracks
 * listing engagement server-side and is not gated by consent (no personal data).
 */

const CONSENT_KEY = 'tstr-consent';

/** True when the visitor has explicitly accepted analytics cookies. */
export function hasAnalyticsConsent(): boolean {
  try {
    return localStorage.getItem(CONSENT_KEY) === 'all';
  } catch {
    return false;
  }
}

/** True when the visitor's browser requests do-not-track. */
function doNotTrackEnabled(): boolean {
  const nav = navigator as unknown as { doNotTrack?: string; msDoNotTrack?: string };
  const win = window as unknown as { doNotTrack?: string };
  try {
    return nav.doNotTrack === '1' || win.doNotTrack === '1' || nav.msDoNotTrack === '1';
  } catch {
    return false;
  }
}

/**
 * Load the configured privacy-respecting analytics script (e.g. Plausible/Umami/Fathom).
 * Safe to call repeatedly — only injects once, and only when consent + env + DNT allow.
 * Returns the analytics ID that was loaded, or null if nothing loaded.
 */
export function loadAnalytics(): string | null {
  const id = import.meta.env.PUBLIC_ANALYTICS_ID as string | undefined;
  if (!id) return null; // disabled
  if (doNotTrackEnabled()) return null; // respect DNT
  if (!hasAnalyticsConsent()) return null; // wait for consent
  if (document.getElementById('tstr-analytics-script')) return id; // already loaded

  const s = document.createElement('script');
  s.id = 'tstr-analytics-script';
  s.async = true;
  s.defer = true;
  // Plausible-style endpoint; swap the host/path if you use Umami/Fathom.
  s.src = `https://plausible.io/js/script.js`;
  s.setAttribute('data-domain', id);
  s.setAttribute('data-api', `/api/event`); // optional self-hosted proxy
  document.head.appendChild(s);
  return id;
}

/**
 * Called by the cookie banner when the visitor accepts. Loads analytics immediately
 * if an ID is configured, then re-checks on every Astro view transition.
 */
export function enableAnalyticsOnConsent(): void {
  loadAnalytics();
  document.addEventListener('astro:after-swap', () => loadAnalytics());
}
