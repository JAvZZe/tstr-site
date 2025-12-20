# 🚀 AGENT QUICK REFERENCE CARD

**For**: All AI Agents (CASCADE, CURSOR, etc.)  
**Print This**: Keep handy for every session

---

## 🚨 CRITICAL FIRST STEP

```bash
# ⚠️ MANDATORY: Global bootstrap FIRST
cd "/media/al/AI_DATA/AI_PROJECTS_SPACE" && ./bootstrap_global.sh
```

---

## ⚡ PROJECT SESSION PROTOCOL

```bash
# 1. Global bootstrap (above - required)
# 2. Project bootstrap
./bootstrap.sh TSTR.site

# 3. Read current state
PROJECT_STATUS.md

# 4. Check recent context
handoff_core.md (last 2-3 sessions)

# 5. Understand request
User's actual request

# 6. Do work
Make changes, test, deploy

# 7. Update THIS
PROJECT_STATUS.md (always!)

# 8. Log session
handoff_core.md (append)
```

---

## 📚 DOCUMENT PRIORITY

```
1. PROJECT_STATUS.md       ← SINGLE SOURCE OF TRUTH
2. PROJECT_REFERENCE.md    ← Technical details
3. AGENT_PROTOCOL.md       ← How to work
4. handoff_core.md         ← Session history
5. Everything else         ← Context & guides
```

---

## 🔗 KEY LINKS

**Google Cloud**:
- Console: https://console.cloud.google.com
- Project: `business-directory-app-8888888`
- Functions: https://console.cloud.google.com/functions/list?project=business-directory-app-8888888
- Scheduler: https://console.cloud.google.com/cloudscheduler?project=business-directory-app-8888888

**Supabase**:
- Dashboard: https://supabase.com/dashboard/project/haimjeaetrsaauitrhfy

---

## 💰 CURRENT COSTS (Oct 16, 2025)

```
Cloud Functions:   $0.00  (FREE tier)
Cloud Scheduler:   $0.90  (3 jobs)
Storage/Network:   $0.14
─────────────────────────
TOTAL:            $1.04/month
```

---

## ✅ DEPLOYED FUNCTIONS

```
1. tstr-scraper-primary
   URL: https://us-central1-business-directory-app-8888888.cloudfunctions.net/tstr-scraper-primary
   Schedule: Every 3 days @ 2am Singapore

2. tstr-scraper-secondary
   URL: https://us-central1-business-directory-app-8888888.cloudfunctions.net/tstr-scraper-secondary
   Schedule: Weekly (Sunday) @ 3am Singapore

3. tstr-cleanup
   URL: https://us-central1-business-directory-app-8888888.cloudfunctions.net/tstr-cleanup
   Schedule: Monthly (1st) @ 4am Singapore
```

---

## 🔧 QUICK COMMANDS

```bash
# List functions
gcloud functions list --project=business-directory-app-8888888

# List schedules
gcloud scheduler jobs list --location=us-central1

# View logs
gcloud functions logs read tstr-scraper-primary

# Test function
curl [function-url]

# Run schedule manually
gcloud scheduler jobs run tstr-primary-scraper --location=us-central1
```

---

## 📝 UPDATE TEMPLATE

```markdown
**Last Updated**: October XX, 2025 HH:MM UTC
**Updated By**: [YOUR_AGENT_NAME]
**Changes**: 
- What you deployed/changed
- Impact on costs (if any)
- New status/URLs
```

---

## ⚠️ CRITICAL RULES

```
1. ALWAYS read PROJECT_STATUS.md first
2. ALWAYS update PROJECT_STATUS.md after changes
3. NEVER edit past session logs
4. NEVER guess at costs - verify
5. NEVER deploy without testing
6. ALWAYS timestamp updates
7. ALWAYS sign with your agent name
```

---

## 📊 STATUS CODES

```
✅ OPERATIONAL    - Working in production
🔄 IN PROGRESS    - Being deployed/developed
⏸️ PAUSED         - Temporarily stopped
❌ FAILED         - Broken/not working
🔄 PLANNED        - Not started yet
⚠️ WARNING        - Needs attention
```

---

## 🎯 PENDING TASKS (Current)

```
High Priority:
- [ ] Deploy Astro website to Netlify
- [ ] Connect domain (tstr.site)
- [ ] Test first automated scrape

Medium Priority:
- [ ] Add more categories
- [ ] Expand regions
- [ ] Setup alerts

Low Priority:
- [ ] Fix 1 invalid URL
- [ ] Add analytics
```

---

## 🔍 VERIFICATION CHECKLIST

Before marking ✅:
- [ ] Tested manually
- [ ] No errors in logs
- [ ] Cost documented
- [ ] URLs work
- [ ] PROJECT_STATUS.md updated
- [ ] handoff_core.md logged

---

## 💡 TIPS

- **Before deploying**: Check PROJECT_STATUS.md for conflicts
- **After deploying**: Update costs immediately
- **When stuck**: Check handoff_core.md for context
- **When unsure**: Ask user, don't guess
- **Save time**: Use existing deployment scripts

---

## 🚨 IF SOMETHING BREAKS

```
1. Check logs
   gcloud functions logs read [function-name]

2. Verify deployment
   gcloud functions describe [function-name]

3. Test endpoint
   curl [function-url]

4. Add to Known Issues in PROJECT_STATUS.md

5. Alert user

6. Plan fix
```

---

## 📞 HELP

- Full Protocol: `AGENT_PROTOCOL.md`
- Project Details: `PROJECT_REFERENCE.md`
- User Guide: `EXECUTIVE_SUMMARY.md`
- Technical Docs: `CLOUD_AUTOMATION_SOLUTION.md`

---

**Remember**: 
> "Read First, Update After, Document Always"

**Version**: 1.0  
**Last Updated**: Oct 16, 2025
