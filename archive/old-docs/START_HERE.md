# 🚀 START HERE - TSTR.SITE

**Last Updated**: October 17, 2025  
**For**: All AI Agents (Claude Desktop, Claude Code CLI, Gemini CLI)

---

## 📖 WHAT TO READ (IN ORDER)

### **1️⃣ ALWAYS READ FIRST** ⭐
- [`PROJECT_STATUS.md`](PROJECT_STATUS.md) - Current system state (SINGLE SOURCE OF TRUTH)

### **2️⃣ READ FOR CONTEXT**
- [`DEPLOYMENT_READY_SUMMARY.md`](DEPLOYMENT_READY_SUMMARY.md) - What's deployed, what's next
- [`handoff_core.md`](handoff_core.md) - Recent session history (last 2-3 sessions)

### **3️⃣ READ IF NEEDED**
- [`AGENT_PROTOCOL.md`](AGENT_PROTOCOL.md) - Multi-agent coordination rules
- [`AGENT_QUICK_REFERENCE.md`](AGENT_QUICK_REFERENCE.md) - Commands cheat sheet
- [`Tstr.site Objectives and Context.docx`](Tstr.site%20Objectives%20and%20Context.docx) - Business goals

---

## 🎯 CURRENT PROJECT STATE

**System Status**: ✅ Backend automated, ⏳ Frontend needs deployment

### What's LIVE:
- ✅ 3 Cloud Functions deployed (scrapers + cleanup)
- ✅ Automated scheduling (every 3 days @ 2am Singapore)
- ✅ Database operational (19 verified listings)
- ✅ URL validation (95% success rate)

### What's PENDING:
- ⏳ Deploy Astro website to Netlify
- ⏳ Setup auto-rebuild webhook
- ⏳ Connect custom domain (tstr.site)

**Cost**: $1.04/month ✅

---

## 🛠️ QUICK ACTIONS

### Check Status
```bash
# View deployment status
cat DEPLOYMENT_READY_SUMMARY.md

# Check latest work
tail -100 handoff_core.md
```

### Deploy Website (Next Step)
```bash
# Follow this guide
cat DEPLOY_NOW.md
```

### Work on Project
```bash
# Frontend
cd web/tstr-frontend

# Automation scripts
cd web/tstr-automation
```

---

## 🚨 IMPORTANT RULES

1. **Always read PROJECT_STATUS.md FIRST**
2. **Update PROJECT_STATUS.md after changes**
3. **Log sessions in handoff_core.md**
4. **Keep costs documented**
5. **Test before deploying**

---

## 📞 NEED HELP?

- **Technical**: Read `PROJECT_REFERENCE.md`
- **Deployment**: Read `DEPLOY_NOW.md`
- **Multi-agent**: Read `AGENT_PROTOCOL.md`
- **Quick commands**: Read `AGENT_QUICK_REFERENCE.md`

---

**Remember**: Read first, act second, document after! ✅
