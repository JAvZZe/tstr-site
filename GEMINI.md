# CLAUDE.md - TSTR.site Project

> **CRITICAL**: This project is part of the AI PROJECTS SPACE continuity system.
> **Global System**: `/home/al/AI PROJECTS SPACE/`
> **Project Context**: Read `TSTR.md` (this directory) for project-specific details.

---

## Mandatory Protocol for ALL Agents

### 1. Session Start (ALWAYS)

```bash
cd "/home/al/AI PROJECTS SPACE" && ./resume.sh
```

This loads:
- Global learnings relevant to this project
- Pending tasks (filter by "TSTR.site" project tag)
- Handoff context from previous agents
- Token usage tracking

### 2. During Work

**Checkpoint frequently**:
```bash
cd "/home/al/AI PROJECTS SPACE" && ./checkpoint.sh "description of work completed"
```

**Extract learnings** after errors/discoveries:
```bash
cd "/home/al/AI PROJECTS SPACE/SYSTEM/state" && python3 << 'PYEOF'
from db_utils import add_learning
add_learning(
    "Your learning here",
    "gotcha",  # or "pattern", "optimization", "security"
    confidence=5,
    tags=["TSTR.site", "relevant-tech", "specific-issue"]
)
PYEOF
```

**Track tasks**:
```bash
cd "/home/al/AI PROJECTS SPACE/SYSTEM/state" && python3 << 'PYEOF'
from db_utils import add_task, update_task
task_id = add_task("TSTR.site", "Task description", assigned_to="claude")
# ... do work ...
update_task(task_id, "completed", result="Result summary")
PYEOF
```

### 3. Session End or Handoff

```bash
cd "/home/al/AI PROJECTS SPACE" && ./handoff.sh <agent> <reason>
```

---

## Project-Specific Instructions

**Read these files IN ORDER**:

1. **START_HERE.md** - Quick orientation checklist
2. **TSTR.md** - PRIMARY agent instructions (architecture, commands, priorities)
3. **.ai-session.md** - Latest session context and active tasks
4. **PROJECT_STATUS.md** - Deployment status and infrastructure details
5. **HANDOFF_TO_CLAUDE.md** - Current handoff (if exists)

---

## Quick Reference

**Project Root**: `/home/al/AI PROJECTS SPACE/ACTIVE_PROJECTS/TSTR-site/tstr-site-working`

**Frontend**: `web/tstr-frontend/` (Astro + React + Tailwind)
**Scrapers**: `web/tstr-automation/` (Python, deployed on OCI)
**Database**: Supabase (https://haimjeaetrsaauitrhfy.supabase.co)

**Website**: http://tstr.site (LIVE - 163 listings as of 2025-11-17)

**Git Repo**: https://github.com/JAvZZe/tstr-site.git

---

## Why This Matters

**Token Economics**: Recording learnings prevents repeated mistakes across sessions.
- Repeated error = ~5000 tokens wasted
- Learning recorded once = ~200 tokens
- ROI after 1-2 avoided repetitions

**Continuity**: Without checkpoints/learnings, context is lost between sessions.
- Failed work = wasted time and money
- Checkpoints = instant recovery from failures

**Game Theory**: Using the continuity system is the optimal strategy for long-term project success.

---

## Enforcement

**Self-check compliance**:
```bash
cd "/home/al/AI PROJECTS SPACE" && ./SYSTEM/enforcement/protocol_check.sh
```

Should show:
- ✅ Checkpoints created
- ✅ Learnings recorded
- ✅ Tasks tracked

If any fail → fix violations before continuing.

---

## Development Principles

See `TSTR.md` for:
- User profile (non-tech, AuDHD, OODA + Pareto + First Principles)
- Architecture (frontend, scrapers, database)
- Current priorities (P0, P1, P2)
- Code standards
- Common patterns
- Troubleshooting guides

**Remember**: First Principles. OODA Loop. Test before deploy. No theater, working code only.

---

**Last Updated**: 2025-11-17
**System Version**: AI PROJECTS SPACE v2.0
