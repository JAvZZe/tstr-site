# Token Management Protocol - ALL AGENTS

**CRITICAL REQUIREMENT**: All agents MUST monitor token usage and complete handoffs before exhaustion.

---

## ⚠️ Why This Is Critical

### The Problem
**Handoffs require tokens to execute.**

If an agent runs out of tokens mid-handoff:
- ❌ Context is lost
- ❌ Handoff documentation incomplete
- ❌ Next agent starts blind
- ❌ Work must be reconstructed from git history
- ❌ Time and money wasted

### The Solution
**Plan handoffs proactively at 70% token usage.**

Reserve 10-15% tokens (20-30K for CASCADE) for the handoff process itself.

---

## 📊 Universal Token Thresholds

| Token % | Status | Action Required | Timeline |
|---------|--------|----------------|----------|
| **0-50%** | 🟢 Green | Normal operation | Continue work |
| **50-70%** | 🟡 Yellow | Monitor closely | Plan ahead |
| **70-85%** | 🟠 Orange | **BEGIN HANDOFF** | Start within 30 min |
| **85-90%** | 🔴 Red | **COMPLETE HANDOFF NOW** | Finish within 15 min |
| **90%+** | 🚨 Emergency | **IMMEDIATE HANDOFF** | Stop all work |

---

## 🎯 Agent-Specific Budgets

### CASCADE (Windsurf IDE)
- **Total Budget**: 200,000 tokens
- **Green Zone**: 0 - 100K (0-50%)
- **Yellow Zone**: 100K - 140K (50-70%)
- **Orange Zone**: 140K - 170K (70-85%) ⚠️ **BEGIN HANDOFF**
- **Red Zone**: 170K - 180K (85-90%) 🔴 **COMPLETE NOW**
- **Emergency**: 180K+ (90%+) 🚨 **STOP EVERYTHING**

### Claude Code CLI
- **Total Budget**: ~100,000 tokens (estimated)
- **Green Zone**: 0 - 50K (0-50%)
- **Yellow Zone**: 50K - 70K (50-70%)
- **Orange Zone**: 70K - 85K (70-85%) ⚠️ **BEGIN HANDOFF**
- **Red Zone**: 85K - 90K (85-90%) 🔴 **COMPLETE NOW**
- **Emergency**: 90K+ (90%+) 🚨 **STOP EVERYTHING**

### Gemini CLI
- **Total Budget**: ~50,000 tokens (estimated)
- **Green Zone**: 0 - 25K (0-50%)
- **Yellow Zone**: 25K - 35K (50-70%)
- **Orange Zone**: 35K - 42.5K (70-85%) ⚠️ **BEGIN HANDOFF**
- **Red Zone**: 42.5K - 45K (85-90%) 🔴 **COMPLETE NOW**
- **Emergency**: 45K+ (90%+) 🚨 **STOP EVERYTHING**

---

## 📋 Token Monitoring Checklist

### Every 30 Minutes (Required)
- [ ] Check platform token counter
- [ ] Update `.env.[agentname]` with `SESSION_TOKEN_USAGE`
- [ ] Calculate percentage: `(current / budget) * 100`
- [ ] Update `.env.[agentname]` with `SESSION_TOKEN_PERCENTAGE`
- [ ] If > 70%, trigger handoff protocol

### Real-Time Indicators
**Watch for these signs of high token usage:**
- Multiple large file reads (>1000 lines each)
- Complex reasoning chains (back-and-forth troubleshooting)
- Long error messages and stack traces
- Extensive code generation
- Multiple iterations on same problem

---

## 🚨 Handoff Protocol by Zone

### 🟠 Orange Zone (70-85%): BEGIN HANDOFF

**Immediate Actions**:
1. ⏸️ Pause starting new tasks
2. ✅ Complete current task if < 15 minutes
3. 💾 Commit all working code immediately
4. 📝 Update `handoff_core.md` with current state
5. 🎯 Identify next agent for handoff
6. 📄 Begin documenting context

**Time Allocation**:
- Complete current work: Max 15 minutes
- Documentation: 10-15 minutes
- Handoff execution: 5-10 minutes
- **Total**: 30-40 minutes within 15% token buffer

### 🔴 Red Zone (85-90%): COMPLETE HANDOFF NOW

**Critical Actions**:
1. 🛑 **STOP all new work immediately**
2. 💾 Commit any uncommitted changes
3. 📝 Complete handoff documentation (minimal if needed)
4. 🏷️ Execute handoff commit
5. 📋 Update all identity files
6. ✅ Verify handoff complete
7. 🚀 Hand off to next agent

**Time Limit**: Must complete within 10-15 minutes

### 🚨 Emergency Zone (90%+): IMMEDIATE HANDOFF

**Emergency Protocol**:
1. **STOP EVERYTHING immediately**
2. Quick commit: `[AGENT] EMERGENCY HANDOFF - Token limit`
3. Minimal handoff_core.md update:
   ```markdown
   ## EMERGENCY HANDOFF - [TIMESTAMP]
   From: [AGENT] (90%+ tokens)
   Current task: [Brief description]
   Status: [Partial/Complete]
   CRITICAL next actions:
   1. [Most urgent]
   2. [Second priority]
   3. [Third priority]
   Files touched: [list]
   ```
4. Update `.env.[agentname]` with final stats
5. **IMMEDIATE** handoff to next agent

**Time Limit**: 5 minutes maximum

---

## 💰 Handoff Cost Breakdown

### Documentation Updates (~5-10K tokens)
- `handoff_core.md` session log: 2-3K
- `.env.[agentname]` final stats: 0.5K
- `[AGENTNAME]_IDENTITY.md` update: 1-2K
- Handoff commit message: 0.5-1K
- Context documentation: 2-4K

### Total Reserve Needed
- **Minimum**: 5K tokens (emergency handoff)
- **Recommended**: 10K tokens (proper handoff)
- **Comfortable**: 15K tokens (thorough handoff)

---

## 📐 Calculating Token Usage

### Approximations
- **1 token** ≈ 4 characters (English text)
- **1 token** ≈ 0.75 words (average)
- **Message** (typical): 500-2000 tokens
- **File read** (100 lines): 300-500 tokens
- **File read** (1000 lines): 3-5K tokens
- **Code generation** (50 lines): 500-1000 tokens
- **Complex reasoning** (debugging): 5-10K tokens per cycle

### Tracking Tools
1. **Platform Counter**: Most reliable (if available)
2. **Message History**: Count messages × average tokens
3. **File Operations**: Track large reads (>1000 lines)
4. **Estimate**: When unsure, overestimate

---

## ✅ Best Practices

### Do's ✅
- ✅ Check tokens every 30 minutes
- ✅ Update `.env.[agentname]` regularly
- ✅ Start handoff at 70%
- ✅ Reserve 10-15% for handoff
- ✅ Commit frequently during work
- ✅ Document as you go

### Don'ts ❌
- ❌ Never exceed 90% tokens
- ❌ Don't start new tasks at 70%+
- ❌ Don't assume you have tokens left
- ❌ Don't skip updating token stats
- ❌ Don't hand off without documentation
- ❌ Don't leave uncommitted changes

---

## 🎯 Example Scenarios

### Scenario 1: Smooth Handoff (Ideal)
```
Time 0:00 - Start session: 0K tokens (0%)
Time 1:30 - Check: 60K tokens (30%) - Continue
Time 3:00 - Check: 120K tokens (60%) - Monitor
Time 4:00 - Check: 145K tokens (72%) - BEGIN HANDOFF
Time 4:15 - Complete task, commit code
Time 4:30 - Update documentation
Time 4:40 - Execute handoff commit
Time 4:45 - Handoff complete: 165K tokens (82%)
✅ Success: 35K tokens (17.5%) remaining
```

### Scenario 2: Late Handoff (Risky)
```
Time 0:00 - Start: 0K tokens (0%)
Time 3:00 - Check: 150K tokens (75%) - Should handoff
Time 3:15 - Continue working (MISTAKE)
Time 4:00 - Check: 175K tokens (87%) - CRITICAL
Time 4:05 - Rush handoff, incomplete docs
Time 4:10 - Handoff barely complete: 188K tokens (94%)
⚠️ Warning: Only 12K tokens left, risky
```

### Scenario 3: Token Exhaustion (Failed)
```
Time 0:00 - Start: 0K tokens (0%)
Time 4:00 - Check: 180K tokens (90%) - EMERGENCY
Time 4:05 - Begin handoff, too late
Time 4:08 - Mid-handoff: 195K tokens (97.5%)
Time 4:10 - Token limit reached during documentation
❌ FAILED: Handoff incomplete, context lost
```

---

## 📞 Emergency Contacts

**If Token Exhaustion Occurs**:
1. Check git history: `git log -n 10 --oneline`
2. Read last commit messages
3. Check `.env.[agentname]` for session stats
4. Read `[AGENTNAME]_IDENTITY.md` for actions taken
5. Review `handoff_core.md` session log

**Next Agent Should**:
1. Reconstruct context from git + docs
2. Continue from last known good state
3. Add note to handoff_core.md about recovery
4. Learn from incident to prevent recurrence

---

## 📊 Token Tracking Template

**Add to your `.env.[agentname]`**:

```bash
# Token tracking (update every 30 min)
SESSION_TOKEN_USAGE=80000
SESSION_TOKEN_PERCENTAGE=40.0
SESSION_TOKEN_REMAINING=120000
SESSION_TOKENS_UNTIL_HANDOFF=60000  # 70% threshold - current

# Calculated thresholds
TOKEN_HANDOFF_AT=140000   # 70%
TOKEN_CRITICAL_AT=170000  # 85%
TOKEN_EMERGENCY_AT=180000 # 90%
```

---

## 🎓 Training: Token Awareness

### Learn to Estimate
**High-token operations**:
- Reading large files (>1000 lines)
- Complex debugging sessions
- Multiple iterations on same problem
- Generating extensive code
- Analyzing stack traces

**Low-token operations**:
- Simple file edits
- Running commands
- Reading small files (<100 lines)
- Simple reasoning
- Quick commits

### Develop Intuition
After several sessions, you'll develop a sense of:
- How fast you consume tokens
- Which tasks are token-heavy
- When to check your usage
- When to trigger handoff

---

## 📋 Quick Reference Card

**Print or bookmark this**:

| Token % | Action |
|---------|--------|
| 0-50% | ✅ Work normally |
| 50-70% | 👀 Monitor closely |
| 70% | 🟠 Begin handoff prep |
| 85% | 🔴 Complete handoff now |
| 90% | 🚨 Emergency stop |

**Check tokens every 30 minutes**  
**Start handoff at 70%**  
**Reserve 10% for handoff**

---

**This protocol is MANDATORY for all agents. Violations result in lost context and wasted resources.**

**Last Updated**: 2025-10-15 18:08 UTC  
**Version**: 1.0  
**Maintained by**: CASCADE (windsurf-albert-tstr)
