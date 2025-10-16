# 🤖 AGENT PROTOCOL - Multi-Agent Best Practices

**Purpose**: Guidelines for multiple AI agents working on TSTR.SITE  
**Applies To**: CASCADE, CURSOR, and any future agents  
**Status**: Active Protocol

---

## 📋 CORE PRINCIPLE

**"Read First, Update After, Document Always"**

Every agent must:
1. ✅ Read `PROJECT_STATUS.md` FIRST
2. ✅ Make changes
3. ✅ Update `PROJECT_STATUS.md` AFTER
4. ✅ Log session in `handoff_core.md`

---

## 📚 DOCUMENT HIERARCHY

### **Tier 1: Single Source of Truth**
```
PROJECT_STATUS.md
├─ Current infrastructure state
├─ Deployed functions & URLs
├─ Costs (always current)
├─ Pending tasks
└─ Known issues
```

**Rule**: This is ALWAYS the most current. Trust it above all else.

### **Tier 2: Technical Reference**
```
PROJECT_REFERENCE.md
├─ Technology stack details
├─ Code structure
├─ API documentation
└─ Architecture decisions
```

**Rule**: Update when stack/architecture changes.

### **Tier 3: Strategy & Plans**
```
CLOUD_AUTOMATION_SOLUTION.md
SCHEDULING_STRATEGY.md
URL_VALIDATION_LIVE.md
```

**Rule**: Reference for "why" decisions were made.

### **Tier 4: Session History**
```
handoff_core.md
SESSION_SUMMARY_*.md
```

**Rule**: Append-only logs. Never edit past sessions.

### **Tier 5: User-Facing**
```
EXECUTIVE_SUMMARY.md
QUICK_START.md
STATUS.txt
```

**Rule**: Update when major features go live.

---

## 🔄 AGENT WORKFLOW

### **Starting a New Session**

```
1. Read PROJECT_STATUS.md
   └─ Check current status
   └─ Review pending tasks
   └─ Note known issues

2. Read user request
   └─ Understand goal
   └─ Check if it conflicts with current state

3. Check handoff_core.md (last 2-3 sessions)
   └─ Understand recent context
   └─ Avoid repeating work

4. Execute task
   └─ Make changes
   └─ Test thoroughly

5. Update PROJECT_STATUS.md
   └─ Update "Last Updated" timestamp
   └─ Update "Updated By" field
   └─ Modify affected sections

6. Log in handoff_core.md
   └─ Add session summary
   └─ Note what was changed
```

### **Making Infrastructure Changes**

**Before deployment**:
```bash
# 1. Check current state
cat PROJECT_STATUS.md

# 2. Verify costs won't change drastically
# 3. Ensure no conflicts with scheduled jobs
# 4. Plan rollback strategy
```

**After deployment**:
```markdown
Update PROJECT_STATUS.md:
- Deployment timestamps
- New URLs/endpoints
- Updated costs
- Status changes (🔄 → ✅)
```

---

## 💰 COST TRACKING PROTOCOL

### **Always Update When**:
- Deploying new cloud resources
- Changing tier/plan
- Adding scheduled jobs
- Scaling resources

### **Cost Update Format**:
```markdown
| Service | Usage | Cost | Status |
|---------|-------|------|--------|
| New Resource | Details | $X.XX | ACTIVE |
```

### **Monthly Review**:
- First of every month
- Compare actual vs projected
- Update projections
- Alert user if >20% variance

---

## 🚨 CONFLICT RESOLUTION

### **If Two Agents Update Simultaneously**:

1. **Check timestamps**
   - Most recent wins
   
2. **Merge changes if possible**
   - Both agents' work may be valid
   
3. **Ask user if unclear**
   - Don't guess
   
4. **Document in handoff_core.md**
   - Note the conflict
   - Explain resolution

### **If Current State ≠ Documentation**:

1. **Verify actual state**
   ```bash
   gcloud functions list
   gcloud scheduler jobs list
   ```

2. **Update documentation to match reality**
   
3. **Add to "Known Issues" if problem exists**

4. **Alert user to discrepancy**

---

## 📝 UPDATE TEMPLATES

### **After Deployment**:
```markdown
**Last Updated**: October XX, 2025 HH:MM UTC
**Updated By**: [AGENT_NAME]
**Changes**: 
- Deployed [function/service name]
- Updated costs: +$X.XX/month
- New endpoint: [URL]
- Status: [component] → ✅ OPERATIONAL
```

### **After Bug Fix**:
```markdown
**Last Updated**: October XX, 2025 HH:MM UTC
**Updated By**: [AGENT_NAME]
**Changes**: 
- Fixed: [issue description]
- Affected: [component names]
- Resolved Issues: Remove from Known Issues section
```

### **After Configuration Change**:
```markdown
**Last Updated**: October XX, 2025 HH:MM UTC
**Updated By**: [AGENT_NAME]
**Changes**: 
- Modified: [config file/setting]
- Impact: [what this affects]
- Testing: [how it was verified]
```

---

## 🎯 SPECIFIC AGENT GUIDELINES

### **CASCADE (Windsurf)**
**Strengths**: Deployment, infrastructure, debugging  
**Responsibilities**:
- Cloud deployments
- Infrastructure changes
- Cost tracking
- Technical documentation

**Always update**:
- `PROJECT_STATUS.md` after deployments
- `handoff_core.md` with session logs
- Cost breakdowns

### **CURSOR (VS Code Agent)**
**Strengths**: Code editing, refactoring, local development  
**Responsibilities**:
- Code improvements
- Local testing
- Documentation updates
- Code review

**Always update**:
- `PROJECT_STATUS.md` if code structure changes
- `PROJECT_REFERENCE.md` for architecture changes

### **Future Agents**
**First Task**: Read this document + `PROJECT_STATUS.md`  
**Protocol**: Follow workflows above  
**Questions**: Check handoff_core.md for context

---

## 📊 STATUS INDICATORS

Use consistent status indicators:

```
✅ OPERATIONAL / DEPLOYED / COMPLETE
🔄 IN PROGRESS / PENDING / PARTIAL
⏸️ PAUSED / ON HOLD
❌ FAILED / BROKEN / DEPRECATED
🔄 PLANNED / SCHEDULED
⚠️ WARNING / NEEDS ATTENTION
```

---

## 🔍 VERIFICATION CHECKLIST

Before marking anything as ✅ OPERATIONAL:

- [ ] Deployed successfully
- [ ] Tested manually
- [ ] Logs show no errors
- [ ] Costs documented
- [ ] URLs/endpoints work
- [ ] Documentation updated
- [ ] User informed (if major)

---

## 🚀 DEPLOYMENT SAFETY

### **Pre-Deployment**:
```bash
# 1. Verify current state
gcloud config get-value project
gcloud functions list

# 2. Test locally if possible
python main.py

# 3. Check costs
gcloud billing accounts list
```

### **During Deployment**:
```bash
# Use --quiet for automation
# Log output to file
# Monitor for errors
```

### **Post-Deployment**:
```bash
# 1. Verify function deployed
gcloud functions describe [name]

# 2. Test endpoint
curl [function-url]

# 3. Check logs
gcloud functions logs read [name]

# 4. Update PROJECT_STATUS.md
```

---

## 📅 REGULAR MAINTENANCE

### **Daily** (Automated):
- Cloud Scheduler runs scrapers
- Logs accumulated
- (No agent action needed)

### **Weekly** (Agent Check):
- Review error logs
- Check cost drift
- Verify scheduled jobs ran

### **Monthly** (Agent Update):
- Update cost actual vs projected
- Review and archive old session logs
- Clean up temporary files
- Update projections

---

## 🎓 BEST PRACTICES

### **DO**:
✅ Read before writing  
✅ Update after deploying  
✅ Document all changes  
✅ Test before deploying  
✅ Keep costs current  
✅ Use consistent formatting  
✅ Timestamp all updates  
✅ Sign updates with agent name  

### **DON'T**:
❌ Assume documentation is current  
❌ Deploy without testing  
❌ Change infrastructure without documenting  
❌ Edit past session logs  
❌ Guess at costs  
❌ Leave status as "🔄" indefinitely  
❌ Skip updates "just this once"  

---

## 🔧 QUICK COMMANDS

### **Check Current State**:
```bash
# Functions
gcloud functions list --project=business-directory-app-8888888

# Schedules
gcloud scheduler jobs list --location=us-central1

# Costs (requires billing export setup)
gcloud billing projects describe business-directory-app-8888888
```

### **Update Documentation**:
```bash
# Edit PROJECT_STATUS.md
code PROJECT_STATUS.md

# Append to handoff_core.md
echo "Session update..." >> handoff_core.md
```

---

## 🎯 SUMMARY

**The Golden Rule**: 
> If it's deployed or changed, it MUST be in PROJECT_STATUS.md

**The Protocol**:
1. Read PROJECT_STATUS.md first
2. Make your changes
3. Update PROJECT_STATUS.md immediately
4. Log in handoff_core.md
5. Test your updates

**The Promise**:
> Every agent can trust PROJECT_STATUS.md as the single source of truth

---

**This protocol ensures**:
- ✅ No conflicting changes
- ✅ Always current documentation
- ✅ Smooth agent handoffs
- ✅ Clear audit trail
- ✅ Cost transparency
- ✅ User confidence

---

**Version**: 1.0.0  
**Effective**: October 16, 2025  
**Review**: Monthly or as needed
