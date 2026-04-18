# Supabase MCP Test Results - TSTR.site

> **Test Date**: 2025-11-20
> **Tested By**: Claude (Droid)
> **Project**: TSTR.site (haimjeaetrsaauitrhfy.supabase.co)
> **Status**: ⚠️ Configuration Valid, Authentication Failing

---

## Quick Summary

**What Works**:
- ✅ MCP configuration file exists and is properly formatted
- ✅ NPX available (v10.9.4)
- ✅ Supabase MCP package available
- ✅ Bruno CLI installed and functional

**What Doesn't Work**:
- ❌ API authentication (401 Unauthorized)
- ❌ Bruno health checks failing (same auth issue)
- ❌ Cannot test actual MCP functionality

**Root Cause**: Supabase project likely paused or API keys expired

---

## Test Results

### 1. Configuration Check ✅

**File**: `web/tstr-automation/TSTR1.mcp.json`

```json
{
  "mcpServers": {
    "supabase": {
      "command": "npx",
      "args": [
        "-y",
        "@supabase/mcp-server-supabase@latest",
        "--read-only",
        "--project-ref=haimjeaetrsaauitrhfy"
      ],
      "env": {
        "SUPABASE_ACCESS_TOKEN": "[REDACTED_SECRET]"
      }
    }
  }
}
```

**Result**: Properly formatted, ready to use

### 2. API Connection Test ❌

```bash
$ curl "https://haimjeaetrsaauitrhfy.supabase.co/rest/v1/listings?select=count" \
  -H "apikey: KEY" -H "Authorization: Bearer KEY"

{"message":"Invalid API key","hint":"Double check your Supabase `anon` or `service_role` API key."}
```

**HTTP Status**: 401 Unauthorized

### 3. Bruno Health Check ❌

```bash
$ bru run bruno/supabase/health/connection-test.bru --env production

AssertionError: expected 401 to equal 200
```

**Duration**: 91ms (fast response, but wrong auth)

---

## What Needs to Be Fixed

### Immediate Actions

1. **Check if Supabase project is paused**
   - Go to: https://supabase.com/dashboard/project/haimjeaetrsaauitrhfy
   - Look for "Project Paused" banner
   - Click "Resume Project" if paused

2. **Get fresh API keys**
   - Project Settings → API
   - Copy new "anon/public" key
   - Update in these files:
     - `bruno/environments/production.bru`
     - `web/tstr-frontend/.env`
     - `web/tstr-automation/TSTR1.mcp.json`

3. **Generate new personal access token**
   - Account Settings → Access Tokens
   - Create new token
   - Update `SUPABASE_ACCESS_TOKEN` in MCP config

4. **Test authentication**
   ```bash
   curl "https://haimjeaetrsaauitrhfy.supabase.co/rest/v1/listings?select=count" \
     -H "apikey: NEW_KEY" -H "Authorization: Bearer NEW_KEY"
   ```

---

## When to Use What

### Use Bruno CLI (Current Fallback)
- ✅ API endpoint testing
- ✅ Health checks
- ✅ CI/CD integration
- ✅ Regression testing
- 🎯 More deterministic

**Example**:
```bash
bru run bruno/supabase/health/ --env production
```

### Use Supabase MCP (After Auth Fixed)
- ✅ Database exploration
- ✅ Schema introspection
- ✅ TypeScript type generation
- ✅ Natural language queries
- 🎯 More conversational

**Example**:
```
User: "Show me the schema for the listings table"
Agent: [Uses MCP to query]
```

---

## Documentation Created

**Comprehensive Guide**: `/media/al/AI_DATA/AI_PROJECTS_SPACE/SYSTEM/skills/supabase-mcp-integration.md`

**Includes**:
- Installation methods (3 options)
- Configuration examples
- Credentials setup guide
- Test results (this document's details)
- Troubleshooting guide
- Security considerations
- Usage patterns
- Token economics
- Comparison with Bruno CLI

---

## Key Learnings

1. **Free tier projects pause automatically** after inactivity
2. **Always verify project status** before debugging credentials
3. **Test with curl first** to isolate auth issues
4. **Have multiple access methods** (MCP + Bruno + SQL)
5. **MCP is convenient but not production-critical** - keep fallbacks

---

## Next Steps

When resuming this work:

1. Check Supabase dashboard (project status)
2. Regenerate all credentials
3. Update all config files
4. Test with curl
5. Test with Bruno CLI
6. Try MCP integration
7. Update this document with results

---

**For Full Details**: See `/media/al/AI_DATA/AI_PROJECTS_SPACE/SYSTEM/skills/supabase-mcp-integration.md`

**Status**: Testing complete, awaiting credential refresh to validate full functionality
