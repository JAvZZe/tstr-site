# 📜 VERSION HISTORY - TSTR.directory

> **Full changelog archive** - See `PROJECT_STATUS.md` for executive summary

---

## v2.9.17 - 2026-04-16 - PSEO 2.0 Conversion Optimization Overhaul (Antigravity)

- **UI/UX Landing Overhaul**: Implemented "Obsidian" premium dark mode for PSEO industry pages with Indigo/Emerald accents
- **Conversion Flow**: Added mobile/desktop Sticky CTA bars to landing pages and Listing pages
- **Dynamic FAQ Schema**: Implemented logic to automatically generate structured FAQ schema from database standard metadata
- **Deep-Linking RFQ**: Refactored individual listing pages and `ContactLabModal` to support `#rfq` hash-triggered auto-opening and form pre-filling with standard context
- **Navigation**: Enhanced listing pages with glassmorphic cards and high-velocity conversion paths

## v2.9.16 - 2026-04-15 - Search API Two-Phase Shift & Repo Cleanup (antigravity)

- **Search API**: Fully transitioned `by-standard.ts` to a two-phase retrieval pattern (Identification -> Hydration)
- **Cleanup**: Resolved repository "detachment" by pruning redundant worktrees
- **Verification**: Verified zero regressions in Search API behavior via Playwright

## v2.9.15 - 2026-04-15 - Search API Location Filter Verification (antigravity)

- **Verification**: Executed Playwright tests to confirm the JS-side filtering fix for the Search API

## v2.9.14 - 2026-04-15 - Search API Bug Fix (antigravity)

- **Bug Fix**: Resolved critical Search API location filter `.or()` clause conflict in `by-standard.ts`

## v2.9.13 - 2026-04-09 - Niche Specialization: Calibration & Hydraulic Testing (gemini-2.5-pro)

- **Database**: Created specialized categories `Calibration & Metrology Services` and `Hydraulic & Pneumatic Testing`
- **Standards**: Added 5 specialized standards (ISO 9001, ANSI/ASHRAE 199, ISO 15001, NIST Traceable, etc.)
- **Listings**: Added Trescal, Transcat, Parker Hannifin, and Swagelok

## v2.9.12 - 2026-04-09 - Niche Specialization: Battery Fire Safety & EMC/Wireless (gemini-2.5-pro)

- **Database**: Created specialized categories `Battery Fire & Thermal Abuse Testing` and `Product Safety, EMC & Wireless`
- **Standards**: Added 6 core standards (UL 1973, IEEE 1547, FCC Part 15, CISPR 32, etc.)
- **Listings**: Added DNV BEST Test Center, CSA Group, Eurofins MET Labs, TÜV SÜD America

## v2.9.11 - 2026-04-09 - Niche Specialization: Subsea Integrity & Acoustics (gemini-2.5-pro)

- **Database**: Created specialized categories `Subsea Pipeline & Asset Integrity` and `Acoustics, Vibration & Seismic Testing`
- **Standards**: Added 5 core standards (ISO 3744, IEC 60980, DNV-RP-F116, IMCA D 006, etc.)
- **Listings**: Added DeepOcean, i-Tech 7, HBK, and Sopemea

## v2.9.10 - 2026-04-09 - Sector Specialization: Defense & Ballistics Testing (gemini-2.5-pro)

- **Database**: Created specialized category `Defense & Ballistics Testing`
- **Standards**: Added 6 core defense standards (MIL-STD-810H, MIL-DTL-901E, NIJ 0101.06, STANAG 4569, etc.)
- **Listings**: Added Element U.S. Space & Defense, QinetiQ, Dayton T. Brown, Oregon Ballistic Laboratories

## v2.9.9 - 2026-04-09 - Sector Specialization: Forensics & Semiconductors (gemini-2.5-pro)

- **Database**: Created specialized categories `Forensic Engineering & Failure Analysis` and `Advanced Semiconductor & Materials Characterization`
- **Standards**: Added 5 specialized standards (ASTM E2332, NFPA 921, SEMI E54, ISO 18115, JEDEC JESD22)
- **Listings**: Added Exponent and Jensen Hughes

## v2.9.8 - 2026-04-08 - Sector Specialization: Building Science & Mining (gemini-2.5-pro)

- **Database**: Created specialized categories `Building & Construction Testing` and `Mining & Geochemistry Testing`
- **Standards**: Added 7 core standards (NFPA 285, ASTM E331/E1105, NI 43-101, JORC Code, etc.)
- **Listings**: Added ALS Minerals and Element Building Science

## v2.9.7 - 2026-04-08 - Sector Specialization: Nuclear & Consumer Goods Testing (gemini-2.5-pro)

- **Database**: Created specialized categories `Nuclear Energy Testing & Inspection` and `Consumer Goods & Textile Testing`
- **Standards**: Added 8 core standards (ASME Section III, RSE-M, AATCC TM61, ASTM F963, etc.)
- **Listings**: Added Westinghouse, Framatome, Orano, and QIMA

## v2.9.6 - 2026-04-08 - Niche Specialization: Carbon MRV & 5G Validation (gemini-2.5-pro)

- **Database**: Created specialized categories `Carbon Sequestration & MRV` and `Telecommunications & 5G Testing`
- **Standards**: Added 6 core standards (ISO 14064-1, Verra VM0042, DNV-RP-A203, 3GPP Rel-17, etc.)
- **Listings**: Added Yard Stick PBC, Aker Carbon Capture, Keysight, Rohde & Schwarz, Spirent

## v2.9.5 - 2026-04-08 - Sector Specialization: Cybersecurity & Food Safety (gemini-2.5-pro)

- **Database**: Created specialized categories `Cybersecurity & Software Testing` and `Food Safety & Agricultural Testing`
- **Standards**: Added 8 core standards (ISO 27001, SOC 2, FSSC 22000, HACCP, etc.)
- **Listings**: Added NCC Group, Mérieux NutriSciences, and ALS Global

## v2.9.4 - 2026-04-08 - Sector Specialization: Railway & Medical Device Testing (gemini-2.5-pro)

- **Database**: Created specialized categories `Railway & Rolling Stock Testing` and `Medical Device & Healthcare Testing`
- **Standards**: Added 6 core standards (EN 50126/45545, ISO 22163, IEC 60601, ISO 11135/11137)
- **Listings**: Added TÜV SÜD Rail, Ricardo Rail, Nelson Labs, Charles River, NAMSA

## v2.9.3 - 2026-04-08 - Niche Specialization: Subsea & EV Battery Safety (gemini-2.5-pro)

- **Database**: Created specialized categories `Subsea & Offshore Testing` and `EV & Battery Safety Testing`
- **Standards**: Added 5 core niche standards (DNV-ST-F101, API 17D, UN 38.3, ECE R100, SAE J2464)
- **Listings**: Added Oceaneering, FEV, UTAC Millbrook, Ricardo

## v2.9.2 - 2026-04-08 - Renewable Energy Expansion: Wind, Solar & BESS (gemini-2.5-pro)

- **Database**: Created new category `Renewable Energy Testing & Certification` (Slug: `renewable-energy-testing`)
- **Standards**: Added 5 core renewable standards (IEC 61400 series, IEC 61215, UL 9540A, VDE-AR-N 4105)
- **Listings**: Added TÜV Rheinland, Fraunhofer ISE, Fraunhofer IWES, VDE Renewables

## v2.9.1 - 2026-04-08 - Heading Refinement & Aerospace Integration (gemini-2.5-pro)

- **UI/UX**: Refined business headings by separating service descriptors into "Service Tags" (badges)
- **Architecture**: Repurposed `listing_capabilities` to act as high-visibility tags
- **Aerospace**: Added specialized NDT listings for Magnaflux, Waygate Technologies, Eddyfi Technologies

## v2.9.0 - 2026-04-08 - Asset Integrity Expansion: DNV, DEKRA & LRQA (gemini-2.5-pro)

- **Listings**: Expanded DNV and DEKRA, and added LRQA with high-fidelity profiles
- **Standards**: Added pipeline and maritime standards (API RP 1173, ISO 10426)

## v2.8.9 - 2026-04-08 - Asset Integrity Expansion: Intertek, BV & TÜV SÜD (gemini-2.5-pro)

- **Listings**: Expanded Intertek, Bureau Veritas, and TÜV SÜD with high-fidelity profiles
- **Standards**: Added core compliance and safety standards (API 579, ASME Section XI, ISO 45001)

## v2.8.8 - 2026-04-08 - Asset Integrity Expansion: Applus+ & SGS (gemini-2.5-pro)

- **Listings**: Expanded Applus+ and SGS with high-fidelity profiles highlighting proprietary software
- **Standards**: Added 4 new Asset Management and RBI standards (API 580/581, ISO 19011, ISO 55001)

## v2.8.7 - 2026-04-08 - NDT Context & Mistras Group Integration (gemini-2.5-pro)

- **Database**: Created new category `Non-Destructive Testing (NDT) & Asset Integrity`
- **Standards**: Added 10 core NDT and API standards
- **Listing**: Added MISTRAS Group, Inc. (NYSE: MG) as a Gold Standard listing
- **Template**: Established NDT/Asset Integrity profile template

## v2.8.6 - 2026-03-27 - Mass RLS Policy Hardening (claude-sonnet-thinking)

- **Security**: Fixed 9x "RLS Policy Always True" warnings across 7 tables
- **Critical Fix**: Restricted `payment_history` INSERT from public to service_role only

## v2.8.5 - 2026-03-27 - Search Path Security Hardening (gemini-3-flash)

- **Security**: Hardened `public.calculate_trust_score` function by pinning `search_path=''`

## v2.8.4 - 2026-03-27 - RLS Security Hardening (gemini-3-flash)

- **Security**: Enabled Row Level Security on `public.schema_migrations`

## v2.8.3 - 2026-03-19 - Hydrogen Standards Expansion (opencode)

- **Added**: 15 new hydrogen testing standards from Google Sheets analysis
- **Database**: Standards expanded from 40 to 55

## v2.8.0 - 2026-03-08 - Hydrogen Taxonomy & Certification Filters (antigravity)

- **Database**: Implemented "Amazon-style" browse nodes for Hydrogen category
- **SEO**: Transitioned certification filters to use SEO-friendly slugs in URL

## v2.6.2 - 2026-02-23 - PayPal Live Mode Confirmed & Docs Fixed (antigravity)

- **Status Fix**: Corrected stale TODO for PayPal live switch
- **Docs**: Updated Payment System section to reflect `PAYPAL_MODE=live`

## v2.6.1 - 2026-02-22 - Alternate Gemini API Key Integration (antigravity)

- **AI Integration**: Added second Gemini API key as failover for rate limits

## v2.6.0 - 2026-02-12 - Security Redaction & Repository Cleanup (antigravity)

- **Security**: Redacted exposed API keys across docs
- **Organization**: Moved ~60 historical docs to `_ARCHIVE/`

## v2.5.5 - 2026-01-28 - Apollo Tracking Site-Wide (antigravity)

- **Feature**: Implemented Apollo.io visitor tracking site-wide

## v2.5.4 - 2026-01-28 - Domain Reference Migration (antigravity)

- **Cleanup**: Updated all references of `tstr.site` to `tstr.directory`

## v2.5.3 - 2026-01-22 - Infrastructure & Contact Fix Finalization (gemini)

- **Infrastructure**: User added subdomains for email sending at Cloudflare

## v2.5.2 - 2026-01-16 - Manual Payment Flows & Debugging (gemini)

- **Feature**: Implemented Bank Transfer (EFT) and Bitcoin manual payment flows

## v2.5.1 - 2026-01-16 - Robust Subscription Cancellation Fix (gemini)

- **Bug Fix**: Resolved issue where subscription tier failed to reset to 'free' after cancellation

## v2.5.0 - 2026-01-15 - PayPal Integration Live Readiness (opencode)

- **Deployment**: Finalized PayPal production configuration

## v2.4.26 - 2026-01-13 - Server-Side Subscription State Management (opencode)

- **Root Cause**: Chrome bounce tracking deletes client-side state
- **Solution**: Implemented server-side storage for pending subscriptions

## v2.4.25 - 2026-01-11 - PayPal Integration Success (gemini)

- **JWT Resolution**: Switched from Publishable Key to valid Anon JWT via Supabase CLI

## v2.4.24 - 2026-01-11 - PayPal Fixes (gemini)

- **Jwt Fix**: Updated `pricing.astro` to use Supabase Anon Key for Edge Function calls

## v2.4.23-v2.4.14 - PayPal JWT Validation & Debugging (opencode/gemini)

- Multiple iterations on PayPal JWT validation and Edge Function authentication

## v2.4.13 - 2026-01-09 - SEO Enhancement (opencode)

- **Feature**: Added comprehensive sitemap page and footer link

## v2.4.12 - 2026-01-07 - Infrastructure Bootstrap Refactor (Gemini Pro)

- System-wide bootstrap refactor and tool access fixes

## v2.4.11 - 2026-01-07 - Cleanup: Standardized Agent Files (Gemini Pro)

- Fixed incorrect paths in all agent docs
- Enforced status protocol

## v2.4.10 - 2026-01-06 - Favicon Updated (opencode)

- Created favicon from site logo for consistent branding

## v2.4.9 - 2026-01-06 - PayPal Subscription Flow Fixed (opencode)

- Resolved OAuth redirect losing tier parameter

## v2.4.8 - 2026-01-05 - Claim Form Email Testing Complete

- End-to-end email functionality verified

## v2.4.7 - 2026-01-03 - Claim Form Email Functionality Complete

- Implemented complete Resend email system for claim forms

## v2.4.6 - 2026-01-02 - UX Phase 2 Complete

- Implemented advanced responsive design and refined brand identity

## v2.4.4 - 2026-01-02 - Account Dashboard UI Fix

- Resolved broken layout from Astro's scoped CSS

## v2.4.3 - 2026-01-01 - Domain References Fixed

- Updated OAuth and API test scripts to use correct domain

## v2.4.2 - 2026-01-01 - Sales Email Updated & JSON-LD Fix

- Changed sales contact to sales@tstr.directory
- Resolved JSON-LD parsing error

## v2.4.1 - 2026-01-01 - JSON-LD Structured Data Added

- Implemented proper JSON-LD markup on authentication pages

## v2.4.0 - 2025-12-29 - PayPal Integration Complete

- Full subscription system implemented with Professional ($295/mo) and Premium ($795/mo) tiers

## v2.3.20 - 2025-12-27 - Homepage Logo Updated

- Replaced old SVG with new narrower SVG logo

## v2.3.19 - 2025-12-27 - Homepage Logo Updated

- Replaced PNG logo with inlined SVG logo

## v2.3.18 - 2025-12-27 - Homepage Logo Updated

- Created Header component with larger T-logo

## v2.3.17 - 2025-12-27 - Homepage Logo Updated

- Replaced favicon logo with updated SVG

## v2.3.16 - 2025-12-23 - OCI SSH Access Fully Verified

- Resolved key permission issues preventing access

## v2.3.15 - 2025-12-22 - Phase 1 & Phase 2 Complete

- Core Listing Management: `/account/listing/[id]/edit`
- Lead Management System: Analytics, leads, bulk management

## v2.3.13 - 2025-12-21 - Admin Dashboard Enhanced

- Added comprehensive user and claims management

## v2.3.8 - 2025-12-16 - Security Hardening Deployed

- All 12 functions now have secure search_path

## v2.3.7 - 2025-12-16 - Critical Security Fix

- Removed SUPABASE_SERVICE_ROLE_KEY from frontend .env

## v2.3.6 - 2025-12-04 - Claim Button Visibility Project Plan

- Comprehensive plan for making claim buttons visible to all users

## v2.3.5 - 2025-12-03 - System Health Verification Complete

- 93/100 health score, 191 verified listings

_(See `docs/REFERENCE_STATUS.md` for versions before v2.3.5)_
