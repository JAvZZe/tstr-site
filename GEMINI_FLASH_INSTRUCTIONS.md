# GEMINI FLASH INSTRUCTIONS: Subscription Page UI Polish

**Objective**: Finalize the UX/UI alignment between the Subscription page and the Account Dashboard.

**Target File**: `web/tstr-frontend/src/pages/account/subscription.astro`

## Context
The subscription page has been structurally updated, but lacks the specific "delight" elements (emojis, consistent headers) found on the main account dashboard.

## Task 1: Update Section Headers with Emojis
Locate the `loadSubscriptionPage` function's template literal (around line 600+) and update the section headers to include consistent emojis.

1.  **Current Plan Section**: Ensure the header is `<h3>💎 Your Current Plan</h3>`.
2.  **Upgrade Section**: Change `<h2>Upgrade Your Plan</h2>` to `<h2>🚀 Upgrade Your Plan</h2>`.
3.  **Help Section**: Change `<h2>Need Help?</h2>` to `<h2>🤝 Need Help?</h2>`.

## Task 2: Verify Button & Card Styles
Ensure the `style` block contains the following specific classes to match the dashboard (if not already present):

```css
/* Dashboard-style Grid */
.dashboard-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  margin-bottom: 2rem;
}

/* Card Styling */
.card {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
  position: relative;
  display: flex;
  flex-direction: column;
}

/* Header with Gradient Bar */
.card h3::before {
  content: '';
  width: 4px;
  height: 20px;
  background: linear-gradient(135deg, #000080 0%, #32CD32 100%);
  border-radius: 2px;
}
```

## Task 3: Execution Steps

1.  **Pull Latest**: `git pull origin main --rebase` (Resolve any stashed/local conflicts if needed).
2.  **Apply Edits**: Use `replace_file_content` to inject the emojis and styles.
3.  **Verify**: Ensure the page builds locally (`npm run build` or `astro check`).
4.  **Push**: `git commit -m "UI: Polish subscription page with consistent emojis and spacing" && git push origin main`.
