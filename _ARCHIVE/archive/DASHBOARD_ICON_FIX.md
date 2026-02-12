# DASHBOARD_ICON_FIX.md

This sheet contains the **FINAL** copy-pastable fix for the oversized envelope and other icons on the Account page.

### 1. Fix Scoped Styling
In `src/pages/account.astro`, update the `.info-icon` style to use the `:global()` modifier. This ensures the style applies to HTML injected via `innerHTML`.

```css
/* Update around line 133 in account.astro */
.info-icon, :global(.info-icon) {
  width: 20px !important;
  height: 20px !important;
  color: #667eea;
  flex-shrink: 0;
}
```

### 2. Update Dynamic SVG Attributes
Ensure the SVGs inside the `contentDiv.innerHTML` block have explicit `width` and `height` attributes.

```javascript
/* Example for the Envelope Icon in account.astro */
<svg class="info-icon" width="20" height="20" fill="currentColor" viewBox="0 0 20 20">
  <path d="M2.003 5.884L10 9.882l7.997-3.998A2 2 0 0016 4H4a2 2 0 00-1.997 1.884z"/>
  <path d="M18 8.118l-8 4-8-4V14a2 2 0 002 2h12a2 2 0 002-2V8.118z"/>
</svg>
```

### Why this is necessary:
Astro's **Scoped CSS** appends a unique ID to every class (e.g., `.info-icon[data-astro-cid-xxxx]`). When content is injected via `innerHTML` at runtime, it **does not** have this unique ID, so the styles fail to apply. Using `:global()` and explicit attributes bypasses this limitation.
