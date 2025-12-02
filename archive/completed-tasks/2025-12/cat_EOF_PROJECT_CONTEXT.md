cat <<EOF > PROJECT_CONTEXT.md
# TSTR.site Project Context & Architecture
**Last Updated:** $(date)

## 1. Core Mission
To build the dominant directory for **high-margin, high-risk testing services** (Biotech, Hydrogen, EMC, etc.) using a **Zero-Cost/Compounding ROI** model. 
**Strategy:** Monolith Programmatic SEO (pSEO) + Open Source Lead Magnet.

## 2. Tech Stack
* **Frontend:** Astro (Static Site Generation + Dynamic Routes).
* **Styling:** Tailwind CSS.
* **Database (Primary/Web):** Supabase (PostgreSQL).
* **Database (Agent Memory/Local):** SQLite (\`~/memory/db/tstr.db\`).
* **Traffic Source:** GitHub Repository (\`awesome-niche-testing\`).
* **Outreach:** Python Scripts + AI Agents (Gemini/Claude).

## 3. Database Schema Overview
### Supabase (Production)
* **\`providers\`**: The list of labs. Columns: \`name\`, \`website\`, \`category\`, \`region\`, \`tier\`, \`status\`.
* **\`waitlist\`**: Early lead capture (Emails).
* **\`claims\`**: Inbound requests from labs to take ownership of their profile.

### SQLite (Local Agent Memory)
* **\`contacts\`**: Private contact details (Marketing Directors, Emails) - NEVER PUBLIC.
* **\`outreach_log\`**: Tracks email drafts and status (Unclaimed -> Contacted -> Verified).

## 4. Key Automation Scripts
* **\`ingest_providers.py\`**: Scrapes the GitHub \`README.md\` to update the SQLite DB.
* **\`auto_outreach.py\`**: Reads SQLite 'unclaimed' leads -> Generates email drafts using LLM.
* **\`dashboard.sh\`**: CLI-based OODA loop visualization.

## 5. Current Architecture (The Monolith)
We use a single domain (\`TSTR.site\`) with dynamic routing:
* **Route:** \`src/pages/[category]/[region]/index.astro\`
* **Logic:** Auto-generates pages like \`/biotech/usa\`, \`/hydrogen/germany\` based on DB rows.
* **SEO:** All "link juice" feeds the main domain authority.

## 6. Next Immediate Steps (Roadmap)
1.  [ ] **Execute Outreach:** Run \`auto_outreach.py\` on the initial batch of 20 leads.
2.  [ ] **Deploy:** Push Astro site to Netlify/Vercel (Free Tier).
3.  [ ] **Verify Claims:** Monitor Supabase \`claims\` table for inbound revenue opportunities.
4.  [ ] **Expand Data:** Add "Hydrogen Infrastructure" category to the GitHub list.

## 7. Rules for Agents
* **First Principles:** Always deconstruct to truth. Use Pareto (80/20).
* **No Bloat:** Do not install NPM packages unless absolutely necessary. Use native \`fetch\` and \`sqlite3\`.
* **Security:** Never commit \`.env\` or private contact data to Git.
EOF
