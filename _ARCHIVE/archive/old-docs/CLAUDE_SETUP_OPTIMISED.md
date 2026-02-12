# 🎯 OPTIMISED CLAUDE SETUP - TSTR.SITE

**Date**: October 17, 2025  
**For**: Multi-agent continuity (Claude Desktop, Claude Code CLI, Gemini CLI)

---

## 🚀 IMMEDIATE SETUP (Do This Now)

### **Step 1: Load Core Documents**

In **Claude Desktop**, load these 3 documents:

1. ✅ `START_HERE.md` ← Navigation guide
2. ✅ `PROJECT_STATUS.md` ← Current state (ALWAYS)
3. ✅ `DEPLOYMENT_READY_SUMMARY.md` ← What's next

**Optional** (context-dependent):
- `Tstr.site Objectives and Context.docx` ← Business goals
- `Global Structure and payments` ← Architecture requirements

### **Step 2: Archive Old Docs**

Run this PowerShell command:
```powershell
cd "C:\Users\alber\OneDrive\Documents\.WORK\TSTR.site"
.\cleanup-docs.ps1
```

This moves 12+ completed task docs to `archive/completed-tasks/`

---

## 📋 DOCUMENT STRUCTURE (Optimised)

### **Tier 1: Always Load** ⭐
```
START_HERE.md              ← Read first! Navigation
PROJECT_STATUS.md          ← Single source of truth
DEPLOYMENT_READY_SUMMARY.md ← Current deployment state
```

### **Tier 2: Context Files**
```
handoff_core.md            ← Session history (recent)
AGENT_PROTOCOL.md          ← Multi-agent rules
Tstr.site Objectives...docx ← Business goals
```

### **Tier 3: Reference Files**
```
PROJECT_REFERENCE.md       ← Technical details
AGENT_QUICK_REFERENCE.md   ← Commands cheat sheet
DEPLOY_NOW.md              ← Deployment guide
```

### **Tier 4: Archived** (Don't load)
```
archive/completed-tasks/   ← Old session summaries
archive/completed-tasks/   ← Completed deployment docs
```

---

## 🤖 FOR CLAUDE CODE CLI

When using CLI, reference docs efficiently:

```bash
# Quick status check
cat START_HERE.md | head -50

# Current deployment state
cat DEPLOYMENT_READY_SUMMARY.md

# Check what's been done recently
tail -100 handoff_core.md

# Quick commands reference
cat AGENT_QUICK_REFERENCE.md
```

---

## 🔄 MULTI-AGENT WORKFLOW

### **Agent Handoff Protocol:**

1. **Before Starting**:
   ```bash
   # Read these 3 files
   cat START_HERE.md
   cat PROJECT_STATUS.md
   cat handoff_core.md | tail -200
   ```

2. **During Work**:
   - Make changes
   - Test thoroughly
   - Document as you go

3. **Before Finishing**:
   ```bash
   # Update status
   # (Edit PROJECT_STATUS.md)
   
   # Log session
   # (Append to handoff_core.md)
   ```

---

## 💾 MEMORY & STATE MANAGEMENT

### **Project State Location:**
- **Master**: `PROJECT_STATUS.md`
- **History**: `handoff_core.md`
- **Next steps**: `DEPLOYMENT_READY_SUMMARY.md`

### **What Each Agent Should Track:**
- ✅ Files created/modified
- ✅ Costs changed (if any)
- ✅ Deployment status updated
- ✅ Issues encountered
- ✅ Next actions identified

---

## 📊 TOKEN MANAGEMENT

### **For Claude Desktop:**
- **Load**: 3 core docs (~50K tokens)
- **Reserve**: Keep 40K for responses
- **Total budget**: 190K tokens

### **Efficient Reading Strategy:**
```bash
# Instead of loading full docs, use CLI:
cat PROJECT_STATUS.md | grep "Status"
cat handoff_core.md | tail -50
```

---

## 🎯 PARETO PRINCIPLE (80/20)

### **20% Docs = 80% Value:**
1. `PROJECT_STATUS.md` ← Tells you everything
2. `DEPLOYMENT_READY_SUMMARY.md` ← What to do next
3. `handoff_core.md` (last 100 lines) ← Recent context

**Everything else** = reference when needed

---

## ✅ OPTIMAL SETUP CHECKLIST

- [ ] Load 3 core docs in Claude Desktop
- [ ] Run `cleanup-docs.ps1` to archive old files
- [ ] Bookmark `START_HERE.md` location
- [ ] Test CLI access: `cat START_HERE.md`
- [ ] Configure Desktop Commander allowed directories
- [ ] Verify Git Bash / PowerShell access
- [ ] Test Google Cloud SDK access
- [ ] Confirm Gemini CLI available

---

## 🔧 DESKTOP COMMANDER SETUP

Current config shows:
```json
"allowedDirectories": []  ← Empty = full access
```

**Recommendation**: Leave as is (full access needed for project work)

---

## 📁 PROJECT PATHS

**Main project**:
```
C:\Users\alber\OneDrive\Documents\.WORK\TSTR.site
```

**Frontend**:
```
C:\Users\alber\OneDrive\Documents\.WORK\TSTR.site\web\tstr-frontend
```

**Automation**:
```
C:\Users\alber\OneDrive\Documents\.WORK\TSTR.site\web\tstr-automation
```

---

## 🚨 CRITICAL RULES

1. **Always read `START_HERE.md` first**
2. **Always check `PROJECT_STATUS.md` for current state**
3. **Always update `PROJECT_STATUS.md` after changes**
4. **Always log in `handoff_core.md` after session**
5. **Never load old session summaries unless debugging**

---

## 💡 PRO TIPS

### **For You (Non-Technical):**
- Start each session: "Read START_HERE.md and tell me current status"
- Check progress: "What's the current state according to PROJECT_STATUS.md?"
- Before decisions: "What does DEPLOYMENT_READY_SUMMARY.md say we should do next?"

### **For Agents:**
- Use CLI tools to save tokens (cat, grep, tail)
- Only load docs you actually need
- Update PROJECT_STATUS.md in same session as changes
- Keep handoff_core.md append-only (don't edit past entries)

---

## 🎊 RESULT

**Before**: 45+ markdown files, unclear which to load  
**After**: 3 core files, clear navigation, 12+ archived

**Token savings**: ~70K tokens (don't load irrelevant docs)  
**Clarity**: ⭐⭐⭐⭐⭐ (100% clear what to read)  
**Multi-agent continuity**: ✅ Optimised

---

**Next Step**: Load the 3 core docs and say "Let's continue the project!"
