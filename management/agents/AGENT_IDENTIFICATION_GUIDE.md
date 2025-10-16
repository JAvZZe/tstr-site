# Agent Identification Guide

**Purpose**: Ensure all agents properly identify themselves in commits, handoffs, and file changes for clear audit trails and continuity.

---

## 🆔 Agent Identity Files

### Each Agent MUST Create Two Files:

#### 1. Agent Environment Config: `.env.[agentname]`
**Location**: Project root  
**Purpose**: Agent configuration and session tracking  
**Template**: See `.env.cascade` for reference

**Key Fields**:
```bash
AGENT_NAME="[AGENTNAME]"
AGENT_ACCOUNT="[platform-user-project]"  # e.g., windsurf-albert-tstr
AGENT_SESSION_ID="[YYYYMMDD-HHMMSS-agent]"
AGENT_USER="alber"
SESSION_TOKEN_USAGE=[current]
SESSION_FILES_EDITED=[count]
```

**Update Frequency**: Beginning and end of each session

#### 2. Agent Session Log: `management/agents/[AGENTNAME]_IDENTITY.md`
**Location**: `management/agents/`  
**Purpose**: Track agent activity and handoffs  
**Template**: See `management/agents/AGENT_TEMPLATE.md`

**Contents**:
- Current session details
- Actions taken
- Git activity
- Handoff history

**Update Frequency**: Real-time during session

---

## ✍️ Git Commit Signatures

### Standard Commits

**Format**:
```
[AGENTNAME] Brief description of change

Longer explanation if needed.

Agent: [Agent Full Name]
Account: [account-identifier]
Files: [list or count]
```

**Examples**:
```
[CASCADE] Fix Python dependencies in requirements.txt

Changed supabase-python to supabase to match PyPI package name.

Agent: CASCADE (Windsurf IDE)
Account: windsurf-albert-tstr
Files: requirements.txt
```

```
[GEMINI] Add CSV data validation script

Created utility to validate CSV format before import.

Agent: Gemini CLI
Account: gemini-albert-tstr
Files: validate_csv.py
```

### Handoff Commits

**Format**:
```
[AGENTFROM→AGENTTO] Handoff reason

Agent: [From Agent Name]
Account: [from-account]
Session: [session-id]
Handoff to: [To Agent Name]
Reason: [Brief explanation]
Token usage: [X/YK]
Files modified: [count]

Next actions:
1. [Action 1]
2. [Action 2]
3. [Action 3]
```

**Example**:
```
[CASCADE→CLAUDE] Hand off for architectural review

Agent: CASCADE (Windsurf IDE)
Account: windsurf-albert-tstr
Session: 20251015-150000-cascade
Handoff to: Claude Code CLI
Reason: Need architectural guidance on database schema refactor
Token usage: 180K/200K (90% - approaching limit)
Files modified: 12

Next actions:
1. Review database schema design
2. Recommend indexing strategy
3. Suggest query optimization
```

---

## 📝 File Edit Annotations

### For Markdown Files

**At Top of File**:
```markdown
<!-- 
Last edited: 2025-10-15 17:40 UTC
Editor: CASCADE (windsurf-albert-tstr)
Session: 20251015-150000-cascade
Changes: Added agent identification section
-->
```

### For Code Files (Python)

**At Top of File**:
```python
# Last edited: 2025-10-15 17:40 UTC
# Editor: CASCADE (windsurf-albert-tstr)
# Session: 20251015-150000-cascade
# Changes: Fixed Supabase connection string
```

### For Code Files (JavaScript/TypeScript)

**At Top of File**:
```javascript
/**
 * Last edited: 2025-10-15 17:40 UTC
 * Editor: CASCADE (windsurf-albert-tstr)
 * Session: 20251015-150000-cascade
 * Changes: Updated API endpoint configuration
 */
```

### For Significant Code Blocks

**Inline Comments**:
```python
# CASCADE 2025-10-15: Fixed location mapping logic
def map_location(csv_location):
    # Previous logic was case-sensitive
    return db_locations.get(csv_location.lower())
```

---

## 🔄 Handoff Documentation

### Update handoff_core.md

**Add Entry to Session Log**:
```markdown
### [TIMESTAMP] [FROM_AGENT] → [TO_AGENT]
**From Agent**: [Agent Name]
**From Account**: [account-id]
**To Agent**: [Agent Name]
**To Account**: [account-id]
**Session ID**: [session-id]
**Reason**: [Why handing off]
**State**: [Current system state]
**Next Actions**: 
1. [Action 1]
2. [Action 2]
3. [Action 3]
**Blockers**: [What's blocking progress]
**Context**: [Important background]
**Token Usage**: [X/Y (Z%)]
**Files Modified**: [count]
```

### Update Your Identity File

**Before Handing Off**:
1. Update `.env.[agentname]` with final session stats
2. Update `management/agents/[AGENTNAME]_IDENTITY.md`:
   - Mark session as completed
   - Add handoff entry to history
   - Update file counts and token usage
3. Commit all changes with handoff signature

---

## 🎯 Agent Account Naming Convention

**Format**: `[platform]-[user]-[project]`

**Examples**:
- `windsurf-albert-tstr` - CASCADE in Windsurf IDE
- `gemini-albert-tstr` - Gemini CLI
- `claude-albert-tstr` - Claude Code CLI
- `comet-albert-tstr` - Comet Assistant

**Consistency**: Use the same account identifier throughout entire project

---

## ✅ Checklist: Starting a Session

- [ ] Create `.env.[agentname]` if first time
- [ ] Create `management/agents/[AGENTNAME]_IDENTITY.md` if first time
- [ ] Update session start time in both files
- [ ] Read `handoff_core.md` for current state
- [ ] Note if received handoff from previous agent
- [ ] Set session ID: `YYYYMMDD-HHMMSS-agentname`

---

## ✅ Checklist: During Session

- [ ] Use `[AGENTNAME]` prefix in all commits
- [ ] Add agent signature to commit bodies
- [ ] Update file annotations when making significant changes
- [ ] Track actions in your identity file
- [ ] **Monitor token usage continuously**
- [ ] **Start handoff process at 70% token usage**
- [ ] **Complete handoff by 85% token usage**
- [ ] Never exceed 90% tokens - leave buffer for handoff
- [ ] Update token usage in identity file every 30 minutes

---

## ⚠️ CRITICAL: Token Management

### Token Budget Thresholds

**All agents MUST monitor token usage and proactively hand off before exhaustion.**

| Token Usage | Action Required | Urgency |
|-------------|----------------|----------|
| 0-50% | Normal operation | 🟢 Continue |
| 50-70% | Monitor closely, plan ahead | 🟡 Caution |
| 70-85% | **BEGIN HANDOFF IMMEDIATELY** | 🟠 Warning |
| 85-90% | Complete handoff NOW | 🔴 Critical |
| 90%+ | **EMERGENCY - Stop work, handoff incomplete docs** | 🚨 Emergency |

### Why This Matters

**The handoff process itself requires tokens:**
- Updating handoff_core.md: ~2-3K tokens
- Updating identity files: ~1-2K tokens
- Writing handoff commit: ~1K tokens
- Final documentation: ~2-3K tokens
- **Total handoff cost: ~5-10K tokens**

**If you run out mid-handoff, context is LOST.**

### Token Monitoring Protocol

**Every 30 Minutes**:
1. Check current token usage
2. Update `.env.[agentname]` SESSION_TOKEN_USAGE
3. Calculate percentage used
4. If > 70%, begin handoff preparation

**At 70% Tokens**:
1. Commit all working code immediately
2. Update handoff_core.md with current state
3. Identify next agent for handoff
4. Begin documenting context for handoff
5. Complete current task ONLY if < 15 minutes

**At 85% Tokens**:
1. STOP new work immediately
2. Complete handoff documentation
3. Execute handoff commit
4. Update all identity files
5. Hand off to next agent

**At 90% Tokens (Emergency)**:
1. **STOP EVERYTHING**
2. Quick handoff commit with: "[AGENT] EMERGENCY HANDOFF - Token limit"
3. Update handoff_core.md with minimal context
4. List critical next actions
5. Immediate handoff

### Agent-Specific Token Budgets

- **CASCADE (Windsurf)**: 200K tokens
  - Handoff threshold: 140K (70%)
  - Critical threshold: 170K (85%)
  - Emergency: 180K (90%)

- **Claude Code**: ~100K tokens (estimated)
  - Handoff threshold: 70K (70%)
  - Critical threshold: 85K (85%)
  - Emergency: 90K (90%)

- **Gemini**: ~50K tokens (estimated)
  - Handoff threshold: 35K (70%)
  - Critical threshold: 42.5K (85%)
  - Emergency: 45K (90%)

### Calculating Token Usage

**Approximation**:
- 1 token ≈ 4 characters
- Average message: 500-2000 tokens
- File read (1000 lines): ~3-5K tokens
- Complex reasoning: 5-10K tokens per cycle

**Tools**:
- Check your platform's token counter
- Update `.env.[agentname]` with actual usage
- Track in identity file

---

## ✅ Checklist: Ending a Session

- [ ] **Verify token usage < 85%** (leave room for handoff)
- [ ] Update `handoff_core.md` with current state
- [ ] Update `.env.[agentname]` with final stats (including token usage)
- [ ] Update `management/agents/[AGENTNAME]_IDENTITY.md`
- [ ] Commit all working code
- [ ] If handing off:
  - [ ] Use handoff commit format
  - [ ] Document in handoff_core.md
  - [ ] Update both identity files (yours and recipient's)
  - [ ] List next 3 priority actions clearly
  - [ ] **Confirm handoff completed before token exhaustion**

---

## 📊 Example Agent Directory Structure

```
management/
└── agents/
    ├── AGENT_IDENTIFICATION_GUIDE.md  # This file
    ├── AGENT_TEMPLATE.md               # Template for new agents
    ├── CASCADE_IDENTITY.md             # CASCADE session tracking
    ├── GEMINI_IDENTITY.md              # Gemini session tracking (when used)
    ├── CLAUDE_IDENTITY.md              # Claude Code tracking (when used)
    └── COMET_IDENTITY.md               # Comet tracking (when used)

# Root directory:
.env.cascade      # CASCADE config
.env.gemini       # Gemini config (when created)
.env.claude       # Claude config (when created)
.env.comet        # Comet config (when created)
```

---

## 🎓 Why This Matters

### Auditability
- Know who made what changes and when
- Track decision provenance
- Debug issues by understanding context

### Continuity
- New agent can quickly understand previous work
- Handoffs preserve context
- Session stats help optimize token usage

### Collaboration
- Multiple agents can work on same project
- Clear boundaries and responsibilities
- Avoid duplicate work

### Learning
- Track which agents are best for which tasks
- Optimize future task routing
- Improve handoff protocols

---

## 🔍 Quick Reference

| Situation | Action | Format |
|-----------|--------|--------|
| Regular commit | `[AGENTNAME] Description` | Standard |
| Handoff commit | `[FROM→TO] Reason` | Handoff |
| File annotation | Add comment header | Language-specific |
| Session start | Update identity files | Both .env and .md |
| Session end | Update stats | Token usage, file counts |
| Handoff received | Note in identity file | From agent, reason, context |
| Handoff given | Full handoff protocol | Update all docs |

---

**Maintained by**: CASCADE (windsurf-albert-tstr)  
**Last Updated**: 2025-10-15 17:40 UTC  
**Version**: 1.0  
**Next Review**: When new agent joins project
