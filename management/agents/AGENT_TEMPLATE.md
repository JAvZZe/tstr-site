# [AGENT NAME] Identity Template

**Copy this template when a new agent joins the project**

---

## Agent Information

**Agent Name**: [e.g., GEMINI, CLAUDE-CODE, COMET]  
**Platform**: [e.g., Gemini CLI, Claude Code CLI, Perplexity Browser]  
**Account**: [e.g., gemini-albert-tstr, claude-avztest8]  
**User**: alber  
**Project**: TSTR.directory
**Session Started**: [YYYY-MM-DD HH:MM UTC]

---

## Agent Signature

**Git Commits**:
```
[AGENTNAME] Description of change
```

**Handoffs**:
```
[AGENTNAME→RECIPIENT] Handoff to [agent name]
```

**File Edits**:
```
<!-- Edited by AGENTNAME (account-identifier) on YYYY-MM-DD -->
```

---

## Current Session

**Session ID**: [YYYYMMDD-HHMMSS-agentname]  
**Start Time**: [YYYY-MM-DD HH:MM UTC]  
**Token Budget**: [agent-specific]  
**Token Used**: [current / budget]  
**Status**: [Active/Paused/Completed]

### Actions This Session
1. [ ] Task 1
2. [ ] Task 2
3. [ ] Task 3

### Git Activity
**Commits Made**: 0  
**Files Modified**: 0

---

## Handoff History

### Received From
**Previous Agent**: [Agent name]  
**Handoff Time**: [timestamp]  
**Reason**: [why handed to this agent]  
**Context**: [brief summary]

### Handed Off To
**Next Agent**: [Agent name]  
**Handoff Time**: [timestamp]  
**Reason**: [why handing off]  
**Context**: [brief summary]

---

## Agent Config File

Located at: `.env.[agentname]`

Create with this structure:
```bash
# [AGENT NAME] Environment Configuration
AGENT_NAME="[AGENTNAME]"
AGENT_ACCOUNT="[account-identifier]"
AGENT_SESSION_ID="[session-id]"
AGENT_USER="alber"
# ... (see .env.cascade for full template)
```

---

## Notes

[Any agent-specific notes, preferences, or quirks]

---

**Last Updated**: [timestamp]  
**Updated By**: [agent name]  
**Next Update**: [End of session or specific milestone]
