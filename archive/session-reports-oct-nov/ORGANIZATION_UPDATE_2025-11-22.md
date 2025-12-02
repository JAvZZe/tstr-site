# Organization Update - November 22, 2025

## Directory Restructuring

**Effective**: November 22, 2025
**Updated By**: User (al)

### New Niche-Focused Directory Structure

To support focused vertical development, project documentation is now organized by industry niche:

#### 1. **Hydrogen Infrastructure Testing**
**Path**: `/home/al/AI_PROJECTS_SPACE/ACTIVE_PROJECTS/TSTR-site/tstr-site-working/Hydrogen Infrastructure Testing`

**Contents**: All session documentation, implementation notes, and handoffs related to hydrogen testing standards
- Hydrogen standards implementation (ASME, ISO)
- Standards search functionality
- Whale Labs listing integration
- Google Search Console setup for hydrogen niche
- Session completions and handoffs

**Purpose**: Centralized knowledge base for hydrogen infrastructure testing vertical

#### 2. **Biotech Directory**
**Path**: `/home/al/AI_PROJECTS_SPACE/ACTIVE_PROJECTS/TSTR-site/tstr-site-working/Biotech Directory`

**Contents**: Biotech/Pharma/Life Sciences testing resources
- Biotech listings summaries
- Waitlist implementation and fixes
- Auto-outreach scripts for biotech labs
- CRM utilities for lead generation
- Cold email templates
- Sponsorship and contribution guidelines

**Purpose**: Growth resources for biotech/pharma/life sciences testing vertical

---

## Strategic Focus

### Phase 1: Hydrogen + Biotech/Pharma/Life Sciences

**Rationale**: 
- High-margin, specialized niches
- Clear regulatory requirements = strong need for testing services
- Limited competition in these specific verticals
- Strong B2B lead generation potential

**Priority Industries** (Q4 2025 - Q1 2026):
1. **Hydrogen Infrastructure Testing**
   - Standards: ASME, ISO, DOT
   - Services: Pressure vessels, pipelines, storage systems
   - Target: Energy transition companies, H2 producers

2. **Biotech/Pharma/Life Sciences Testing**
   - Standards: cGMP, FDA, ISO 13485
   - Services: Laboratory testing, clinical trials, quality control
   - Target: Biotech startups, pharmaceutical companies, research labs

**Future Expansion** (Q2 2026+):
- Environmental testing (already have 14 listings)
- Materials testing (already have 41 listings)
- Oil & Gas (legacy focus, maintenance mode)

---

## Agent Instructions

### When Working on Niche-Specific Tasks:

1. **Check the niche directory first** for existing documentation and learnings
2. **Save session notes to the appropriate niche directory** (not root)
3. **Tag learnings** with both "TSTR.site" and the niche (e.g., "hydrogen", "biotech")
4. **Reference previous work** from niche directories to avoid duplication

### Directory Usage Patterns:

**Root Directory**: Project-wide documentation (TSTR.md, PROJECT_STATUS.md, etc.)
**Niche Directories**: Industry-specific implementations, learnings, and resources

### When Creating New Verticals:

Follow the established pattern:
```
/[Niche Name] Directory/
  ├── README_[NICHE]_WORKFLOW.md
  ├── [NICHE]_LISTINGS_SUMMARY.md
  ├── Implementation notes
  ├── Session handoffs
  └── Scripts/utilities
```

---

## Files to Update

Agents should update these files to reflect niche-specific progress:

1. **PROJECT_STATUS.md** - Overall listing counts by niche
2. **TSTR.md** - Priority updates when niche focus changes
3. **Niche Directory READMEs** - Workflow and implementation details

---

## Continuity System Integration

### Recording Learnings:

When recording niche-specific learnings:
```python
add_learning(
    "Your learning here",
    "gotcha",  # or pattern, optimization, security
    confidence=5,
    tags=["TSTR.site", "hydrogen", "specific-tech"]  # or "biotech"
)
```

### Tracking Tasks:

Prefix niche-specific tasks with the niche name:
```python
add_task(
    "TSTR.site", 
    "[Hydrogen] Task description", 
    assigned_to="claude"
)
```

---

**Why This Matters**:
- **Focus**: Prevents scope creep by organizing work by vertical
- **Efficiency**: Agents can quickly find niche-specific context
- **Knowledge Transfer**: Session learnings preserved in relevant locations
- **Scalability**: Clean pattern for adding new niches

---

**Last Updated**: 2025-11-22
**Applies To**: All agents (Claude, Gemini, etc.)
