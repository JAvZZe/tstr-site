# TSTR 2.0: Concept & Implementation Plan

**Goal**: Rebuild TSTR.site from scratch as a premium, AI-native directory for testing services.
**Philosophy**: "Premium Aesthetic, AI-Driven, Serverless Scale."

## Tech Stack (The "Gemini Choice")

We will use a stack optimized for developer velocity, free-tier longevity, and Google ecosystem integration.

*   **Frontend**: **React (Vite)** + **TypeScript**.
    *   *Why*: Lightweight, compiles to static assets (perfect for Firebase Hosting), huge ecosystem.
*   **Styling**: **Tailwind CSS** + **Framer Motion**.
    *   *Why*: Mandatory for that "wow" active UI factor. Animations are key to feeling "premium."
*   **Backend / DB**: **Firebase**.
    *   *Auth*: Google/Email login.
    *   *Firestore*: NoSQL database for lightning-fast reads.
    *   *Hosting*: CDN-backed static hosting.
*   **AI Engine**: **Gemini 1.5 Flash**.
    *   *Role*: Summarizing lab capabilities, converting messy scraper data into structured JSON, and powering a "natural language search" (e.g., "Find me a lab in Texas that does cryogenic hydrogen testing").
*   **Data Pipeline (The "Free" Scraper)**:
    *   Use **GitHub Actions** (2000 free minutes/month) to run Python scrapers.
    *   Scrapers push data directly to Firestore.

## Core "Improvements" over Original

1.  **AI-First Experience**: Instead of just checkboxes, users can ask: *"I need to test a valve for hydrogen embrittlement."* Gemini parses this and filters tags.
2.  **Premium UI**: Dark mode by default (or user toggle), glassmorphism, skeletons while loading, smooth transitions.
3.  **Speed**: Firestore is generally faster for simple document reads than relational joins on a small free-tier SQL DB.

## Estimated Timeline

| Phase | Duration | Output |
| :--- | :--- | :--- |
| **1. Design & Setup** | 2 Days | Repo, Design System, Firebase Config |
| **2. Scraper 2.0** | 3 Days | New efficient scrapers (Python) w/ Gemini parsing |
| **3. Frontend Core** | 4 Days | Homepage, Search, Listing Cards (High Polish) |
| **4. AI Integration** | 3 Days | "Smart Match" feature, Summaries |
| **5. Polish & Launch** | 2 Days | SEO, Sitemap, Performance tuning |
| **Total** | **~2 Weeks** | **MVP Release** |

## Immediate Next Steps (If approved)
1.  Initialize standard React+Vite+Tailwind project.
2.  Set up Firebase Emulator for local development.
3.  Draft the new Firestore schema.
