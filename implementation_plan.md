# Implementation Plan - Fix Account Page Image Scaling

The goal is to fix the oversized "icon images" on the account page and standardize the site's logo using FFMPEG.

## User Review Required

> [!IMPORTANT]
> The current logos in `/public` have unusual dimensions (e.g., 530x713 portrait). I will be using FFMPEG to create standardized, resized versions (e.g., 90px height or 64x64 square) to ensure they display correctly across headers and dashboards.

## Proposed Changes

### [Component] Image Assets (Standardization)

#### [NEW] [TSTR-Logo-90px.png](file:///media/al/AI_DATA/AI_PROJECTS_SPACE/ACTIVE_PROJECTS/TSTR-site/tstr-site-working/web/tstr-frontend/public/TSTR-Logo-90px.png)
- Optimized logo with 90px height and correct aspect ratio.

#### [NEW] [TSTR-Logo-Square-64.png](file:///media/al/AI_DATA/AI_PROJECTS_SPACE/ACTIVE_PROJECTS/TSTR-site/tstr-site-working/web/tstr-frontend/public/TSTR-Logo-Square-64.png)
- Square icon for use in dashboards and favicons.

### [Component] Frontend Components

#### [MODIFY] [Header.astro](file:///media/al/AI_DATA/AI_PROJECTS_SPACE/ACTIVE_PROJECTS/TSTR-site/tstr-site-working/web/tstr-frontend/src/components/Header.astro)
- Replace complex inlined SVG with a standardized `<img>` tag pointing to the new optimized PNG.
- Constrain height to 60-80px for a sleeker look.

#### [MODIFY] [account.astro](file:///media/al/AI_DATA/AI_PROJECTS_SPACE/ACTIVE_PROJECTS/TSTR-site/tstr-site-working/web/tstr-frontend/src/pages/account.astro)
- Incorporate the site's standard Header/Logo if missing, or fix the scaling of any existing images.
- **CRITICAL FIX**: Add explicit `width="20" height="20"` to all SVGs within the `innerHTML` dashboard rendering block.
- **ROBUSTNESS FIX**: Added `:global(.info-icon)` to the `<style>` block in `account.astro` to ensure CSS applies to dynamically injected HTML that bypasses Astro's standard scoping.

## Verification Plan

### Automated Tests
- Run `ffprobe` to verify the final dimensions of the generated images.

### Manual Verification
- Check `https://tstr.directory/account` and `https://tstr.directory/` to ensure the logo is correctly scaled and looks "premium".
