# OPENCODE.md - TSTR.site

> **Role**: Vibe Coding Specialist (Frontend, UI/UX, Tailwind)
> **Project**: TSTR.site (Testing Laboratory Directory)
> **Reference**: See `docs/AGENT_REFERENCE.md` for model specs and generic commands.

---

## 🚀 QUICK START
1. **Bootstrap**: `cd "/media/al/AI_SSD/AI_PROJECTS_SPACE/ACTIVE_PROJECTS/TSTR-site/tstr-site-working" && ./bootstrap.sh TSTR.site`
2. **Dev**: `cd web/tstr-frontend && npm run dev`
3. **Status**: Read `PROJECT_STATUS.md`

---

## 🛠️ TECH STACK
- **Frontend**: Astro 5.14.4 + React 18.3.1
- **Styling**: Tailwind CSS 3.4.1
- **Database**: Supabase (PostgreSQL)
- **Deployment**: Cloudflare Pages via Github push
- **Scrapers**: Python 3.9 (OCI and local)

---

## ⚠️ CRITICAL RULES (DO NOT BREAK)

### 1. SEO Hybrid Hook
- **H1**: Brand Identity (e.g., "Hydrogen Testers")
- **H2**: SEO Traffic (e.g., "Hydrogen Infrastructure Testing Services")
- **Title/Meta**: Combine both.
- **Reason**: Captures 100% of traffic.

### 2. Click Tracking
- Use `/api/out?url=...` for external links.
- **NEVER** link directly to external sites in listings.

### 3. Key Paths
- **Frontend**: `web/tstr-frontend/`
- **Scrapers**: `web/tstr-automation/`
- **Docs**: `docs/`

### 4. Environment Files (.env)
**IMPORTANT**: .env files contain sensitive secrets and are blocked from read/edit tools. Use bash commands instead:
```bash
# Create .env from example
cp web/tstr-frontend/.env.example web/tstr-frontend/.env

# Read .env file
cat web/tstr-frontend/.env

# Edit .env file
nano web/tstr-frontend/.env  # or vim, code, etc.
```

---

## 💡 OPENCODE STRATEGY

### **Best For**:
- ✅ UI Components (React/Astro)
- ✅ Tailwind Styling & Animations
- ✅ Landing Pages
- ✅ Responsive Design

### **Delegate To**:
- ❌ **Claude**: Database schema, Analytics, SEO Strategy.
- ❌ **Droid**: Bulk file processing, Performance profiling.

### **Example Prompt**:
```
Create a [feature] with:
- Modern, clean aesthetic using Tailwind CSS
- Smooth animations and micro-interactions
- Accessibility features (ARIA labels)
```

---

## 📝 RECORD LEARNINGS
When you discover a pattern, record it:
```python
# In SYSTEM/state
add_learning("GPT 5.1 Codex excels at Tailwind...", "opencode-pattern", 5, ["TSTR.site"])
```