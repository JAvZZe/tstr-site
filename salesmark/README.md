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
└── automation/           # Scripts and tools for outreach and data gathering
    ├── apify_skills/     # Specific Apify actors or configurations for scraping
    ├── email_outreach/   # Scripts to automate email sending (e.g., via Resend)
    └── workflows/        # Agentic workflows combining scraping and outreach
```

## Tools Available
We use **Apify** for localized scraping and standard outreach scripts, integrating deeply with the overarching **MuninnDB** base via system agents to gain contact insights before initiating outreach.
