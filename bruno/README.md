# TSTR.site Bruno API Collection

> **Status**: Active - Bruno MCP installed for agent integration
> **Last Updated**: 2025-11-20
> **Purpose**: API repository, test automation, agent tools

---

## Quick Start

### For Humans (CLI)

```bash
# Test Supabase connection
bru run bruno/supabase/health/connection-test.bru --env production

# Run all health checks
bru run bruno/supabase/health/ --env production

# Get listings
bru run bruno/supabase/listings/get-all-listings.bru --env production
```

### For Agents (MCP)

**Installation** (already done):
```bash
droid mcp add bruno "npx -y @hungthai1401/bruno-mcp"
```

**Usage in conversation**:
- "Run the Supabase health checks"
- "Test the listings API endpoints"
- "Validate the database connection"

---

## Collection Structure

```
bruno/
├── bruno.json                      # Collection config
├── README.md                       # This file
├── environments/
│   ├── production.bru              # Live Supabase (keys included)
│   ├── local.bru                   # Dev environment
│   └── ci.bru                      # GitHub Actions
├── supabase/
│   ├── health/                     # Health checks (P0)
│   │   ├── connection-test.bru     # Basic connectivity
│   │   └── listings-count.bru      # Verify data exists
│   └── listings/                   # CRUD operations (P1)
│       ├── get-all-listings.bru    # Retrieve listings
│       └── get-by-category.bru     # Category filtering
├── infrastructure/                 # Infrastructure access info
│   └── oci-access.bru              # OCI SSH and scraper status
└── scrapers/                       # Future: scraper endpoints
```

---

## Environments

### Production
- **BASE_URL**: `https://haimjeaetrsaauitrhfy.supabase.co`
- **AUTH**: Supabase ANON_KEY (included in environment)
- **Usage**: Live API testing, health monitoring

### Local
- Same as production (no local Supabase instance)
- Use for development/testing without fear

### CI
- Used in GitHub Actions workflows
- Secrets loaded from repository secrets

---

## Current Collections

### Health Checks (Priority 0)

**connection-test.bru**
- Tests: Basic Supabase connectivity
- Expected: 200 OK
- Run: `bru run bruno/supabase/health/connection-test.bru --env production`

**listings-count.bru**
- Tests: Database has listing data
- Expected: At least 163 listings
- Run: `bru run bruno/supabase/health/listings-count.bru --env production`

### Listings API (Priority 1)

**get-all-listings.bru**
- Tests: Retrieve listings with pagination
- Expected: Array of 10 listings, required fields present
- Run: `bru run bruno/supabase/listings/get-all-listings.bru --env production`

**get-by-category.bru**
- Tests: Category filtering (Pharmaceutical)
- Expected: All results match category filter
- Run: `bru run bruno/supabase/listings/get-by-category.bru --env production`

### Infrastructure Access (Reference)

**oci-access.bru**
- **Purpose**: Reference collection for infrastructure access information
- **Contents**: SSH key paths, OCI instance details, scraper status checks
- **Note**: Contains access documentation, not executable tests
- **SSH Key Path**: `/media/al/69AD-FC41/AI_PROJECTS_ARCHIVE/Oracle_Cloud_Machines/avz_Oracle_Linux_9_pvt_ssh-key-2025-10-25.key`
- **OCI Instance**: `84.8.139.90` (Oracle Linux 9, Python 3.9.21)
- **Scraper Path**: `~/tstr-scraper/` on OCI instance

---

## Usage Patterns

### 1. Pre-Deployment Validation

```bash
# Before deploying scraper changes
bru run bruno/supabase/health/ --env production

# If all pass → safe to deploy
# If any fail → investigate before deploying
```

### 2. Post-Deployment Smoke Tests

```bash
# After scraper runs
bru run bruno/supabase/listings/ --env production

# Verify new data inserted correctly
```

### 3. Health Monitoring (Cron)

```bash
# On OCI instance, run daily
0 3 * * * cd /home/opc/tstr-site && bru run bruno/supabase/health/ --env production >> /var/log/api-health.log 2>&1
```

### 4. Agent Integration

```
User: "Check if the Supabase database is healthy"
Agent: [Runs bruno/supabase/health/ collection via MCP]
Agent: "✅ All health checks passed. 163 listings confirmed."
```

---

## Token Economics

**Bash approach**:
```bash
curl -H "apikey: $KEY" "$URL/rest/v1/listings?select=count" | jq
# Parse output, check status, validate response
# Cost: ~200 tokens per test
```

**Bruno MCP approach**:
```
[Agent calls mcp__bruno__run with collection path]
# Structured JSON response with test results
# Cost: ~70 tokens per test
```

**Savings**: 65% per API test

---

## Roadmap

### Phase 1: Critical (✅ Complete)
- [x] Basic structure
- [x] Environment setup
- [x] Health checks
- [x] Listings API basics
- [x] Bruno MCP installed

### Phase 2: High Value (Next)
- [ ] Validation collection (URL validity, data quality)
- [ ] Category-specific tests (all 4 categories)
- [ ] Location-based queries
- [ ] CI/CD integration (GitHub Actions)

### Phase 3: Enhancement (Future)
- [ ] Scraper endpoints
- [ ] External API monitoring
- [ ] Performance tests
- [ ] Load testing collections

---

## Secrets Management

**Included in environments**:
- `SUPABASE_ANON_KEY` - Safe to commit (public-facing key)

**Not committed** (use `vars:secret`):
- `SUPABASE_SERVICE_KEY` - Full database access
- Store locally or in CI secrets

**Security**:
- ANON_KEY has Row Level Security (RLS) restrictions
- SERVICE_ROLE_KEY bypasses RLS (dangerous!)
- Never expose SERVICE_ROLE_KEY in client code

---

## Troubleshooting

### Bruno CLI not found
```bash
npm install -g @usebruno/cli
bru --version
```

### Connection test fails
```bash
# Check Supabase is accessible
curl -I https://haimjeaetrsaauitrhfy.supabase.co/rest/v1/

# Verify ANON_KEY
echo $SUPABASE_ANON_KEY

# Check environment file syntax
cat bruno/environments/production.bru
```

### MCP not working for agents
```bash
# Verify MCP installed
droid mcp list

# Check MCP config
cat ~/.factory/mcp.json

# Reinstall if needed
droid mcp remove bruno
droid mcp add bruno "npx -y @hungthai1401/bruno-mcp"
```

---

## Related Documentation

- **Skills Guide**: `/media/al/AI_DATA/AI_PROJECTS_SPACE/SYSTEM/skills/bruno-api-management.md`
- **TSTR.site Main**: `../TSTR.md`
- **Project Status**: `../PROJECT_STATUS.md`
- **Bruno Docs**: https://docs.usebruno.com/
- **Bruno MCP**: https://github.com/hungthai1401/bruno-mcp

---

## Contact

For issues with:
- **Collection structure**: Update this README
- **Environment variables**: Edit `environments/*.bru` files
- **New collections**: Create `.bru` files, follow existing patterns
- **Agent integration**: See `SYSTEM/skills/bruno-api-management.md`

---

**Remember**: Bruno collections are executable documentation. Keep them up-to-date!
