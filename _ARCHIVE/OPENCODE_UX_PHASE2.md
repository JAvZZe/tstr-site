# OPENCODE_UX_PHASE2.md

**Objective**: Execute Phase 2 UI/UX High-Impact Improvements.

## 1. Gradient Refinement (Green to Royal Blue)
**Issue**: The current "Soft Blue" (#667eea) is perceived as purple.
**Action**: Update the brand gradient to be explicitly "Green to Royal Blue".

*   **Target Gradient**: `linear-gradient(135deg, #059669 0%, #2563EB 100%)`
    *   Start: `#059669` (Brand Green)
    *   End: `#2563EB` (Royal Blue / Tailwind blue-600)
*   **Scope**: Find/Replace all instances of the old gradient `linear-gradient(135deg, #667eea 0%, #059669 100%)` (and its reverse).
*   **Files**: `Header.astro`, `Footer.astro`, `account.astro`, `login.astro`, `signup.astro`, `submit.astro`, etc.

## 2. Responsive Header & Hamburger Menu (Critical UX)
**Issue**: "Pricing", "Browse", "Account" buttons overlap the logo on mobile.
**Action**: Implement a responsive navigation with a Hamburger Menu for mobile.

### Instructions for `src/components/Header.astro`:

1.  **Containerize Navigation**:
    *   Remove `position: absolute` from the nav buttons.
    *   Wrap the Logo and the Nav Buttons in a parent flex container:
        ```css
        .header-content {
          display: flex;
          justify-content: space-between;
          align-items: center;
          max-width: 1200px;
          margin: 0 auto;
        }
        ```

2.  **Desktop View (> 768px)**:
    *   Show the Logo on the left.
    *   Show the Nav Links (Pricing, Browse, Account) on the right as a row.

3.  **Mobile View (< 768px)**:
    *   **Hide** the desktop nav links.
    *   **Show** a "Hamburger" icon (SVG) on the right.
    *   Implement a slide-out or dropdown menu triggered by the Hamburger.
    *   **Menu Content**:
        *   "My Account" / "Login" (Prominent Button)
        *   "Browse Listings"
        *   "Pricing"

4.  **Implementation Tips**:
    *   Use `<script>` tag within `Header.astro` to handle the toggle state.
    *   Ensure the expanded menu has a high `z-index` and a solid background (use the white or the new Green/Blue gradient).

## 3. Account Button Placement
**Requirement**: "Account" or "Register/Login" should be universally accessible.
**Action**: Ensure the Hamburger Menu (on mobile) and Top-Right Nav (on desktop) **ALWAYS** includes this dynamic auth button, consistent with the logic added in Phase 1.
