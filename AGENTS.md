# AGENTS.md - Development Guidelines for TSTR.site

## 🚀 INITIALIZATION (MANDATORY)

**When starting any session in this project:**
```bash
./bootstrap.sh TSTR-site    # Load project context, learnings, and pending tasks
```

This loads:
- Project-specific learnings from database
- Pending tasks for TSTR-site
- Recent session context
- Pending handoffs
- Recent checkpoints

## Commands

### Frontend (Astro + React)
```bash
cd web/tstr-frontend
npm run dev          # Start dev server
npm run build        # Build for production
npm run preview      # Preview production build
```

### Testing
```bash
npm run test          # Run all Playwright tests
npx playwright test tests/example.spec.ts    # Run single test
npx playwright test --grep "test name"      # Run tests by name
```

### Python Scrapers
```bash
cd web/tstr-automation
pip install -r requirements.txt
python scrapers/a2la_materials.py    # Run specific scraper
```

## Code Style

### TypeScript/JavaScript
- Use strict TypeScript config (`extends: "astro/tsconfigs/strict"`)
- Import order: 1) External libs, 2) Internal components, 3) Relative imports
- Use React functional components with hooks
- Error handling with try/catch and proper logging

### Python
- Use type hints (`from typing import Dict, List, Optional`)
- Import order: 1) stdlib, 2) third-party, 3) local imports
- Inherit from `BaseNicheScraper` for all scrapers
- Use logging, not print statements

### Astro
- Use `export const prerender = true` for static pages
- Fetch data in frontmatter with Supabase client
- Use Tailwind CSS classes, avoid inline styles

### Naming
- Files: kebab-case (`my-component.astro`, `scraper_name.py`)
- Components: PascalCase (`MyComponent`)
- Variables/functions: camelCase (JS) or snake_case (Python)
- Constants: UPPER_SNAKE_CASE

### Git Commits
- Format: `[AGENTNAME] Brief description`
- Include context in body for complex changes