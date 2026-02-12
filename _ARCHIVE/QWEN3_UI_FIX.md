# QWEN3_UI_FIX.md

**Objective**: Fix the broken layout on the Account Dashboard caused by Astro's Scoped CSS not applying to runtime-injected HTML.

## The Problem
Content injected via `innerHTML` (the entire dashboard content in `account.astro`) does not receive Astro's scoped data attributes (e.g., `data-astro-cid-xxxx`). However, the CSS styles defined in the `<style>` block ARE scoped. This results in the HTML elements not matching the CSS selectors, causing them to lose all layout styling (grids, flexbox, alignment).

## The Solution
Update the CSS selectors in `src/pages/account.astro` to target both the scoped AND global versions of the classes using `:global()`.

## Instructions for Qwen3-Coder CLI

Edit `web/tstr-frontend/src/pages/account.astro` and find the `<style>` block. Update the following selectors to include their `:global()` counterpart.

**Pattern to Apply:**
Change `SELECTOR { ... }` to `SELECTOR, :global(SELECTOR) { ... }`

### List of Selectors to Update

1.  **Grid & Layout**
    *   `.dashboard-grid` -> `.dashboard-grid, :global(.dashboard-grid)`
    *   `.card` -> `.card, :global(.card)`
    *   `.card h3` -> `.card h3, :global(.card h3)`
    *   `.card h3::before` -> `.card h3::before, :global(.card h3::before)`
    *   `.card-content` -> `.card-content, :global(.card-content)`
    *   `.full-width` -> `.full-width, :global(.full-width)`

2.  **Info Rows (Critical for Alignment)**
    *   `.info-row` -> `.info-row, :global(.info-row)`
    *   `.info-row:hover` -> `.info-row:hover, :global(.info-row:hover)`
    *   `.info-row:last-child` -> `.info-row:last-child, :global(.info-row:last-child)`
    *   `.info-content` -> `.info-content, :global(.info-content)` **(Fixes Icon Alignment)**
    *   `.info-text` -> `.info-text, :global(.info-text)`
    *   `.info-label` -> `.info-label, :global(.info-label)`
    *   `.info-value` -> `.info-value, :global(.info-value)`

3.  **Badges & Lists**
    *   `.tier-badge` -> `.tier-badge, :global(.tier-badge)`
    *   `.tier-badge:hover` -> `.tier-badge:hover, :global(.tier-badge:hover)`
    *   `.tier-badge.free` -> `.tier-badge.free, :global(.tier-badge.free)` (and all other tier variants: basic, professional, premium, enterprise)
    *   `.benefits-list` -> `.benefits-list, :global(.benefits-list)`
    *   `.benefits-list li` -> `.benefits-list li, :global(.benefits-list li)`
    *   `.benefits-list li:before` -> `.benefits-list li:before, :global(.benefits-list li:before)`

4.  **Buttons & Interactive**
    *   `.button-group` -> `.button-group, :global(.button-group)`
    *   `.btn` -> `.btn, :global(.btn)`
    *   `.btn-primary`, `.btn-secondary`, `.btn-danger` (and their hover states)

5.  **Listings**
    *   `.listings-grid` -> `.listings-grid, :global(.listings-grid)`
    *   `.listing-item` -> `.listing-item, :global(.listing-item)`
    *   `.listing-header` -> `.listing-header, :global(.listing-header)`
    *   `.status-badge` -> `.status-badge, :global(.status-badge)` (and variants: verified, pending, rejected)

### Example

**Before:**
```css
.info-row {
  display: flex;
  justify-content: space-between;
  /* ... */
}
```

**After:**
```css
.info-row, :global(.info-row) {
  display: flex;
  justify-content: space-between;
  /* ... */
}
```

**Note:** The `.info-icon` class has already been fixed. Do not modify it unless strictly necessary.
