# MEMORY.md Template & Starter Guide

## Quick Start

Create `MEMORY.md` in your memory directory (e.g., `~/.claude/agent-memory/<name>/` or project `.claude/memory/`):

```markdown
---
name: Agent Memory Index
description: Central index for agent long-term memory
created: 2025-06-20
last-reviewed: 2025-06-20
---

# Memory Index

## Recent Feedback (newest first)
- [2025-06-20] Always verify file exists before reading — prevents crashes
  → `feedback/file-operations.md`
- [2025-06-19] Use `set -euo pipefail` in all bash scripts
  → `feedback/shell-scripts.md`

## Methodology Improvements
- [2025-06-18] React optimization priority: waterfalls > bundles > re-renders
  → `methodology/react-performance.md`
- [2025-06-15] Pentest recon sequence: passive → active → service scan
  → `methodology/pentest-recon.md`

## Key Knowledge
- Python asyncio patterns → `knowledge/python-async.md`
- JWT security best practices → `knowledge/jwt-security.md`
- SQL injection WAF bypass techniques → `knowledge/sql-injection.md`

## Reusable Patterns
- API error handling pattern → `patterns/api-error-handling.md`
- Database migration checklist → `patterns/db-migrations.md`
```

## Topic File Templates

### Feedback Template

```markdown
---
name: [Topic] Corrections and Insights
description: Mistakes made and lessons learned about [topic]
type: feedback
created: 2025-06-20
updated: 2025-06-20
---

# [Topic] Feedback Log

## 2025-06-20: [Brief Title]
**Mistake:** [What went wrong]
**Correction:** [What to do instead]
**Context:** [When/where this applies]
**Source:** [Original task that triggered this]
```

### Methodology Template

```markdown
---
name: [Domain] Methodology
description: Improved workflows for [domain]
type: methodology
created: 2025-06-20
updated: 2025-06-20
---

# [Domain] Methodology

## Current Best Practice
1. Step one
2. Step two (updated 2025-06-20: added verification)
3. Step three

## Rationale
[Why this order / these steps]

## Common Pitfalls
- Pitfall 1 → Solution
- Pitfall 2 → Solution

## History
- 2025-06-20: Initial methodology
```

### Knowledge Template

```markdown
---
name: [Topic] Knowledge Base
description: Key facts and definitions about [topic]
type: knowledge
created: 2025-06-20
updated: 2025-06-20
confidence: high
---

# [Topic] Knowledge

## Key Facts
- Fact 1 (source: [link or experience])
- Fact 2 (source: [link or experience])

## Definitions
- **Term**: Definition

## Rules of Thumb
- Rule 1
- Rule 2

## Related
- Links to other memory files
```

### Pattern Template

```markdown
---
name: [Domain] Solution Patterns
description: Recurring solution patterns for [domain]
type: pattern
created: 2025-06-20
updated: 2025-06-20
---

# [Domain] Patterns

## Pattern: [Name]
**Problem:** [What situation triggers this]
**Solution:** [Step-by-step]
**Example:** [Concrete code or command example]
**When to use:** [Conditions]
**When NOT to use:** [Anti-conditions]

## Pattern: [Name]
...
```

## Directory Structure Examples

### Minimal Setup (Getting Started)
```
memory/
  MEMORY.md           # Index (< 200 lines)
  feedback.md         # All corrections
  methodology.md      # Process improvements
```

### Standard Setup (Recommended)
```
memory/
  MEMORY.md           # Index (< 200 lines)
  feedback/
    file-operations.md
    shell-scripts.md
    web-security.md
  methodology/
    react-development.md
    pentest-recon.md
  knowledge/
    python-patterns.md
    jwt-security.md
  patterns/
    api-error-handling.md
    db-migrations.md
```

### Advanced Setup (High Volume)
```
memory/
  MEMORY.md           # Index (< 200 lines)
  feedback/
    [topic-specific files]
  methodology/
    [domain-specific files]
  knowledge/
    [topic-specific files]
  patterns/
    [domain-specific files]
  archive/             # Old entries
    2025-q1/
    2025-q2/
```

## Size Management Rules

1. **MEMORY.md**: Hard limit 200 lines. Exceed → move content to topic files.
2. **Individual topic files**: Soft limit 500 lines. Exceed → split by subtopic.
3. **Archive quarterly**: Move entries older than 90 days to `archive/`.
4. **Delete obsolete**: If a fact/tool/pattern is no longer relevant, delete it.

## Naming Conventions

- **Files**: `kebab-case-descriptive-name.md`
- **Names in frontmatter**: Short but specific ("React Hooks" not "Frontend")
- **Dates**: ISO 8601 (`2025-06-20`)
- **Tags**: comma-separated, lowercase, hyphenated

## Frontmatter Required Fields

| Field | Required | Description |
|---|---|---|
| `name` | Yes | Short descriptive title |
| `description` | Yes | One-line relevance hint for retrieval |
| `type` | Yes | `feedback` \| `methodology` \| `knowledge` \| `pattern` |
| `created` | Recommended | ISO date |
| `updated` | Recommended | ISO date |
| `confidence` | Optional | `low` \| `medium` \| `high` |
| `tags` | Recommended | Comma-separated keywords |
| `source` | Optional | Original task or reference |
