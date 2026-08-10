# Analytics Setup Guide (non-tech)

> **What this is for:** "Fix 2 — Add analytics" is already built into the website.
> You just need to **turn on a free analytics provider** so the site starts counting
> visitors. This guide tells you exactly which free provider to use and how to switch
> it on. No code, no server, no paid plan.

---

## 1. Which free provider should you use?

**Recommendation: Cloudflare Web Analytics.**

Why it's the right pick for TSTR.directory:

| Reason | Detail |
|--------|--------|
| **Free forever** | No trial, no traffic limit, no credit card. |
| **Already in your account** | Your site (`tstr.directory`) is hosted on Cloudflare Pages. Web Analytics is a built-in Cloudflare feature — no new signup. |
| **Privacy-first (cookieless)** | It does NOT use cookies and does NOT collect personal data. Under GDPR this means you generally do **not** need a consent banner for it (your existing banner already covers the Apollo tracker). |
| **2-minute setup** | One toggle in the dashboard. |
| **Works with your deploy** | Cloudflare auto-injects the tracking script — nothing to change in the code. |

**Alternatives (only if you later want more detail or self-hosting):**
- **Umami** — open-source, free if you self-host on your free Oracle (OCI) box. More setup (SSH + Docker). Use only if you want the data on your own server.
- **Plausible** — excellent, but the *hosted* version costs money (only a 30-day trial is free). Self-hosting it is free but needs a server.

For now: **use Cloudflare Web Analytics.** It costs $0 and is already yours.

---

## 2. Turn it on (exact steps)

1. Open **https://dash.cloudflare.com** and log in (the Tstr.site / tstr account).
2. On the left menu, click **Analytics & Logs**.
3. Click **Web Analytics**.
4. Click **+ Add a site** (or "Create a Web Analytics site").
5. Enter your domain: `tstr.directory`
6. Click **Add site / Start**.
7. Cloudflare will say the site is already proxied (orange-clouded) — that's expected.
   It will confirm **"Your site is being tracked"** within a minute or two.
8. Done. No script tag to copy, no code to deploy.

> **Why no code change?** Because `tstr.directory` already runs through Cloudflare,
> Cloudflare automatically attaches its analytics beacon to every page. The website
> code we already shipped (the cookie banner + consent logic) stays in place and
> continues to gate the Apollo tracker.

---

## 3. Check it's working (verify, don't assume)

1. In the Cloudflare dashboard, go to **Analytics & Logs → Web Analytics → tstr.directory**.
2. Wait ~24 hours (or generate a visit: open `https://tstr.directory` in a private/incognito window and click around).
3. You should see:
   - **Page views** and **visits** climbing.
   - **Top pages** (e.g. `/`, `/browse`, a standards page).
   - **Countries** and **referrers** (Google, direct, etc.).

If the numbers stay at 0 after 24h, re-check step 2 (the domain must be the one
Cloudflare proxies, and the orange cloud must be on for `tstr.directory` in **DNS**).

---

## 4. What you get vs. what you already had

- **Before:** only *internal click analytics* (how many times a listing's contact/link
  was clicked) — visible in your admin dashboard at `/admin/analytics` and `/account/analytics`.
- **Now (after enabling):** *site traffic analytics* — total visitors, page views,
  top pages, countries, referrers, devices. This answers "is anyone coming to the site
  and from where?" which the click analytics could not.

You do **not** need to set `PUBLIC_ANALYTICS_ID` for Cloudflare Web Analytics — that
env var is only for a Plausible/Umami/Fathom style provider (see section 5).

---

## 5. (Optional) Use a different provider instead

If you ever prefer Umami/Plausible/Fathom:

1. Sign up / self-host and get your **data-domain** (e.g. `tstr.directory` for Umami,
   or your Plausible subdomain).
2. In **Cloudflare Pages → tstr-hub → Settings → Environment variables**, add:
   - **Production:** `PUBLIC_ANALYTICS_ID` = your data-domain
   - **Preview:** `PUBLIC_ANALYTICS_ID` = your data-domain
3. Redeploy (push to `main`, or "Retry" the last deploy in Cloudflare Pages).
4. The site's consent-gated loader will then pull that provider's script **after** the
   visitor accepts the cookie banner.

> Note: with these providers the script only loads after consent (GDPR-safe), unlike
> Cloudflare Web Analytics which is cookieless and runs automatically.

---

## 6. Privacy / legal note

- Cloudflare Web Analytics is **cookieless and aggregates data** — it is widely treated
  as GDPR-compliant without a consent prompt. Your existing cookie banner still covers
  the Apollo.io tracker, so you're covered either way.
- Keep the banner. If you later add a cookie-based provider (section 5), the banner
  already gates it correctly.

---

## 7. Project to-do reference

- `PROJECT_STATUS.md` → Low Priority → **Fix 2 — wire a free analytics provider**.
- Code already live: consent banner + consent-gated loader (`src/components/CookieConsent.astro`,
  `src/lib/analytics.ts`, `src/layouts/BaseLayout.astro`).
- After you complete section 2–3, mark Fix 2 done in `PROJECT_STATUS.md`.
