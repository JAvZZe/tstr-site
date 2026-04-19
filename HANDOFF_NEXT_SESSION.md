# 🤝 Handoff: AdSense Optimization & Automation Cleanup

## 📋 Status Overview
- **AdSense**: Production tag verified on live site. `ads.txt` is active. User has requested review.
- **Automation**: Critical scripts (`get_current_listings.py`, `check_listings.py`) hardened with `dotenv` and PEP 8 fixes.

## 🛠️ Pending Tasks (Next Session)

### 1. 🧹 Bulk Linting Fix (Task #2)
- **Problem**: 40+ scripts in `web/tstr-automation/` still have PEP 8 violations (mostly E402 and unused imports) and path-dependent `.env` loading.
- **Goal**: Run a recursive fix to apply the pattern:
    ```python
    import os
    from dotenv import load_dotenv
    # load_dotenv must be HERE
    load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
    # Other imports AFTER load_dotenv
    import requests
    ```
- **Tooling**: Use `ruff --fix` followed by manual verification of `load_dotenv` placement.

### 2. 📍 Location Data Backfill (Task #3)
- **Problem**: Some listings are failing insertion due to `NOT NULL constraint` on `location_id`.
- **Goal**: Identify and fix the logic in `base_scraper.py` or `enrich_listings.py` that fails to resolve a valid `location_id` for new entries.
- **Success Criteria**: No 23502 errors during a full `run_scraper.py` execution.

## 🔑 Environment Notes
- Use `PUBLIC_SUPABASE_ANON_KEY` for data fetching.
- Use `SUPABASE_SERVICE_ROLE_KEY` (if available) only for DDL/RLS migrations.
- Keys are in `.env` and `TSTR_hub_Supabase_Keys.md`.

## 📈 Current Project State
- **Branch**: `main` (pushed and verified)
- **Version**: v2.2.4
- **Live URL**: https://tstr.directory
