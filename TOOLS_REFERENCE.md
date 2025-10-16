# TSTR.site - Tools & Plugins Reference

**Last Updated**: 2025-10-15 17:00 UTC  
**Environment**: Windows 11, PowerShell 7, Windsurf IDE

---

## 🎯 Currently Active Tools

### CASCADE (Windsurf IDE)
- **Status**: ✅ Active
- **Access**: Native IDE agent
- **Capabilities**: Full-stack development, DevOps, multi-file editing
- **Token Budget**: 200K per session
- **Best For**: Complex integrations, debugging, platform setup

### CLI Tools Installed
1. **Node.js** - v18+ (frontend development)
2. **npm** - Package manager for JavaScript
3. **Python** - v3.14 (backend automation)
4. **pip** - Package manager for Python
5. **Git** - Version control
6. **Wrangler** - Cloudflare Pages CLI (via npx)
7. **Claude CLI** - Available but not yet configured
8. **Gemini CLI** - Available but not yet configured

---

## 🔧 Recommended IDE Extensions

### High Priority (Enable These Next)

#### 1. Python Extension
- **ID**: `ms-python.python`
- **Why**: Linting, debugging, IntelliSense for Python scripts
- **Use Case**: Backend automation scripts, import scripts
- **Enable**: Windsurf → Extensions → Search "Python" → Install

#### 2. Astro Extension
- **ID**: `astro-build.astro-vscode`
- **Why**: Syntax highlighting, IntelliSense for Astro files
- **Use Case**: Frontend development (tstr-frontend)
- **Enable**: Extensions → Search "Astro" → Install

#### 3. Tailwind CSS IntelliSense
- **ID**: `bradlc.vscode-tailwindcss`
- **Why**: Auto-complete for Tailwind classes
- **Use Case**: Frontend styling
- **Enable**: Extensions → Search "Tailwind CSS" → Install

#### 4. ESLint
- **ID**: `dbaeumer.vscode-eslint`
- **Why**: JavaScript/TypeScript linting
- **Use Case**: Code quality, catch errors early
- **Enable**: Extensions → Search "ESLint" → Install

#### 5. Prettier
- **ID**: `esbenp.prettier-vscode`
- **Why**: Code formatting consistency
- **Use Case**: Auto-format on save
- **Enable**: Extensions → Search "Prettier" → Install

### Medium Priority (Optional)

#### 6. GitLens
- **ID**: `eamodio.gitlens`
- **Why**: Advanced Git features (blame, history, compare)
- **Use Case**: Understanding code history, collaboration
- **Enable**: Extensions → Search "GitLens" → Install

#### 7. Error Lens
- **ID**: `usernamehw.errorlens`
- **Why**: Inline error/warning display
- **Use Case**: See errors without hovering
- **Enable**: Extensions → Search "Error Lens" → Install

#### 8. Better Comments
- **ID**: `aaron-bond.better-comments`
- **Why**: Colorize different comment types
- **Use Case**: TODO, FIXME, NOTE highlighting
- **Enable**: Extensions → Search "Better Comments" → Install

---

## 🚀 Additional CLI Tools to Consider

### High Priority (Not Yet Installed)

#### 1. Supabase CLI
- **Purpose**: Direct database operations, migrations
- **Install**:
  ```powershell
  npm install -g supabase
  ```
- **Use Cases**:
  - Database migrations
  - Local development
  - Schema management
  - Direct SQL execution
- **Why Now**: Would simplify database operations

#### 2. GitHub CLI (gh)
- **Purpose**: GitHub operations from terminal
- **Install**: https://cli.github.com/
- **Use Cases**:
  - Create/manage issues
  - PR operations
  - Repository management
- **Why Later**: Nice to have, not critical

### Medium Priority

#### 3. Vercel CLI
- **Purpose**: Alternative deployment platform
- **Install**: `npm install -g vercel`
- **Use Cases**: Testing alternative hosting
- **Why Later**: Already using Cloudflare Pages

---

## 📦 Project Dependencies

### Frontend (web/tstr-frontend/)

**Core**:
```json
{
  "astro": "^5.14.4",
  "react": "^18.3.1",
  "react-dom": "^18.3.1",
  "@astrojs/react": "^3.6.2",
  "@astrojs/tailwind": "^5.1.1",
  "tailwindcss": "^3.4.1",
  "@supabase/supabase-js": "^2.45.4"
}
```

**Dev Dependencies**:
```json
{
  "supabase": "^2.51.0"
}
```

**Status**: ✅ Installed and working

### Backend (web/tstr-automation/)

**Requirements**:
```txt
beautifulsoup4==4.12.3
requests==2.31.0
schedule==1.2.0
supabase
python-dotenv==1.0.0
```

**Status**: ✅ Installed and working (fixed from `supabase-python`)

---

## 🔌 Platform Integrations

### Currently Connected

#### 1. GitHub
- **Status**: ✅ Connected
- **Auth Method**: Personal Access Token (PAT)
- **Repository**: https://github.com/JAvZZe/tstr-site.git
- **Access**: Read/Write
- **Auto-Deploy**: Yes (Cloudflare watches repo)

#### 2. Cloudflare Pages
- **Status**: ✅ Deployed
- **Project**: tstr-site
- **Domain**: tstr.site
- **Auto-Deploy**: Yes (on git push)
- **Issue**: ⚠️ Environment variables need update

#### 3. Supabase
- **Status**: ✅ Connected
- **Project**: haimjeaetrsaauitrhfy
- **Database**: PostgreSQL (20 listings imported)
- **Auth**: Publishable + Service Role keys
- **Issue**: ⚠️ Frontend needs publishable key in Cloudflare env vars

### Not Yet Connected

#### 1. Analytics (Optional)
- Google Analytics
- Cloudflare Web Analytics
- Plausible Analytics

#### 2. Monitoring (Optional)
- Sentry (error tracking)
- LogRocket (session replay)
- UptimeRobot (uptime monitoring)

#### 3. Email (Future)
- SendGrid / Mailgun
- For contact forms, notifications

---

## 🤖 Agent CLI Configuration

### Claude Code CLI

**Status**: Installed but not configured  
**Purpose**: Deep architectural work, complex debugging

**Setup** (when needed):
```powershell
# Check if installed
claude --version

# Configure (if needed)
claude configure

# Test connection
claude "Hello world"
```

**Use When**:
- CASCADE needs architectural guidance
- Complex multi-file refactoring (>10 files)
- Deep algorithmic problems
- Token budget running low

### Gemini CLI

**Status**: Installed but not configured  
**Purpose**: Fast, token-efficient simple tasks

**Setup** (when needed):
```powershell
# Check if installed
gemini --version

# Configure with API key (already in .env)
# GEMINI_API_KEY in root .env

# Test connection
gemini "Write hello world in Python"
```

**Use When**:
- Simple code generation (<50 lines)
- Documentation writing
- SQL queries
- CSV processing scripts
- Need to conserve CASCADE tokens

**Last Issue**: API overload (503) during pip install - service was temporarily unavailable

---

## 📋 Tool Usage Guidelines

### When to Use CASCADE
✅ Multi-file editing  
✅ Terminal operations  
✅ Git workflow  
✅ Debugging  
✅ Platform configuration  
✅ Deployment  
✅ Complex integrations  

### When to Use Claude Code CLI
✅ Architectural decisions  
✅ Complex refactoring (>10 files)  
✅ Strategic planning  
✅ When CASCADE tokens < 50K  

### When to Use Gemini CLI
✅ Simple code generation  
✅ Boilerplate creation  
✅ Documentation  
✅ SQL queries  
✅ Data processing scripts  
✅ Quick utility functions  

### When to Use Comet Assistant
✅ Web dashboard navigation  
✅ Research/documentation lookup  
✅ Retrieving API keys from UIs  
✅ Web form submissions  

---

## 🔒 Security Tools & Practices

### Current Setup
- ✅ `.gitignore` configured (excludes .env files)
- ✅ Environment variables in separate .env files
- ✅ API keys not hardcoded
- ✅ Git credential manager for GitHub auth

### Recommended Additions

#### 1. git-secrets
- **Purpose**: Prevent committing secrets
- **Install**: https://github.com/awslabs/git-secrets
- **Setup**:
  ```powershell
  # Install git-secrets
  # Then in repo:
  git secrets --install
  git secrets --register-aws
  ```

#### 2. Environment Variable Validation
- **Purpose**: Catch missing env vars early
- **Implementation**: Add to startup scripts
- **Example** (Python):
  ```python
  import os
  required = ['SUPABASE_URL', 'SUPABASE_KEY']
  missing = [k for k in required if not os.getenv(k)]
  if missing:
      raise Exception(f"Missing env vars: {missing}")
  ```

---

## 📊 Performance & Monitoring Tools

### Frontend Performance

#### Lighthouse (Built into Chrome)
- **Access**: F12 → Lighthouse tab
- **Metrics**: Performance, SEO, Accessibility, Best Practices
- **Use**: Before launch, after major changes

#### Web Vitals
- **Install**: `npm install web-vitals`
- **Use**: Monitor Core Web Vitals (LCP, FID, CLS)

### Backend Performance

#### Python Profiling
- **Built-in**: `cProfile`
- **Use**:
  ```python
  python -m cProfile -s time import_to_supabase.py
  ```

---

## 🎓 Learning Resources

### Astro
- Docs: https://docs.astro.build
- Tutorial: https://docs.astro.build/en/tutorial/0-introduction/

### Supabase
- Docs: https://supabase.com/docs
- Python Client: https://supabase.com/docs/reference/python

### Cloudflare Pages
- Docs: https://developers.cloudflare.com/pages/
- Framework Guides: https://developers.cloudflare.com/pages/framework-guides/

### Tailwind CSS
- Docs: https://tailwindcss.com/docs
- Components: https://tailwindui.com/components

---

## ✅ Recommended Next Steps

### Immediate (This Session)
1. Update Cloudflare environment variables (user action)
2. Verify site loads correctly

### Short Term (Next Session)
1. Install Python extension for better development experience
2. Install Astro extension for frontend work
3. Install Tailwind CSS IntelliSense
4. Configure ESLint and Prettier

### Medium Term
1. Set up Supabase CLI for easier database operations
2. Configure Claude Code CLI for architectural work
3. Add analytics (Cloudflare Web Analytics - free)
4. Set up basic monitoring

### Long Term
1. Implement CI/CD testing
2. Add error monitoring (Sentry)
3. Performance optimization
4. SEO improvements

---

**Document Version**: 1.0  
**Last Updated**: 2025-10-15 17:00 UTC  
**Maintained By**: CASCADE Agent
