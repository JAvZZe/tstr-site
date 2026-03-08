# Sales and Marketing Setup (salesmark)

This folder houses operations related to marketing, sales planning, and lead generation for tstr.directory.

## Structure

```
salesmark/
├── planning/             # Strategy docs, OKRs, campaign briefs, GTM strategy
├── assets/               # Email templates, ad copy, branding assets, social media graphics
├── data/                 # Lead lists, market research, competitor analysis
├── analytics/            # Reporting scripts, dashboard configs, KPI tracking
├── CRM/                  # Notes, contact routing, and integration logic for memory system/CRM
    ├── scrapers/         # Custom Python/Playwright lead generation scripts
    ├── email_outreach/   # Scripts to automate email sending (e.g., via Resend)
    └── workflows/        # Agentic workflows combining scraping and outreach
```

## Tools Available & Recommended Skills
Based on the `AI_PROJECTS_SPACE` capabilities, the following AI agent skills and extensions should be utilized for workflows in this folder:

### 🌐 Web Scraping & Lead Generation (Custom)
- **`Custom Scrapers`**: Primary tools for finding specific prospects and businesses, built natively in Python using `BaseNicheScraper` inside `/web/tstr-automation/scrapers`. Allows full control without third-party platform limitations.

### 🕵️ Advanced Research (`exa-mcp-server`)
- **`company-research`**: Finds in-depth company info, competitors, news, and financials for account-based marketing (ABM).
- **`people-research`**: Finds LinkedIn profiles and professional backgrounds for personalized outreach.

### 🗄️ CRM & Integration
- Outbound scripts should deeply integrate with the overarching **MuninnDB / Supabase** system via system agents to gain contextual contact insights before initiating an outreach sequence.
