# Test Supabase MCP - Quick Guide

> **Status**: Authentication complete, ready to test
> **Date**: 2025-11-20

---

## Quick Test Queries

Try these natural language queries with me (Claude):

### Schema Discovery
```
"Show me the schema for the listings table"
"What tables exist in the database?"
"List all columns in the listings table with their types"
```

### Data Queries
```
"How many listings are in the database?"
"Show me the first 5 listings"
"What categories exist in the listings?"
"How many pharmaceutical testing listings are there?"
```

### TypeScript Generation
```
"Generate TypeScript types for the listings table"
"Create types for all database tables"
```

### Analysis
```
"Which US states have the most testing laboratories?"
"Show me listings with missing website URLs"
"What's the most common category?"
```

---

## Expected Behavior

**If MCP Works**:
- I'll respond naturally with data/schema information
- Faster than manual SQL queries
- Can introspect database structure
- Can generate TypeScript types
- Token efficient (~70 tokens vs 200 for bash)

**If Still Having Issues**:
- I'll get 401 errors or timeout
- Will fall back to explaining the problem
- May need to update API keys manually

---

## Fallback: Update API Keys Manually

If MCP still fails, get fresh keys from Supabase:

1. Go to: https://supabase.com/dashboard/project/haimjeaetrsaauitrhfy
2. Settings → API → Copy "anon/public" key
3. Update these files:
   - `bruno/environments/production.bru`
   - `web/tstr-frontend/.env`
   - `web/tstr-automation/TSTR1.mcp.json`

---

## After Testing

Let me know what works/doesn't work, and I'll:
1. Document working examples in the skills guide
2. Update the MCP integration docs
3. Create usage patterns for future reference
4. Add to learnings database

---

**Ready when you are!** Just ask me any of the queries above.
