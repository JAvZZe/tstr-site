# OPENCODE_UX_UI_TASKS.md

**Objective**: Execute high-impact (Pareto) UX/UI improvements to professionalize the TSTR.directory experience.

## 1. Standardize Brand Gradient (Pareto Fix)
**Issue**: The site uses inconsistent gradients. Some pages use "purple/blue" while the homepage uses "blue/green".
**Action**: Standardize ALL backgrounds and primary accents to the "Homepage Gradient".

*   **Target Gradient**: `linear-gradient(135deg, #667eea 0%, #059669 100%)` (Blue -> Green)
*   **Remove**: Any instances of "purple" gradients (e.g., `#764ba2`, `#7b1fa2`).

**Specific Files to Check & Update**:
1.  **`src/layouts/Layout.astro` & `src/layouts/BaseLayout.astro`**: Ensure the body or header background uses the target gradient.
2.  **`src/pages/account.astro`**:
    *   Update `.card h3::before` (vertical accent bar) to use the Blue/Green gradient.
    *   Update `.btn-primary` background.
    *   Update `.tier-badge` gradients to harmonize (or remove conflicting purples).
    *   Update `.benefits-list li:before` (checkmark color).
3.  **`src/pages/index.astro`**: Confirm it matches the standard.

## 2. Universal Auth Navigation (Pareto Fix)
**Issue**: Navigation is inconsistent. Users can't easily Register/Login from every page.
**Action**: Ensure a "Register / Login" or "Account" button is visible in the Header on EVERY page.

**Implementation**:
Modify `src/components/Header.astro`:
*   **Current State**: Has "Pricing" and "Get Started Free" hardcoded absolute positioned buttons.
*   **Required Change**:
    *   Replace hardcoded buttons with a valid `<nav>` flex container.
    *   **Logic**:
        *   If user is NOT logged in: Show "Pricing", "Browse", "Login / Register".
        *   If user IS logged in: Show "Pricing", "Browse", "My Account".
    *   **Styling**: Use the "Green/Blue" gradient for the primary CTA button (e.g., "Get Started" or "My Account") and a clean white/outline for secondary links.

## 3. Account Dashboard UI Layout (Critical Fix)
*   **Reference**: Execute the implementation steps in `QWEN3_UI_FIX.md` first. This restores the broken grid/flex layouts.

## 4. Visual Polish (Quick Wins)
*   **Buttons**: Ensure all buttons have explicit `cursor: pointer` and a subtle `hover` elevation (transform: translateY(-1px)).
*   **Typography**: Ensure `font-family` is consistent (prefer system fonts or Inter if available).
*   **Spacing**: Add consistent `padding-bottom` (e.g., `4rem`) to all pages so content doesn't touch the very bottom of the viewport.

## Execution Order
1.  **`QWEN3_UI_FIX.md`** (Fix broken layout first).
2.  **Gradient Standardization** (Immediate visual impact).
3.  **Header/Auth Navigation** (Critical functionality).
4.  **Visual Polish** (Refinement).
