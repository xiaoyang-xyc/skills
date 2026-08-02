# Knowledge Consolidation Pipeline

## Overview

Raw episodic memories (task logs) must be refined into durable semantic knowledge through a multi-stage consolidation pipeline. This prevents memory bloat and ensures stored knowledge is actionable.

## The Consolidation Stages

### Stage 1: Episode Capture
**When**: Immediately after task completion
**Input**: Raw task execution trace
**Output**: Episodic memory entry

```markdown
---
name: Failed exploit attempt via SQLMap
description: SQLMap WAF bypass attempt failed, manual injection succeeded
type: episodic
source: web-pentest-2025-06-15
date: 2025-06-15
tags: sql-injection, waf-bypass, sqlmap, manual
---

Tried SQLMap with --tamper=space2comment on target with ModSecurity WAF.
Result: Blocked (403). Manual time-based blind injection with custom
User-Agent rotation succeeded. Extracted DB name in ~12min.
```

### Stage 2: Pattern Recognition
**When**: After 3+ similar episodes
**Input**: Related episodic entries
**Output**: Pattern abstraction

```markdown
---
name: WAF bypass pattern for SQL injection
description: When SQLMap fails against WAF, switch to manual with rotation
type: pattern
confidence: medium  # 3 episodes observed
source: consolidation-from-episodes
date: 2025-06-20
tags: sql-injection, waf-bypass, pattern
---

## Pattern
When automated SQLi tools fail against WAF:
1. Don't abandon — WAFs often miss manual crafted payloads
2. Rotate User-Agent + add delays between requests
3. Start with time-based blind (least likely to trigger WAF)
4. Only if time-based works, try error-based or UNION

## Evidence
- 2025-06-12: sqlmap blocked, manual succeeded (target: XX)
- 2025-06-15: sqlmap blocked, manual succeeded (target: YY)
- 2025-06-18: sqlmap blocked, manual succeeded (target: ZZ)

## Counter-evidence
- None so far — always succeeded with manual after sqlmap failed
```

### Stage 3: Semantic Rule Extraction
**When**: Pattern has been validated across 3+ successful applications
**Input**: Stable pattern
**Output**: Semantic rule

```markdown
---
name: SQL injection WAF bypass heuristic
description: Prioritize manual injection when WAF detected and sqlmap blocked
type: semantic
confidence: high  # 5+ successful validations
date: 2025-07-01
tags: sql-injection, waf, heuristic, rule
---

## Rule
If WAF detected AND automated SQLi tool blocked → Switch to manual time-based
blind injection with request rotation within 5 minutes.

## Rationale
WAFs pattern-match known tool signatures. Manual payloads bypass signature
matching while maintaining effectiveness. Time-based blind has lowest
false-positive rate for WAF detection.

## Confidence Level
HIGH — validated 5/5 times since pattern identified.

## When to Re-evaluate
If validation rate drops below 80% over next 10 applications.
```

### Stage 4: Procedural Integration
**When**: Semantic rule proves stable over time
**Input**: High-confidence semantic rule
**Output**: Updated workflow/checklist/skill

Update procedural memory (e.g., modify pentest methodology):
```markdown
## SQL Injection Testing (Updated)

1. [NEW] Check for WAF presence (via response headers / wafw00f)
2. [NEW] If WAF present → skip automated tools, go to manual
3. Run sqlmap with --batch --level=3 --risk=1 (quick scan)
4. If sqlmap blocked → manual time-based blind with rotation
5. If DBMS identified → use database-specific payloads
6. Document bypass technique for report
```

### Stage 5: Archive
**When**: Rules are integrated into procedural memory
**Input**: Raw episodes and intermediate patterns
**Output**: Archive (or deletion)

Move raw episodes to `archive/` or delete if fully consolidated. Keep pattern file with reference to integrated rule.

## Consolidation Trigger Conditions

| Condition | Action |
|---|---|
| 3+ similar episodic entries | Create pattern |
| Pattern validated 3+ times | Promote to semantic rule |
| Rule stable for 30 days | Integrate into procedural memory |
| Rule fails 2+ times | Demote confidence, revisit pattern |
| Pattern contradicted by evidence | Add counter-evidence, re-evaluate |

## Maintenance Rules

1. **Weekly**: Review new episodic entries for emerging patterns
2. **Monthly**: Run consolidation on unprocessed episodes
3. **Quarterly**: Review semantic rules for staleness
4. **Annually**: Full memory audit — archive or delete obsolete content
