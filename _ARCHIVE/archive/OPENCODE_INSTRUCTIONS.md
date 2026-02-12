# Instructions for Opencode: Update TSTR.site Homepage Logo

**Task**: Replace the current small logo with the new larger T-logo, resizing and aligning it to match the "TSTR hub" text block, and ensuring the container fits the new layout.

## 1. Asset Location
The new logo image has already been uploaded to the project:
`web/tstr-frontend/public/TSTR-Logo-New.png`

## 2. File to Modify
`web/tstr-frontend/src/components/Header.astro`

## 3. Required Changes

### A. Update the `img` tag
- Change `src` from `/TSTR Grey Logo.svg` to `/TSTR-Logo-New.png`.
- **Resize**: The user wants the logo to be the same size (height) as the "TSTR hub" text block.
  - The text block combines "TSTR" (2.5rem) and "hub" (3.2rem).
  - Total stack height is approx **90px** (or roughly 5.6rem).
  - Update `width` and `height` attributes (or styles) to:
    - `height="90"` (or `style="height: 90px; width: auto;"`)
    - Keep aspect ratio (so `width: auto`).

### B. Adjust the Container (`h1`)
- **Current Issue**: The `h1` currently has a fixed `width: 200px` and `height: 200px`.
  - A larger logo (approx 90px wide + text width) will likely overflow or look cramped in a fixed 200px box.
- **Action**:
  - Remove `width: 200px`.
  - Add `padding: 0 2rem` (or appropriate padding) to maintain the "badge" look without fixed width constraints.
  - Make sure `height` is sufficient (remove fixed `height: 200px` if needed, or change to `min-height: 200px` if the box shape is important).
  - Ideally, use `width: auto` or `display: inline-flex` (centered) with padding.

### C. Styling & Alignment
- Ensure the logo is **on the left** of the text block (current structure `[img] [text]` is correct).
- Adjust `margin-right` on the image if needed (currently `1rem`, maybe increase to `1.5rem` for better proportion).
- Ensure the flex alignment (`align-items: center`) keeps them vertically centered relative to each other.

## 4. Verification
1. Run `npm run dev` in `web/tstr-frontend`.
2. Visit the homepage.
3. Verify:
   - Logo is the new "T" image.
   - Logo height matches the "TSTR hub" text height.
   - The container box surrounds them comfortably without overflow.
   - The badge is centered on the page.

---
**Example Code Snippet (Guidance)**:

```html
<h1 style="... display: inline-flex; width: auto; padding: 2rem; min-width: 200px; ...">
    <div style="display: flex; align-items: center; justify-content: center;">
      <img src="/TSTR-Logo-New.png" alt="TSTR Logo" style="height: 90px; width: auto; margin-right: 1.5rem;"/>
      <div>
        <!-- text spans -->
      </div>
    </div>
</h1>
```
