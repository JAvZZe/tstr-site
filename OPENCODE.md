# OPENCODE.md

Guidance for OpenCode AI agent when working with code in this repository.

## System Overview

**AI_PROJECTS_SPACE v2.0** - Multi-agent continuity system for long-running projects with persistent memory, reasoning, learning and self improvement, checkpoint/resume, and token-aware routing.

**Purpose**: Handle complex multi-session tasks (like building the TSTR.site project) where context preservation, agent handoffs, and learning accumulation are critical.

## Agent Specializations

**OpenCode (You)**: Vibe coding specialist, modern web frameworks, UI/UX patterns, rapid prototyping
**Claude**: Architecture, reasoning, analytics, SEO strategy, complex system integration  
**Droid**: Tool efficiency, parallel operations, performance optimization, native tool usage

**Collaboration Pattern**: 
- OpenCode → UI components, styling, frontend features
- Claude → System architecture, analytics, SEO implementation
- Droid → Performance optimization, tool automation, bulk operations

## Active Projects Overview

### TSTR.site (Primary Project)
**Type**: Global B2B testing laboratory directory
**Status**: Production (163 listings live)
**Tech Stack**: Astro 5.14.4 + React 18.3.1 + Tailwind CSS + Supabase
**Deployment**: Cloudflare Pages (frontend) + Oracle Cloud Infrastructure (scrapers)
**Strategic Focus**: Hydrogen Infrastructure Testing + Biotech/Pharma/Life Sciences

### Project Locations
- **TSTR.site**: `/media/al/AI_SSD/AI_PROJECTS_SPACE/ACTIVE_PROJECTS/TSTR-site/tstr-site-working/`
- **File Cleanup**: 35K files project (not started yet)

## OpenCode Model Capabilities & Recommendations

### Best OpenCode Models for Web Directory Projects

**For Vibe/Prompt Coding (Web Directory Projects):**

1. **GPT 5.1 Codex** (`opencode/gpt-5.1-codex`) - **PRIMARY CHOICE**
   - Specialized for code generation and UI patterns
   - Excellent with modern web frameworks (React, Vue, Next.js, Astro)
   - Strong understanding of design systems and Tailwind CSS
   - Cost: $1.07/1M input, $8.50/1M output
   - **Use for**: UI components, styling, landing pages, responsive design

2. **Qwen3 Coder** (`opencode/qwen3-coder`) - **BUDGET WORKHORSE**
   - Good code generation capabilities
   - Cost-effective for bulk operations and repetitive tasks
   - Cost: $0.45/1M input, $1.50/1M output
   - **Use for**: Component scaffolding, bulk file generation, template work

3. **Claude Sonnet 4.5** (`opencode/claude-sonnet-4-5`) - **COMPLEX ARCHITECTURE**
   - Strong reasoning and system design skills
   - Better for complex integrations and API work
   - Cost: $3.00/1M input, $15.00/1M output
   - **Use for**: Database schema, API integration, analytics systems (delegate to Claude when possible)

**Free Models (for testing/simple tasks):**
- **GPT 5 Nano** (`opencode/gpt-5-nano`) - Free, good for prototyping and exploration
- **Big Pickle** (`opencode/big-pickle`) - Free, experimental model

### Model Selection Strategy for TSTR.site

**OpenCode Strengths:**
- ✅ Rapid UI prototyping with Tailwind CSS
- ✅ Modern component architecture (React/Astro)
- ✅ Responsive design and mobile-first approach
- ✅ Design system implementation
- ✅ Landing page optimization

**OpenCode Weaknesses (Delegate to other agents):**
- ❌ Complex database operations → Use Claude
- ❌ Performance optimization → Use Droid  
- ❌ Bulk file processing → Use Droid
- ❌ SEO strategy implementation → Use Claude
- ❌ System architecture decisions → Use Claude

### Why GPT 5.1 Codex for Web Directory Projects

- **Vibe Coding**: Excels at rapid prototyping and aesthetic UI generation
- **Prompt Engineering**: Strong natural language to code translation
- **Modern Stack**: Up-to-date with current web development patterns
- **Design Sense**: Better at implementing visually appealing interfaces
- **Component Architecture**: Good at breaking down UI into reusable components

## User Profile & Communication Style

**Non-tech, AuDHD. Terse, factual, critique bad ideas. OODA + Pareto. First Principles Thinking. Game Theory. Root Cause Analysis. Test before deploying.**

### OpenCode Communication Guidelines:
- **Be concise** - User prefers terse, factual responses
- **Show working code** - No theater, demonstrate results
- **Test before suggesting** - Always verify functionality
- **First principles** - Question framework choices
- **OODA Loop** - Observe, Orient, Decide, Act rapidly

### When to Handoff:
- **Database/Analytics complexity** → Claude
- **Performance/bulk operations** → Droid
- **System architecture questions** → Claude
- **UI/UX implementation** → Keep (OpenCode strength)

## Development Environment

**OS**: Linux Ubuntu 24.04 (6.14.0-33-generic kernel)
**Shell**: Bash scripting is native - use bash for automation, file operations, and system tasks.
**Path**: `/home/al/AI_PROJECTS_SPACE/` - always work within this folder and subfolders, avoid saving project files to the PC root.
**Hardware**: 40GB RAM, i5-1135G7, NVIDIA MX330 GPU (CUDA 12.2), 39GB free SSD
**External Storage**: 2x 1TB drives mounted (one has 35K files of the TSTR.site project to process and clean)

### OpenCode-Specific Tools

**Available through OpenCode TUI:**
- Native file editing and creation
- Terminal command execution
- Multi-file project awareness
- LSP integration for code intelligence
- Git integration
- Image analysis for design reference

**Pre-approved CLI Tools:**
- `oci` - Oracle Cloud Infrastructure CLI (ACTIVE for TSTR.site scrapers)
- `supabase` - Supabase CLI for database operations (ACTIVE)
- `wrangler` - Cloudflare Workers (for TSTR.site deployment)
- `gh` - GitHub CLI (authenticated, repository connected)
- `npm`, `node` - Node.js ecosystem (TSTR.site uses Astro + React)
- `bru` - Bruno CLI for API testing (v2.14.0, MCP integrated)
- `python3`, `pip3` - Python ecosystem (scrapers on OCI)
- `uv` - Fast Python package manager (installed at /snap/bin/uv)

### TSTR.site Infrastructure

**Production Stack:**
- **Frontend**: Astro 5.14.4 + React 18.3.1 + Tailwind CSS
- **Database**: Supabase PostgreSQL (free tier, 163 listings)
- **Scrapers**: Python 3.9.21 on Oracle Linux 9 (OCI instance 84.8.139.90)
- **Deployment**: Cloudflare Pages (via GitHub auto-deploy)
- **Scheduler**: Cron daily at 2 AM GMT

**Key URLs:**
- **Live Site**: https://tstr.site
- **Database**: https://haimjeaetrsaauitrhfy.supabase.co

**API Keys:**
- **Anon Key**: sb_publishable_EFSlg4kPRIvAYExPmyUJyA_7_BiJnHO
- **Service Role Key**: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhhaW1qZWFldHJzYWF1aXRyaGZ5Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2MDQzNjU4NSwiZXhwIjoyMDc2MDEyNTg1fQ.zd47WtS1G1XzjP1obmr_lxHU_xJWtlhhu4ktm9xC5hA

**MCP Server**: ✅ Configured in `web/tstr-automation/TSTR1.mcp.json`
- Server: @supabase/mcp-server-supabase@latest
- Project Ref: haimjeaetrsaauitrhfy
- Access Token: sbp_e290bc7ea1ba64ae4b0be38134b7b4a67ca24e04
- Mode: Read-only
- **GitHub**: https://github.com/JAvZZe/tstr-site.git

## OpenCode Workflow Patterns

### 1. Project Initialization
```bash
cd /path/to/project
opencode
/init  # Creates AGENTS.md file
```

### 2. Vibe Coding Pattern
```
Create a modern directory website with:
- Hero section with gradient background
- Category cards with hover effects
- Search functionality with autocomplete
- Responsive design using Tailwind CSS
- Dark mode toggle
Use Next.js 14 with TypeScript
```

### 3. Plan Mode for Complex Features
```
<TAB>  # Switch to Plan mode
Build a multi-vendor marketplace with:
- User authentication system
- Product listing pages
- Shopping cart functionality
- Payment integration
- Admin dashboard
```

### 4. Iterative Development
```
Add a filter sidebar to the directory
Reference this design: [drag-drop image]
Make it collapsible on mobile
```

## Core System Commands (Continuity)

### Continuity Workflow
```bash
./resume.sh              # Load checkpoint + context (START HERE)
./checkpoint.sh "label"  # Save state
./handoff.sh <agent> <reason>  # Transfer to another agent
```

### Database Operations
```bash
cd SYSTEM/state
python3 db_utils.py init                    # Initialize DB
python3 db_utils.py session-start <agent> <task>
python3 db_utils.py checkpoint "label"
python3 db_utils.py task-add <project> <description>
python3 db_utils.py task-list
python3 db_utils.py stats
python3 db_utils.py learning-query [tags...]
```

## OpenCode + System Integration

### Mandatory Protocol

**ALL agents must use continuity system:**

1. **Start Session**: `cd "/media/al/AI_SSD/AI_PROJECTS_SPACE" && ./bootstrap.sh TSTR.site`
2. **During Work**: `./checkpoint.sh "progress description"`
3. **Record Learnings**: Use database utils to add findings
4. **Handoff**: `./handoff.sh <agent> <reason>`

### OpenCode-Specific Strengths for TSTR.site

**EXCELLENT AT:**
- ✅ Modern UI components with Tailwind CSS
- ✅ Responsive design and mobile optimization
- ✅ Component architecture and reusability
- ✅ Landing page creation and optimization
- ✅ Design system implementation
- ✅ Rapid prototyping and vibe coding
- ✅ Astro + React integration patterns

**AVOID/DELEGATE:**
- ❌ Complex Supabase queries → Claude
- ❌ Analytics system modifications → Claude  
- ❌ Performance profiling → Droid
- ❌ Bulk file operations → Droid
- ❌ Complex bash scripting → Droid

### OpenCode-Specific Learnings

When using OpenCode, record these learnings:
```python
from SYSTEM.state.db_utils import add_learning
add_learning(
    "GPT 5.1 Codex excels at Tailwind CSS utility classes",
    "opencode-model",
    confidence=5,
    tags=["opencode", "gpt-5.1-codex", "css", "tailwind"]
)
```

### Token Economics with OpenCode

**OpenCode Zen Pricing** (per 1M tokens):
- GPT 5.1 Codex: $1.07 input, $8.50 output
- Claude Sonnet 4.5: $3.00 input, $15.00 output
- Qwen3 Coder: $0.45 input, $1.50 output
- GPT 5 Nano: FREE

**Strategy**:
- Use GPT 5.1 Codex for: UI components, styling, rapid prototyping
- Use Qwen3 Coder for: Bulk code generation, repetitive tasks
- Use GPT 5 Nano for: Testing, simple scripts, exploration

## Web Directory Project Patterns

### TSTR.site Tech Stack (Current)
```
Framework: Astro 5.14.4 with React integration
Styling: Tailwind CSS 3.4.1
Database: Supabase PostgreSQL (free tier)
Authentication: Supabase Auth
Deployment: Cloudflare Pages (free tier)
API: Supabase REST + MCP integration
```

### Vibe Coding Approach
1. **Design-First**: Start with visual design and user experience
2. **Component-Based**: Build reusable UI components
3. **Progressive Enhancement**: Start simple, add complexity incrementally
4. **Mobile-First**: Responsive design from mobile up

### Prompt Engineering for Web Directories
```
Create a [feature] with:
- Modern, clean aesthetic using Tailwind CSS
- Smooth animations and micro-interactions
- Accessibility features (ARIA labels, keyboard navigation)
- SEO optimization (meta tags, structured data)
- Performance optimization (lazy loading, image optimization)
```

### TSTR.site Specific Patterns

**SEO Hybrid Hook (MANDATORY - Claude Implemented)**:
- H1 = Brand Identity ("[Category] Testers")
- H2 = SEO Traffic ("[Category] Testing Services")
- Title/Meta = Both keywords combined
- Purpose: Capture 100% of search traffic (vs 20% with brand-only)
- ⚠️ **DO NOT MODIFY** - Claude's implementation is live and working

**Current Live Features (Do Not Break)**:
- ✅ Click tracking system (`/api/out` redirect endpoint)
- ✅ Analytics dashboard (`/admin/analytics`)
- ✅ Low-density concierge fallback (mailto links)
- ✅ Category/region dynamic routes with static prerendering
- ✅ Supabase API integration (new key format: `sb_*`)

**Component Structure**:
```
src/
├── pages/
│   ├── index.astro              # Homepage
│   ├── [category]/index.astro   # Category pages (Hybrid Hook)
│   └── [category]/[region]/index.astro  # Region pages
├── components/
│   ├── Header.astro
│   ├── Footer.astro
│   └── ListingCard.astro
└── layouts/
    └── Layout.astro
```

**Data Flow**:
```
OCI Scrapers → Supabase DB → Astro Build → Static Pages → Cloudflare Edge
```

## Critical Patterns

### 1. Always Bootstrap First (TSTR.site Protocol)
```bash
cd "/media/al/AI_SSD/AI_PROJECTS_SPACE/ACTIVE_PROJECTS/TSTR-site/tstr-site-working"
./bootstrap.sh TSTR.site  # Loads project-specific learnings & context
```

**Note**: The bootstrap script file is `Link_to_bootstrap_agent.sh` in the project root. Always run bootstrap at the start of every session.

### 2. Use Plan Mode for Complex Features
```bash
<TAB>  # Switch to Plan mode in OpenCode
# Describe the feature
# Review the plan
<TAB>  # Switch back to Build mode
# Implement
```

### 3. Extract Learnings
When you discover effective patterns:
```bash
cd "/home/al/AI_PROJECTS_SPACE/SYSTEM/state"
python3 db_utils.py learning-add \
  "OpenCode's GPT 5.1 Codex generates better Tailwind classes than manual writing" \
  "opencode-pattern" \
  5 \
  "TSTR.site,opencode,tailwind,productivity"
```

### 4. Token-Aware Development
- Use Plan mode to avoid costly rewrites
- Start with cheaper models for scaffolding
- Use premium models for complex components
- Batch similar requests together

### 5. TSTR.site Specific Protocol
```bash
# During work
cd "/media/al/AI_SSD/AI_PROJECTS_SPACE" && ./checkpoint.sh "description"

# End of session
cd "/media/al/AI_SSD/AI_PROJECTS_SPACE" && ./handoff.sh <agent> <reason>

# Check compliance
cd "/media/al/AI_SSD/AI_PROJECTS_SPACE" && ./SYSTEM/enforcement/protocol_check.sh"
```

### 6. OpenCode Handoff Guidelines

**When to handoff to Claude:**
- Database schema changes or complex queries
- Analytics system modifications
- SEO strategy implementation
- API integration challenges
- System architecture decisions

**When to handoff to Droid:**
- Performance optimization tasks
- Bulk file operations or processing
- Complex bash scripting needs
- Tool automation requirements
- Parallel processing tasks

**Handoff format:**
```bash
cd "/media/al/AI_SSD/AI_PROJECTS_SPACE" && ./handoff.sh claude "Need database schema modification for new feature"
cd "/media/al/AI_SSD/AI_PROJECTS_SPACE" && ./handoff.sh droid "Performance optimization needed for scraper batch processing"
```

## File Structure Integration

```
AI_PROJECTS_SPACE/
├── checkpoint.sh, resume.sh, handoff.sh   # Core workflow
├── SYSTEM/
│   ├── state/              # SQLite persistence
│   ├── agents/             # Client scripts
│   └── mcp-servers/        # MCP integrations
├── ACTIVE_PROJECTS/        # Current work
│   └── [project-name]/
│       ├── AGENTS.md       # OpenCode project context
│       └── [project files]
└── OPENCODE.md             # This file
```

## OpenCode Configuration

### Recommended Config for Web Directory Projects

```json
{
  "$schema": "https://opencode.ai/config.json",
  "model": "opencode/gpt-5.1-codex",
  "provider": {
    "opencode": {
      "models": {
        "gpt-5.1-codex": {
          "options": {
            "temperature": 0.7,
            "maxTokens": 8192
          }
        }
      }
    }
  }
}
```

### LSP Servers for Web Development
- `typescript-language-server`
- `tailwindcss-language-server`
- `css-language-server`
- `html-language-server`

## Methodology Principles (Applied to OpenCode)

### First Principles + Vibe Coding
- Question framework choices ("Why Next.js vs Remix?")
- Build from user experience backward
- Optimize for developer experience AND end-user experience

### Game Theory + Token Economics
- Choose models based on task complexity
- Use Plan mode to reduce token waste
- Batch similar UI components together

### OODA Loop with OpenCode
1. **Observe**: Review existing code with `@` file search
2. **Orient**: Check AGENTS.md and project context
3. **Decide**: Choose model and approach
4. **Act**: Implement with OpenCode, checkpoint frequently

## Recovery and Error Handling

### If OpenCode Generates Poor Code
```bash
cd "/home/al/AI_PROJECTS_SPACE" && ./checkpoint.sh "before attempting refactor"
# Use /undo in OpenCode
# Try different prompt or model
cd "/home/al/AI_PROJECTS_SPACE" && ./resume.sh  # If needed, revert to last checkpoint
```

### Model Switching
```bash
# Switch to cheaper model for bulk work
/models
# Select qwen3-coder
# Continue work
```

## Project-Specific Workflows

### TSTR.site Development Workflow

**OpenCode-Focused Workflow:**
```bash
# 1. Bootstrap project context
cd "/media/al/AI_SSD/AI_PROJECTS_SPACE/ACTIVE_PROJECTS/TSTR-site/tstr-site-working"
./bootstrap.sh TSTR.site

# 2. Frontend development (OpenCode specialty)
cd web/tstr-frontend
npm run dev          # Local development
npm run build        # Build for deployment
npm run lint         # Code quality check

# 3. Component development (OpenCode strength)
# Focus on: src/components/, src/pages/, Tailwind styling
# Avoid: Complex database queries, API endpoints

# 4. Testing and verification
npm run test         # Run tests before deployment
npm run preview      # Preview production build

# 5. Database operations (Delegate to Claude if complex)
~/.local/bin/supabase status  # Simple checks only
# Complex queries → handoff to Claude

# 6. API testing (Delegate to Droid for bulk testing)
bru run bruno/supabase/health/ --env production  # Simple tests only
# Complex API testing → handoff to Droid
```

**OpenCode Task Examples:**
- "Create a modern contact form component with Tailwind CSS"
- "Add dark mode toggle to the header"
- "Design a responsive pricing section"
- "Implement smooth scroll animations"
- "Create category filter UI components"

### File Cleanup Project Workflow (35K Files)
```bash
# 1. Bootstrap global system
cd "/home/al/AI_PROJECTS_SPACE"
./resume.sh

# 2. Add tasks for file processing
python3 SYSTEM/state/db_utils.py task-add "FileCleanup" "Scan directory structure"
python3 SYSTEM/state/db_utils.py task-add "FileCleanup" "Sample 100 files for analysis"

# 3. Use OpenRouter for bulk processing
./SYSTEM/agents/openrouter_client.sh "process 1000 files with pattern X"
```

## Verification

### Check OpenCode Integration
```bash
cd "/home/al/AI_PROJECTS_SPACE" && ./resume.sh
```

Should show:
- Recent learnings about OpenCode patterns
- Tasks with OpenCode model usage
- Token efficiency metrics

### Protocol Compliance
```bash
cd "/home/al/AI_PROJECTS_SPACE" && ./SYSTEM/enforcement/protocol_check.sh
```

Should show:
- ✅ Checkpoints created
- ✅ Learnings recorded
- ✅ Tasks tracked

## OpenCode Performance Metrics

### Track Your Effectiveness
```bash
# Record learnings about model performance
cd "/media/al/AI_SSD/AI_PROJECTS_SPACE/SYSTEM/state"
python3 << 'PYEOF'
from db_utils import add_learning

# UI Generation Speed
add_learning(
    "GPT 5.1 Codex generates responsive Tailwind components 3x faster than manual coding",
    "opencode-performance",
    confidence=5,
    tags=["TSTR.site", "opencode", "tailwind", "productivity"]
)

# When to delegate
add_learning(
    "Complex Supabase queries better handled by Claude - OpenCode struggles with SQL optimization",
    "opencode-limitation",
    confidence=4,
    tags=["TSTR.site", "opencode", "supabase", "delegation"]
)
PYEOF
```

### Success Indicators
- ✅ UI components deployed without bugs
- ✅ Responsive design works across devices
- ✅ Tailwind CSS follows design system
- ✅ Components are reusable and maintainable
- ✅ Page load times remain fast
- ✅ User experience improvements measured

### When You're Not the Right Tool
- Database performance issues → Claude
- SEO optimization needs → Claude  
- Bulk data processing → Droid
- Complex API integrations → Claude
- Performance profiling → Droid

---

**OpenCode integration added**: 2025-11-24 - Optimized for web directory development
**TSTR.site specifics integrated**: 2025-11-24 - Production-ready patterns and protocols
**Agent collaboration defined**: 2025-11-24 - Clear handoff guidelines and specialization areas