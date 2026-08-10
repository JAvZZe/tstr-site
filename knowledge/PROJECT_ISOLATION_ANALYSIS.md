# Project Isolation Architecture Analysis & Recommendations

## Context
This document analyzes whether the TSTR.directory project (and other projects in AI_PROJECTS_SPACE) should use separate MuninnDB and SQLite instances per project to avoid cross-project contamination, or maintain the current shared-but-isolated architecture.

## Current Architecture Analysis

### What We Found:
1. **SQLite Databases**:
   - Central system database: `SYSTEM/state/project.db`
   - Project-specific ledgers: `SYSTEM/state/project_ledgers/` 
     - `tstr-site-working.db` (for TSTR.directory)
     - `ai-projects-space.db` (for system)
     - Other project databases as needed

2. **MuninnDB**:
   - Shared system-wide service running on `http://localhost:8750/mcp`
   - Referenced as the "primary memory system" with 65+ memories persisted
   - Accessible via `muninn-cli` tool system-wide
   - Uses tagging/scoping for project isolation

3. **Project-Specific Storage**:
   - Each project has its own memory directory (e.g., `tstr-site-working/memory/`)
   - Bootstrap process loads project-specific context and memories
   - Learning extraction examples show project-specific tagging

## Evaluation: Shared vs. Separate Instances

### Current Shared-but-Isolated Approach Benefits:
1. **Cross-Project Learning**: Valuable patterns and learnings can be shared across projects when appropriate
2. **Reduced Infrastructure Overhead**: One MuninnDB service to maintain vs. N instances
3. **Global Search Capability**: Ability to search memories across all projects
4. **Centralized Maintenance**: Backups, updates, monitoring in one place
5. **Designed for Isolation**: Uses tagging/scoping and project-specific ledgers to prevent bleed

### Current Approach Risks (Theoretical):
1. **Improper Tagging**: If memories aren't tagged correctly, cross-project contamination could occur
2. **Relevance Pollution**: One project's memories might affect another's search relevance scoring
3. **Resource Contention**: Heavy usage by one project could affect others

### Separate Instances Approach Benefits:
1. **Absolute Isolation**: Zero risk of cross-project bleed or contamination
2. **Project-Specific Tuning**: Each project can optimize its memory/DB independently
3. **Simplified Security Model**: Clear boundaries between projects
4. **No Relevance Interference**: Projects don't affect each other's memory search results

### Separate Instances Drawbacks:
1. **Lost Cross-Project Learning**: Cannot benefit from patterns discovered in other projects
2. **Increased Infrastructure Complexity**: N services to maintain instead of 1
3. **No Global Memory View**: Impossible to search or learn across projects
4. **Higher Maintenance Overhead**: Backups, updates, monitoring multiplied by N
5. **Contradicts System Goals**: AI_PROJECTS_SPACE is designed as a continuity system where learning accumulation across projects is valuable

## Recommendation

**MAINTAIN THE CURRENT ARCHITECTURE** but strengthen the isolation mechanisms:

The current shared-but-isolated approach is better aligned with the system's goals as a "multi-agent continuity system for long-running projects with persistent memory, reasoning, learning and self improvement." The ability to accumulate and share learnings across projects is a feature, not a bug.

However, to address contamination concerns, we recommend:

### Verification & Strengthening Current Isolation:
1. **Verify MuninnDB Tagging Works Correctly**: Test that project-scoped bootstrapping and learning storage properly isolates memories
2. **Audit Learning Extraction Processes**: Ensure all learning storage includes proper project tags
3. **Monitor for Cross-Project Bleed**: Periodically check that memories from one project don't inappropriately appear in another's context
4. **Document Best Practices**: Create clear guidelines for project-scoped memory usage

### When Separate Instances Might Be Warranted:
Only consider separate MuninnDB/SQLite instances if:
1. A project deals with highly sensitive/confidential data that absolutely cannot risk any cross-project exposure
2. A project has radically different memory/usage patterns that would interfere with others
3. Legal/compliance requirements mandate complete data isolation

Even in these cases, consider:
- Using encrypted namespaces/tags within the shared MuninnDB instead of separate instances
- Leveraging the existing project-ledger model for SQL isolation
- Applying strict project-scoping at the bootstrap/learning level

## Verification Approach

To verify the current isolation is working:
1. Test project-specific bootstrapping only loads appropriate memories
2. Verify learning storage with project tags doesn't bleed to other projects
3. Check that PROJECT_STATUS.md and other project-specific files remain isolated
4. Confirm gitnexus impact analysis stays within project boundaries when appropriately scoped

## Implementation Best Practices

### For SQL Isolation (Already Implemented):
- Use project-specific ledger databases: `SYSTEM/state/project_ledgers/{project-slug}.db`
- The `db_utils.py` already supports project-scoped operations

### For MuninnDB Isolation:
- Always use project-scoped bootstrapping: `muninn-cli bootstrap {project-name}`
- Store learnings with proper project tags:  
  `muninn-cli store "learning content" "concept" "{project-name},relevant-tags"`
- Query learning with project scope:  
  `python3 db_utils.py learning-query-project {project-name}`

### Critical Protocols to Follow:
1. **Always bootstrap before project work**:  
   `cd "/media/al/AI_DATA/AI_PROJECTS_SPACE" && ./bootstrap_global.sh`  
   Then: `./bootstrap.sh {project-name}`
2. **Use project-specific tags when storing learnings**:  
   Include the project name in all learning tags
3. **Rely on project-ledger databases for SQL isolation** (already implemented)
4. **Test before making changes** to isolation mechanisms

## Verification Commands

To check current isolation status:

```bash
# Check MuninnDB status
cd "/media/al/AI_DATA/AI_PROJECTS_SPACE" && muninn-cli status

# Query learnings for a specific project
cd "/media/al/AI_DATA/AI_PROJECTS_SPACE/SYSTEM/state" && \
python3 db_utils.py learning-query-project TSTR.directory

# Verify no cross-project bleed (should return minimal/no unrelated learnings)
cd "/media/al/AI_DATA/AI_PROJECTS_SPACE/SYSTEM/state" && \
python3 db_utils.py learning-query-project ai-projects-space | grep -i tstr || echo "No TSTR learnings in system project (good)"
```

## Conclusion

The current architecture provides appropriate isolation while preserving the valuable cross-project learning capabilities that are central to the AI_PROJECTS_SPACE continuity system. By strengthening verification practices and ensuring consistent use of project-scoping mechanisms, we can maintain effective isolation without sacrificing the system's core benefits.

This approach aligns with the First Principles thinking encouraged in our methodology: we've identified the core requirement (preventing harmful cross-project contamination) while preserving the fundamental value proposition (cross-project learning and continuity).

---

*Analysis conducted: 2026-05-24*  
*Based on exploration of: TSTR.directory project structure, CLAUDE.md documentation, AGENTS.md guidelines, and system architecture*